from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Annonces(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100, blank=True, default='')
    description = models.TextField()
    updated = models.DateTimeField(auto_now = True, blank = True)
    user = models.ForeignKey(User, on_delete = models.CASCADE, blank = True, null = True)

 
    class Meta:
        ordering = ['created']
    
    def __str__(self):
        return self.title
