from django.db import models

# Create your models 
class User(models.Model):
    username = models.CharField(max_length=50, default=True)
    fname = models.CharField(max_length=50, default=True)
    lname = models.CharField(max_length=50, default=True)
    email = models.CharField(max_length=50, default=True)
    password = models.CharField(max_length=50, default=True)
    conf_pass = models.CharField(max_length=50, default=True)

    def __str__(self):
        return self.username