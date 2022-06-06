from distutils.command.upload import upload
from tkinter import CASCADE, image_names
from django.db import models
from django.urls import reverse

from django.contrib.auth.models import User

# from django.db.models.signals import Image_save
from django.dispatch import receiver
# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    profile_picture = models.ImageField(upload_to='images/', default='default.png')
    bio = models.TextField(max_length=500, default="My Bio", blank=True)

    def __str__(self):
        return f'{self.user.name} Profile'

    # @receiver(Image_save, sender=User)
    # def create_user_profile(sender, instance, created, **kwargs):
    #     if created:
    #         Profile.objects.create(user=instance)

    # @receiver(Image_save, sender=User)
    # def save_user_profile(sender, instance, **kwargs):
    #     instance.profile.save()

    def save_profile(self):
        self.user

    def delete_profile(self):
        self.delete()

    @classmethod
    def search_profile(cls, name):
        return cls.objects.filter(user__username__icontains=name).all()

class Image(models.Model):
    image=models.ImageField(upload_to='images/')
    image_name=models.CharField(max_length=60, blank=True)
    image_caption=models.CharField(max_length=60, blank=True)
    image_likes = models.ManyToManyField(User, related_name='likes', blank=True, )
    image_comments = models.ManyToManyField(User, related_name='comments', blank=True, )
    profile = models.ForeignKey(User, on_delete=models.CASCADE, related_name='images')
   
    
    @property
    def get_all_comments(self):
        return self.comments.all()

    def save_image(self):
        self.save()

    def delete_image(self):
        self.delete()

    def total_likes(self):
        return self.likes.count()

    def __str__(self):
        return f'{self.user.name} Image'
    
    def get_absolute_url(self):
        return f"/Image/{self.id}"

    class Meta:
       ordering = ["-pk"]

class Comments(models.Model):
    comment = models.TextField()
    image = models.ForeignKey(Image, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='comments')
    
      
   

    def __str__(self):
        return f'{self.user.name} Image'

class Likes(models.Model):
    likes = models.IntegerField()
    image = models.ForeignKey(Image, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='likes')
 
      
   

    def __str__(self):
        return f'{self.user.name} Image'

class Follow(models.Model):
    following = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.following

class Followers(models.Model):
    followers = models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        return self.followers