from django.db import models
from django.conf import settings
from django.utils.text import slugify 
from django.urls import reverse 
import time
from django.utils import timezone
from django.contrib.auth.models import User
from account.models import Profile
class Forum(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    desc = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def save(self, *args, **kwargs):
        if self.pk is None: 
            self.slug = slugify(self.title) + '-' + time.strftime("%Y%m%d%H%M%S")
        super(Forum, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('forum-list')

    def __str__(self):
        return self.title
    
class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    forum = models.ForeignKey(Forum, on_delete=models.CASCADE)
    desc = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    edited = models.BooleanField(default=False)
    edited_at = models.DateTimeField(null=True, blank=True)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='replies', on_delete=models.CASCADE)
    def get_absolute_url(self):
        return reverse('forum-detail', kwargs={'slug': self.forum.slug})
    def save(self, *args, **kwargs):
        if self.pk:
            self.edited = True
            self.edited_at = timezone.now()
        super().save(*args, **kwargs)