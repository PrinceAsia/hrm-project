from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class Jobs(models.Model):
    job_title = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.job_title

    class Meta:
        db_table = 'jobs'
        ordering = ['job_title']
        verbose_name = 'Job'
        verbose_name_plural = 'Jobs'


class City(models.Model):
    city_name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.city_name

    class Meta:
        db_table = 'cities'
        ordering = ['city_name']
        verbose_name = 'City'
        verbose_name_plural = 'Cities'


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True, verbose_name='email address')
    phone = models.CharField(max_length=15, verbose_name='Phone', unique=True, null=True, blank=True)
    start_date = models.DateField(verbose_name='Start date', null=True, blank=True)
    avatar = models.ImageField(upload_to='images/avatars', default='images/avatars/default.png')

    city = models.ForeignKey(City, on_delete=models.PROTECT, verbose_name='City', null=True, blank=True)
    job = models.ForeignKey(Jobs, on_delete=models.PROTECT, verbose_name='Job', null=True, blank=True)

    REQUIRED_FIELDS = []
    USERNAME_FIELD = 'email'

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        db_table = 'users'
        ordering = ['first_name', 'last_name']
        verbose_name = 'User'
        verbose_name_plural = 'Users'
