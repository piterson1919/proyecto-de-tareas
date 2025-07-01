from django.db import models 
from django.contrib.auth.models import User 

class Task(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=100)
    importance = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    

class Evento(models.Model):
    titulo = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    fecha_inicio = models.DateTimeField()
    fecha_fin = models.DateTimeField()

