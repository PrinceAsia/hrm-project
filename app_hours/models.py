from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from users.models import City, CustomUser


# Create your models here.
class WorkPlaces(models.Model):
    place_name = models.CharField(max_length=100, unique=True)
    place_city = models.ForeignKey(City, on_delete=models.CASCADE)
    place_address = models.TextField()

    def __str__(self):
        return self.place_name

    class Meta:
        ordering = ['place_name']
        db_table = 'workplaces'


class WorkingHours(models.Model):
    work_day = models.DateField()
    work_hours = models.FloatField(validators=[MinValueValidator(0.5), MaxValueValidator(10.0)])
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    work_place = models.ForeignKey(WorkPlaces, on_delete=models.CASCADE)
    work_desc = models.TextField()

    def __str__(self):
        return f"{self.work_day} - {self.work_hours} - {self.user.username}"

    class Meta:
        ordering = ['work_day']
        db_table = 'working_hours'
        unique_together = ('work_day', 'user')
