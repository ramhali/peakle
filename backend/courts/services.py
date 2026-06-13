from django.db import transaction

from .models import Court, CourtImage, CourtAmenity, CourtSchedule

@transaction.atomic
def create_court(owner, data):
    court = Court.objects.create(
        owner=owner,
        court_name=data.get('court_name'),
        court_type=data.get('court_type'),
        location=data.get('location'),
        rate=data.get('rate'),
        description=data.get('description'),
    )

    # Create associated images and amenities if provided
    court_images = data.get('court_images', [])
    for image in court_images:
        CourtImage.objects.create(court=court, image=image)

    court_amenities = data.get('court_amenities', [])
    for amenity in court_amenities:
        CourtAmenity.objects.create(court=court, amenity_name=amenity)

    court_schedules = data.get('court_schedules', [])
    for schedule in court_schedules:
        CourtSchedule.objects.create(
            court=court,
            day_of_week=schedule['day_of_week'],
            opening_time=schedule['opening_time'],
            closing_time=schedule['closing_time']
            )
        
    return court