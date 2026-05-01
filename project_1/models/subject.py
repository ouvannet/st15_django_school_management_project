from django.db import models
from django.contrib.auth.models import User

class Subject(models.Model):
    id = models.AutoField(primary_key=True)
    subject_name = models.CharField(max_length=100)
    created_at=models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, related_name='created_subjects', on_delete=models.SET_NULL, null=True)

    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(User, related_name='updated_subjects', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    class Meta:
        app_label = 'core'