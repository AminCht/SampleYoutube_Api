from django.core.validators import FileExtensionValidator
from django.db import models

# Create your models here.
from core.models import User


class AppUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birth_date = models.DateField(null=True)
    phone_number = models.CharField(max_length=255)
    MEMBERSHIP_PREMIUM = 'P'
    MEMBERSHIP_NORMAL = 'N'
    MEMBERSHIP_CHOICES = [
        (MEMBERSHIP_NORMAL, 'Normal'),
        (MEMBERSHIP_PREMIUM, 'Premium')
    ]
    MEMBERSHIP_STATUS = models.CharField(max_length=1, choices=MEMBERSHIP_CHOICES, default=MEMBERSHIP_NORMAL)


class Collection(models.Model):
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title


class Content(models.Model):
    app_user = models.ForeignKey(AppUser, on_delete=models.CASCADE)
    file = models.FileField(upload_to='app/contents', validators=[FileExtensionValidator(allowed_extensions=['mp4'])])
    title = models.CharField(max_length=255)
    description = models.TextField()
    upload_date = models.DateTimeField(auto_now=True)
    collection = models.ForeignKey(Collection, on_delete=models.PROTECT)


class Comment(models.Model):
    description = models.TextField()
    user = models.ForeignKey(AppUser, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now=True)


class Subscriber(models.Model):
    app_user = models.ForeignKey(AppUser, on_delete=models.CASCADE, related_name='subscribers')
    user = models.ForeignKey(AppUser, on_delete=models.CASCADE)


class History(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.ForeignKey(Content, on_delete=models.CASCADE)


class LikeItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.ForeignKey(Content, on_delete=models.CASCADE)

