from django.core.mail import mail_managers
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Comment
