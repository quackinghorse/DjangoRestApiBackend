from django.db import models
from django.contrib.auth.hashers import make_password

class Student(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    fee = models.IntegerField()
    email = models.EmailField(unique=True, null=True, blank=True)
    password = models.CharField(max_length=128, null=True, blank=True)  # Large enough to store hashed passwords

    def save(self, *args, **kwargs):
        if not self.pk or 'password' in self.get_dirty_fields():
            self.password = make_password(self.password)
        super().save(*args, **kwargs)
