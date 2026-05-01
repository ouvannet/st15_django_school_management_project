from django.db import models
from project_1.models.position import Position

class Staff(models.Model):
    id = models.AutoField(primary_key=True)
    last_name = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    gender = models.CharField(max_length=10, choices=[
        ('male', 'Male'),   
        ('female', 'Female'),
        ('other', 'Other'),
    ])
    date_of_birth = models.DateField()
    # position_id = models.IntegerField()
    position = models.ForeignKey(Position, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    class Meta:
        app_label = 'core'