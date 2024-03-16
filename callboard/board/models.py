from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save

# Create your models here.


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    announcement = models.ForeignKey('Announcement', on_delete=models.CASCADE)
    content = models.TextField()

    def __str__(self):
        return f'Comment by {self.user.username} on {self.announcement.title}'


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    follows = models.ManyToManyField("self",
                                     related_name="followed_by",
                                     symmetrical=False,
                                     blank=True)
    date_modified = models.DateTimeField(User, auto_now=True)
    comments = models.ManyToManyField(Comment,
                                       related_name="commented_by",
                                       blank=True)

    def __str__(self):
        return self.user.username


def create_profile(sender, instance, created, **kwargs):
    if created:
        user_profile = Profile(user=instance)
        user_profile.save()
        user_profile.follows.set([instance.profile.id])
        user_profile.save()


post_save.connect(create_profile, sender=User)


class Author(models.Model):
    name = models.CharField(max_length=255)
    users = models.OneToOneField(User, on_delete=models.CASCADE)


class Category(models.Model):
    name = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return f'{self.name.title()}'


class Announcement(models.Model):
    title = models.CharField(max_length=100)
    text = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    author = models.ForeignKey(User, default=1, on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='images/', null=True, blank=True)
    video = models.FileField(upload_to='videos/', null=True, blank=True)
    likes = models.ManyToManyField(User, related_name="ad_like", blank=True)
    comments = models.ManyToManyField(Comment, related_name="commented_on", blank=True)

    def __str__(self):
        return f'{self.title.title()}: {self.text[:20]}'

    def likes_number(self):
        return self.likes.count()