from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils import timezone
from django.views.decorators.http import require_http_methods

from .models import User

def index(request):
    return render(request, "login.html")

def login(request):

    if request.method == "POST":
        email = request.POST.get("email", "").strip().lower()
        password = request.POST.get("password", "")
        remember_me = bool(request.POST.get("remember_me"))
 
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            user = None
 
        if user is None or not user.check_password(password):
            messages.error(request, "Invalid email or password.")
            return render(request, "login.html", {"email": email})
 
        request.session["user_id"] = user.id
 
        if remember_me:
            request.session.set_expiry(60 * 60 * 24 * 30)  # 30 days
        else:
            request.session.set_expiry(0)  # expires on browser close
 
        return redirect("dashboard")
 
    return render(request, "login.html")
    

    
def signup(request):
    if request.method == "POST":
        full_name = request.POST.get("full_name", "").strip()
        email = request.POST.get("email", "").strip().lower()
        password = request.POST.get("password", "")
        confirm_password = request.POST.get("confirm_password", "")
        agreed_to_terms = bool(request.POST.get("agreed_to_terms"))
 
        errors = []
        if not full_name:
            errors.append("Full name is required.")
        if not email:
            errors.append("Email is required.")
        elif User.objects.filter(email=email).exists():
            errors.append("An account with this email already exists.")
        if not password:
            errors.append("Password is required.")
        elif password != confirm_password:
            errors.append("Passwords do not match.")
        if not agreed_to_terms:
            errors.append("You must agree to the Terms & Conditions.")
 
        if errors:
            for e in errors:
                messages.error(request, e)
            return render(request, "signup.html", {"full_name": full_name, "email": email})
 
        user = User(
            full_name=full_name,
            email=email,
            agreed_to_terms=True,
            terms_agreed_at=timezone.now(),
        )
        user.set_password(password)
        user.save()
 
        messages.success(request, "Account created successfully. You can log in now.")
        request.session["user_id"] = user.id
        return redirect("signup")
 
    return render(request, "signup.html")
 
 
@require_http_methods(["GET", "POST"])
def logout_view(request):
    request.session.flush()
    return redirect("login")
 
 
def dashboard_view(request):
    user_id = request.session.get("user_id")
    if not user_id:
        return redirect("login")
 
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        request.session.flush()
        return redirect("login")
 
    return render(request, "login.html")