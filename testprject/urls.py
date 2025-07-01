from django.contrib import admin
from django.urls import path
from app import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home,name='home'),
    path('login/', views.loguin,name='login'),
    path('tasks/', views.tasks,name='tasks'),
    path('register/', views.register,name='register'),
    path('create_task/', views.create_task,name='create_task'),
    path('task/<int:task_id>/', views.task_detail, name='task_detail'),
    path('task/<int:task_id>/delete/', views.delete_task, name='delete_task'),
    path('logout/', views.singout, name='logout'),
    path('asistence/', views.attendance_qr_page, name="asistensia"),
    path('asistence/qr', views.attendance_qr_image, name="attendance_qr_image"),
    path('crear/', views.crear_evento, name='crear_evento'),
    path('calendario/', views.ver_calendario, name='ver_calendario'),
    path('eventos-json/', views.eventos_json, name='eventos_json'),
]



