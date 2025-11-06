from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.models import User  
from django.contrib.auth import authenticate, login, logout  
from .models import Task
from .forms import Taskform
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
import io
import qrcode
from django.http import HttpResponse
from django.conf import settings
from .models import Evento
from .forms import EventoForm
from django.http import JsonResponse



class AsistenciaIframeView(TemplateView):
    template_name = "asistence.html"
    
# inicio de la aplicacion
def home(request):
    return render(request, 'home.html')

#login de la aplicacion
def loguin(request):
    if request.method == 'GET':
        return render(request,'login.html')
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password1'])
        if user is None:
            return render(request, 'login.html', { 'error': 'Usuario o contraseña incorrectos'})
        else:
            login(request, user)
            return redirect('tasks')

#registro de la aplicacion
def register(request):
    if request.method == 'GET':
        return render (request,'register.html')
    else:
        if request.POST['password1'] == request.POST['password2']:
            
                user = User.objects.create_user(username=request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('tasks')
            
        else:
            return render(request, 'register.html', {'error': 'las contraseñas no coinciden'})

#tareas de la aplicacion
@login_required
def tasks(request):
        tasks = Task.objects.filter(user=request.user)
        return render(request,'tasks.html',{'tasks': tasks})

#crear tarea
@login_required
def create_task(request):
    if request.method == 'GET':
        return render(request, 'create_task.html', {'form': Taskform()})
    else:
        form = Taskform(request.POST)
        nueva_tarea = form.save(commit=False)
        nueva_tarea.user = request.user
        nueva_tarea.save()
        return redirect('tasks')

#detalles de la tarea
@login_required
def task_detail(request, task_id):
    if request.method == 'GET':
        task = get_object_or_404(Task, id=task_id, user=request.user)
        form = Taskform(instance=task)
        return render(request, 'task_detail.html', {'form': form, 'task': task})
    else:
        try:
            task = get_object_or_404(Task, id=task_id, user=request.user)
            form = Taskform(request.POST, instance=task)
            form.save()
            return redirect('tasks')
        except ValueError:
            return render(request, 'task_detail.html', {'form': form, 'task': task, 'error': 'error al actualizar la tarea'})

#borrar la tarea
@login_required
def delete_task(request,task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    if request.method == 'POST':
        task.delete()
        return redirect('tasks')
    
def singout(request):
    logout(request)
    return redirect('home')

#imagen de el qr

def attendance_qr_image(request):
    form_url = "https://docs.google.com/forms/d/e/1FAIpQLSco21m73FzunFwdhCEjHtXWI7JbOWucbJCnP0AG91h-LN0lRw/viewform?usp=header"
    
    qr_img = qrcode.make(form_url)
    
    buffer = io.BytesIO()
    qr_img.save(buffer, format='PNG')
    buffer.seek(0)
    
    return HttpResponse(buffer.getvalue(), content_type='image/png')

#pagina de la asistencia
def attendance_qr_page(request):
    return render(request, 'asistence.html')

#crear un evento
def crear_evento(request):
    if request.method == 'POST':
        form = EventoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('ver_calendario')
    else:
        form = EventoForm()
    return render(request, 'crear_evento.html', {'form': form})

#calendario
def ver_calendario(request):
    return render(request, 'calendario.html')

#detalles de el evento
def eventos_json(request):
    eventos = Evento.objects.all()
    data = [{
        'title': e.titulo,
        'start': e.fecha_inicio.isoformat(),
        'end': e.fecha_fin.isoformat(),
    } for e in eventos]
    return JsonResponse(data, safe=False)

# creador: piter.RA