from django import forms   
from django.forms import ModelForm
from .models import Task, Evento

class Taskform(ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'importance']
        
class EventoForm(forms.ModelForm):
    class Meta:
        model = Evento
        fields = ['titulo', 'descripcion', 'fecha_inicio', 'fecha_fin']
        widgets = {
            'fecha_inicio': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'fecha_fin': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }
