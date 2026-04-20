"""
Optional: Run this to seed sample data.
Usage: python manage_seed.py
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wanderly.settings')
django.setup()

from accounts.models import User
from locations.models import City
from partners.models import Partner, Hotel, Agency, Restaurant, Coffee

# Create admin
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@wanderly.com', 'admin123', role='admin')
    print("Created admin: admin / admin123")

# Create cities
cities_data = [
    ('Algiers', 'The vibrant capital of Algeria, blending Ottoman history with modern culture.'),
    ('Oran', 'A coastal gem known for its music, beaches, and Mediterranean vibe.'),
    ('Constantine', 'City of bridges — dramatic ravines and ancient Roman heritage.'),
    ('Sétif', 'Gateway to the eastern highlands, known for its mosaics and nature.'),
]
cities = {}
for name, desc in cities_data:
    city, created = City.objects.get_or_create(name=name, defaults={'description': desc})
    cities[name] = city
    if created:
        print(f"Created city: {name}")

# Create partner users
partner_data = [
    ('hotel_algiers', 'Hotel El Aurassi', 'hotel', 'Algiers', 'Luxury hotel with panoramic bay views.'),
    ('agency_travel', 'Sahara Tours', 'agency', None, 'Premier travel agency for Algerian adventures.'),
    ('restaurant_oran', 'La Méditerranée', 'restaurant', 'Oran', 'Fresh seafood and traditional Algerian cuisine.'),
    ('cafe_constantine', 'Café des Ponts', 'coffee', 'Constantine', 'Historic café overlooking the gorges.'),
]

for username, fullname, ptype, city_name, desc in partner_data:
    if not User.objects.filter(username=username).exists():
        u = User.objects.create_user(username=username, password='partner123', role='partner',
                                      first_name=fullname.split()[0], last_name=' '.join(fullname.split()[1:]))
        p = Partner.objects.create(user=u, partner_type=ptype, phone='+213 555 000 000',
                                   description=desc, is_approved=True,
                                   verification_document='verifications/sample.pdf')
        city = cities.get(city_name) if city_name else None
        if ptype == 'hotel':
            Hotel.objects.create(partner=p, city=city)
        elif ptype == 'agency':
            Agency.objects.create(partner=p)
        elif ptype == 'restaurant':
            Restaurant.objects.create(partner=p, city=city)
        elif ptype == 'coffee':
            Coffee.objects.create(partner=p, city=city)
        print(f"Created partner: {username} / partner123")

print("\n✅ Seed complete! Login at /admin/ with admin/admin123")
