from django.db import models

# Create your models here.
class Court(models.Model):
    court_id = models.AutoField(primary_key=True)
    owner = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='courts')
    court_name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    rate = models.DecimalField(max_digits=6, decimal_places=2)
    description = models.TextField(blank=True)

class CourtImage(models.Model):
    court = models.ForeignKey('courts.Court', on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to="court_images/")
    uploaded_at = models.DateTimeField(auto_now_add=True)

class CourtAmenity(models.Model):
    court = models.ForeignKey('courts.Court', on_delete=models.CASCADE, related_name='amenities')
    amenity_name = models.CharField(max_length=255)

class CourtLink(models.Model):
    court = models.ForeignKey('courts.Court', on_delete=models.CASCADE, related_name='links')
    link_url = models.URLField()
    description = models.CharField(max_length=255, blank=True)

class CourtSchedule(models.Model):
    court = models.ForeignKey('courts.Court', on_delete=models.CASCADE, related_name='schedules')
    day_of_week = models.CharField(max_length=20)
    opening_time = models.TimeField()
    closing_time = models.TimeField()

class CourtReview(models.Model):
    court = models.ForeignKey('courts.Court', on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='court_reviews')
    review_text = models.TextField()
    rating = models.IntegerField(max_length=5)
    date_reviewed = models.DateTimeField(auto_now_add=True)