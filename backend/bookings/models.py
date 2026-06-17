from django.db import models

# Create your models here.
class Booking(models.Model):
    RESERVATION_STATUS = [
        ('awaiting_payment', 'Awaiting Payment'), # slot reserved, payment not yet submitted
        ('awaiting_confirmation', 'Awaiting Confirmation'), # payment proof submitted, waiting for owner review
        ('confirmed', 'Confirmed'), # reservation approved
        ('cancelled', 'Cancelled'), # cancelled by user or owner
        ('expired', 'Expired'), # payment window elapsed
    ]

    booking_id = models.AutoField(primary_key=True)
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='bookings')
    court = models.ForeignKey('courts.Court', on_delete=models.CASCADE, related_name='bookings')
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    status = models.CharField(choices=RESERVATION_STATUS, default='awaiting_payment')
    is_open_match = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

class OpenMatch(models.Model):
    SKILL_LEVELS = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    ]

    MATCH_TYPES = [
        ('casual', 'Casual'),
        ('tournament', 'Tournament'),
        ('open_play', 'Open Play'),
    ]

    match_id = models.AutoField(primary_key=True)
    reservation = models.OneToOneField(Booking, on_delete=models.CASCADE, related_name='open_match')
    skill_level = models.CharField(max_length=20, choices=SKILL_LEVELS, default='beginner')
    type = models.CharField(choices=MATCH_TYPES, default='casual')
    max_players = models.IntegerField(default=2)
    description = models.TextField(blank=True)

class MatchParticipant(models.Model):
    PARTICIPATION_STATUS = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
        ('expired', 'Expired'),
    ]

    match = models.ForeignKey(OpenMatch, on_delete=models.CASCADE, related_name='participants')
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='matches_joined')
    joined_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(choices=PARTICIPATION_STATUS, default='pending')

    class Meta:
        unique_together = ('match', 'user')