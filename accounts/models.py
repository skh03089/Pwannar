from django.db import models
from django.conf import settings




class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    image = models.ImageField(
        upload_to='profile/%Y/%m/%d',
        blank=True,
        null=True,
    )
    birth_date = models.DateField(null=True, blank=True)
    school = models.CharField(max_length=50, blank=True, null=True)
    location = models.CharField(max_length=30, blank=True, null=True)
    bio = models.TextField(max_length=500, blank=True, null=True)
    history = models.TextField(blank=True, null=True)


    def image_url(self):
        if self.image:
            image_url = self.image.url
        else:
            image_url = '/static/img/default_profile_image.jpg'
        return image_url

    def __str__(self):
        return str(self.user)