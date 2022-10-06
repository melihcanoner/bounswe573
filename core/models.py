from cgitb import text
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.utils.text import slugify
from django.urls import reverse
import time


class User(AbstractUser):
    pass


class Questions(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    text = models.TextField()
    created_on = models.DateTimeField(auto_now=True)
    updated_on = models.DateTimeField(auto_now_add=True)




class Answers(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    question = models.ForeignKey(Questions, on_delete=models.CASCADE)
    text = models.TextField()
    created_on = models.DateTimeField(auto_now=True)


class Learningspace(models.Model):
   
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    desc = models.TextField(blank=True, null = True)
    created_on = models.DateTimeField(auto_now_add=True)
    

    def save(self, *args, **kwargs):
        if self.pk is None:
            self.slug = slugify(self.title) + '-' + time.strftime('%Y%m%d%H%M%S')
        super(Learningspace, self).save(*args, **kwargs)

    def get_absolute_url(self): 
        return reverse('home')
        
    def __str__(self):
        return self.title

class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    slug = models.ForeignKey(Learningspace, on_delete=models.CASCADE)
    desc = models.TextField(blank=True, null = True)
    created_at = models.DateTimeField(auto_now_add=True)