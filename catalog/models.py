from django.db import models
from django.urls import reverse  #Used to generate URLs by reversing the URL patterns
from django.contrib.auth.models import User, Group
from datetime import datetime, timedelta


# Create your models here.


class Proyecto(models.Model):
    """
    Modelo que representa un proyecto
    """
    idBacklog = models.AutoField(primary_key=True, help_text="ID único para este Proyecto")
    nombre = models.CharField(max_length=50, help_text="Ingrese el nombre del proyecto")
    descripcion = models.CharField(max_length=200, help_text="Ingrese una descripcion para el proyecto")
    fechaInicio = models.DateField()
    fechaFin = models.DateField()

    estadoProyecto = (
        ('Iniciado', 'Iniciado'),
        ('Finaliza', 'Finalizado'),
        ('Pospuesto', 'Pospuesto'),
    )

    estado = models.CharField(max_length=10, choices=estadoProyecto, blank=True, default='Iniciado', help_text='Estado del proyecto')

    def __str__(self):
        """
        Cadena que representa a la instancia particular del modelo (p. ej. en el sitio de Administración)
        """
        return self.nombre

    def get_absolute_url(self):
        
        # Devuelve el URL a una instancia particular del Proyecto
        
        return reverse('proyecto_detail', args=[str(self.idBacklog)])


class Rol(models.Model):

    idRol = models.AutoField(primary_key=True, help_text="ID único para este Rol")
    rol = models.CharField(max_length=50,
                           help_text="Ingrese el nombre del Rol")

    def __str__(self):
        """
        Cadena que representa a la instancia particular del modelo (p. ej. en el sitio de Administración)
        """
        return self.rol


class UsuarioProyecto (models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE)
    rol = models.ForeignKey(Rol, on_delete=models.CASCADE)


class Sprint(models.Model):

    # Modelo que representa un Sprint.
    nombre = models.CharField(max_length=100)
    idSprintBacklog = models.AutoField(primary_key=True, help_text="ID único para este Sprint")
    idBacklog = models.ForeignKey(Proyecto, on_delete=models.CASCADE)
    fechaInicio = models.DateField()
    fechaFin = models.DateField()

    @property
    def duration(self):
        return (self.fechaInicio - self.fechaFin) // timedelta(weeks=2)

    def __str__(self):
      
        # String que representa al objeto Sprint
        
        return self.nombre

    def get_absolute_url(self):
        
        # Devuelve el URL a una instancia particular de Sprint
        
        return reverse('sprint_detail', args=[str(self.idSprintBacklog)])


class UserStory(models.Model):
    idUserStory = models.AutoField(max_length=10, primary_key=True)
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE)
    storyPoints = models.IntegerField(editable=True, default=0)
    hecho = models.CharField(max_length=100)
    prioridadTarea = (
        ('Mayor', 'Mayor'),
        ('Media', 'Media'),
        ('Menor', 'Menor'),
    )
    prioridad = models.CharField(max_length=10, choices=prioridadTarea,
                                 blank=True, default='2', help_text='Prioridad de la tarea')
    estadoUS = (('To do', 'To do'),
                ('Doing', 'Doing'),
                ('Done', 'Done'),
                ('Cancelled', 'Cancelled'),)
    estado = models.CharField(max_length=10, choices=estadoUS, blank=True, 
                              default='I', help_text='Estado de la tarea')
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks_assigned')
    fechaInicio = models.DateField()
    fechaFin = models.DateField()

    def __str__(self):
        return self.nombre
    
    def get_absolute_url(self):
        
        # Devuelve el URL a una instancia particular del UserStory
        
        return reverse('userstory_detail', args=[str(self.idUserStory)])


class SprintBacklog (models.Model):
    sprint = models.ForeignKey(Sprint, on_delete=models.CASCADE)
    userstory = models.ForeignKey(UserStory, on_delete=models.CASCADE)
