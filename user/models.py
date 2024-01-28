from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=200, null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    email = models.EmailField(max_length=200, blank=True, null=True)
    locations = models.CharField(max_length=200, null=True, blank=True)
    profile_image = models.ImageField(
        null=True,
        blank=True,
        upload_to="profile/",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.username

    @property
    def get_followers(self):
        count = self.followed_by.count()
        return count

    @property
    def get_following(self):
        return Follow.objects.filter(user=self.user).count()


class Follow(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    followed = models.ForeignKey(
        User,
        related_name="followed_by",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
