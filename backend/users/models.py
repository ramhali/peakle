from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

# Create your models here.
class User(AbstractUser):
    SKILL_LEVELS = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    ]

    user_id = models.AutoField(primary_key=True)
    email = models.EmailField(unique=True)
    user_skill_level = models.CharField(max_length=20, choices=SKILL_LEVELS, default='beginner')
    phone_number = models.CharField(max_length=20, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)

class UserFollowing(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='following')
    following_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='followers')
    date_followed = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'following_user')


class UserReviews(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reviews')
    review_text = models.TextField()
    rating = models.IntegerField()
    date_reviewed = models.DateTimeField(auto_now_add=True)

class UserLinks(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='links')
    link_url = models.URLField()
    description = models.CharField(max_length=255, blank=True)