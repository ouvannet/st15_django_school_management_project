from django.db import models

class Position(models.Model):
    id = models.AutoField(primary_key=True)
    position_name = models.CharField(max_length=100, default="Manager")

    def __str__(self):
        return self.position_name

    class Meta:
        app_label = 'core'