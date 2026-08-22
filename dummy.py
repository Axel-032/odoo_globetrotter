from datetime import date, timedelta
from globetrotter.models import User, Trip

# create a couple dummy users
user1, _ = User.objects.get_or_create(
    email="test@example.com",
    defaults={"full_name": "Test User", "agreed_to_terms": True}
)
user2, _ = User.objects.get_or_create(
    email="test2@example.com",
    defaults={"full_name": "Second User", "agreed_to_terms": True}
)

trips_data = [
    {"name": "Goa Getaway", "description": "Beach trip with friends, lots of sun and seafood."},
    {"name": "Himalayan Trek", "description": "10-day trekking trip through the mountains."},
    {"name": "Europe Backpacking", "description": "3 weeks across 5 countries on a budget."},
    {"name": "Rajasthan Road Trip", "description": "Forts, deserts, and palaces across Rajasthan."},
    {"name": "Kerala Backwaters", "description": "Houseboat trip through the backwaters."},
    {"name": "Tokyo Adventure", "description": "City exploring, food, and technology."},
    {"name": "Bali Retreat", "description": "Relaxed trip focused on beaches and yoga."},
    {"name": "New York City Break", "description": "Quick weekend trip to see the city."},
]

for i, t in enumerate(trips_data):
    trip = Trip.objects.create(
        name=t["name"],
        description=t["description"],
        start_date=date.today() + timedelta(days=i * 30),
        end_date=date.today() + timedelta(days=i * 30 + 7),
    )
    trip.members.add(user1)
    if i % 2 == 0:  # add user2 to every other trip, to show shared trips
        trip.members.add(user2)

print(f"Created {len(trips_data)} trips.")