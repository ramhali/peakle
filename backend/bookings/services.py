from django.db import transaction

from .models import Booking, OpenMatch, MatchParticipant


@transaction.atomic
#need to check if the court is available for the given date and time before creating the booking
def create_booking(user, data):
    if Booking.objects.filter(
        court=data.get('court'),
        date=data.get('date'),
        start_time__lt=data.get('end_time'),
        end_time__gt=data.get('start_time'),
    ).exists():
        return None  # Court is not available

    booking = Booking.objects.create(
        user=user,
        court=data.get('court'),
        date=data.get('date'),
        start_time=data.get('start_time'),
        end_time=data.get('end_time'),
        is_open_match=data.get('is_open_match', False)
    )

    if data.get('is_open_match') and data.get('open_match_data'):
        # Create an open match booking
        open_match_data = data.get('open_match_data')
        OpenMatch.objects.create(
            reservation=booking,
            skill_level=open_match_data.get('skill_level'),
            type=open_match_data.get('type'),
            max_players=open_match_data.get('max_players'),
            description=open_match_data.get('description')
        )

    return booking

@transaction.atomic
def create_open_match_player(user, match):
    if match.participants.count() >= match.max_players:
        return "FULL"
    
    if MatchParticipant.objects.filter(
        match=match,
        user=user
    ).exists():
        return "ALREADY_JOINED"

    participant = MatchParticipant.objects.create(
        match=match,
        user=user,
        status='pending'
    )

    return participant