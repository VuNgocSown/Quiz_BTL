from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.templatetags.static import static
# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, related_name='profile', verbose_name='User Object')
    user_class = models.TextField(blank=True, null=True)
    email = models.EmailField(blank=True, null=True, max_length=254, unique=True)
    profile_img = models.ImageField(upload_to='profile_images', default='profile_images/user.jpg', blank=True, null=True, verbose_name='Profile Pic')
    studen_id = models.CharField(max_length=15, blank=True, null=True)
    GENDER = (
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    )
    gender = models.CharField(max_length=6, choices=GENDER, blank=True, null=True)
    
    def get_profile_img_url(self):
        if self.profile_img:
            return self.profile_img.url
        return static('images/user.jpg')
        
    def __str__(self):
        return self.user.username
    # get full name of user
    def full_name(self):
        return self.user.first_name + ' ' + self.user.last_name
