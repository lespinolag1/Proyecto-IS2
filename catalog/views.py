from django.shortcuts import render
from django.views import generic
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
import json
from django.db.models import Count
from datetime import timedelta
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate
from django.http import HttpResponseRedirect
from django.db.models import Q
from django.views.generic.edit import FormView


from django.contrib.auth.models import User
from .models import Proyecto, Sprint, UserStory, UsuarioProyecto, SprintBacklog
from .forms import ProjectForm, UserStoryForm, SprintForm, UserForm, AsignarUserStoryForm

# Create your views here.


class ProjectListView(LoginRequiredMixin,  generic.ListView):
    model = Proyecto
    queryset = Proyecto.objects.all()


class ProyectoDetailView(LoginRequiredMixin, generic.DetailView):
    model = Proyecto
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        proyecto = context['object']
        usuarios_proyecto = UsuarioProyecto.objects.filter(proyecto=proyecto)
        context['usuarios_proyecto'] = usuarios_proyecto
        return context


class ProjectCreateView(LoginRequiredMixin, CreateView):
    model = Proyecto
    form_class = ProjectForm


class AgregarUsuario(LoginRequiredMixin, CreateView):
    model = UsuarioProyecto
    fields = ['user', 'rol']
    template_name = 'agregar_usuario.html'

    def get_success_url(self):
        return reverse_lazy('proyecto_detail', args=[self.kwargs['pk']])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        proyecto = get_object_or_404(Proyecto, pk=self.kwargs['pk'])
        context['proyecto'] = proyecto
        return context

    def form_valid(self, form):
        proyecto = get_object_or_404(Proyecto, pk=self.kwargs['pk'])
        usuario_proyecto = form.save(commit=False)
        usuario_proyecto.proyecto = proyecto
        usuario_proyecto.save()
        return super().form_valid(form)


class ProjectUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Proyecto
    fields = ['nombre', 'descripcion', 'fechaInicio', 'fechaFin', 'estado']
    success_url = reverse_lazy('proyectos')


class ProjectDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Proyecto
    success_url = reverse_lazy('proyectos')


class UserListView(LoginRequiredMixin,  generic.ListView):
    model = User
    queryset = User.objects.all()


class UserDetailView(LoginRequiredMixin, generic.DetailView):
    model = User
    paginate_by = 10


class UserCreateView(LoginRequiredMixin, CreateView):
    model = User
    fields = ['username', 'email', 'password', 'first_name', 'last_name']
    success_url = reverse_lazy('users')

    def form_valid(self, form):
        # Antes de guardar el formulario, procesamos la contraseña
        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password'])
        user.save()
        return super().form_valid(form)


class UserUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = User
    fields = ['username', 'email', 'password', 'first_name', 'last_name']
    success_url = reverse_lazy('users')


class UserDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = User
    success_url = reverse_lazy('users')


class UserStoryListView(LoginRequiredMixin, ListView):
    model = UserStory
    queryset = UserStory.objects.all()


class UserStoryDetailView(LoginRequiredMixin, generic.DetailView):
    model = UserStory
    paginate_by = 10


class UserStoryCreateView(LoginRequiredMixin, generic.CreateView):
    model = UserStory
    form_class = UserStoryForm
    success_url = reverse_lazy('user_story_list')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class UserStoryUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = UserStory
    form_class = UserStoryForm
    success_url = reverse_lazy('user_story_list')


class UserStoryDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = UserStory
    success_url = reverse_lazy('user_story_list')


class SprintListView(LoginRequiredMixin, ListView):
    model = Sprint
    context_object_name = 'sprint_list'


class SprintDetailView(LoginRequiredMixin, generic.DetailView):
    model = Sprint
    paginate_by = 10


class SprintCreateView(LoginRequiredMixin, generic.CreateView):
    model = Sprint
    form_class = SprintForm
    success_url = reverse_lazy('sprint_list')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class SprintUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Sprint
    form_class = SprintForm
    success_url = reverse_lazy('sprint_list')


class SprintDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Sprint
    success_url = reverse_lazy('sprint_list')


class AsignarUserStory(FormView):
    form_class = AsignarUserStoryForm
    template_name = 'asignar_historia.html'

    def get_success_url(self):
        return reverse_lazy('sprint_detail', args=[self.kwargs['pk']])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        sprint = get_object_or_404(Sprint, pk=self.kwargs['pk'])
        context['sprint'] = sprint
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        sprint = get_object_or_404(Sprint, pk=self.kwargs['pk'])
        kwargs['sprint'] = sprint
        return kwargs

    def form_valid(self, form):
        sprint = get_object_or_404(Sprint, pk=self.kwargs['pk'])
        userstory = form.cleaned_data['userstory']

        # Verificar si el User Story ya está asignado a otro Sprint
        try:
            sprintbacklog = SprintBacklog.objects.get(userstory=userstory)
            # Eliminar la asignación anterior del User Story
            sprintbacklog.delete()
        except SprintBacklog.DoesNotExist:
            pass

        # Crear un nuevo SprintBacklog para asignar el User Story al Sprint actual
        SprintBacklog.objects.create(sprint=sprint, userstory=userstory)

        return super().form_valid(form)


@login_required
def kanban_board(request):
    # Obtener todos los user stories
    user_stories = UserStory.objects.exclude(estado='Cancelled')

    # Filtrar user stories por estado
    todo = user_stories.filter(estado='To do')
    doing = user_stories.filter(estado='Doing')
    done = user_stories.filter(estado='Done')

    context = {
        'todo': todo,
        'doing': doing,
        'done': done
    }

    return render(request, 'kanban_board.html', context)


@login_required
def burndown_chart(request):
    # Obtener los parámetros del proyecto/sprint para filtrar
    proyecto_id = request.GET.get('proyecto_id')
    sprint_id = request.GET.get('sprint_id')

    # Filtrar los User Stories realizados (estado 'Done') para el proyecto/sprint especificado
    user_stories = UserStory.objects.filter(estado='Done',
                                            proyecto_id=proyecto_id,
                                            sprintbacklog__sprint_id=sprint_id)

    # Ordenar los User Stories por fecha de finalización
    user_stories = user_stories.order_by('fechaFin')

    # Obtener la fecha de inicio y fin del sprint
    sprint = Sprint.objects.get(idSprintBacklog=sprint_id)
    fecha_inicio = sprint.fechaInicio
    fecha_fin = sprint.fechaFin

    # Calcular la duración total del sprint en días
    duracion_sprint = (fecha_fin - fecha_inicio).days + 1

    # Obtener la cantidad de User Stories realizados por día
    user_stories_realizados = user_stories.filter(fechaFin__gte=fecha_inicio).values('fechaFin').annotate(total=Count('idUserStory'))

    # Crear listas para almacenar los datos del Burndown Chart
    fechas = []
    us_realizadas = []
    dias_sprint = []
    us_restantes = []

    # Calcular los valores para el Burndown Chart
    fecha_actual = fecha_inicio
    user_stories_restantes = user_stories.count()
    for _ in range(duracion_sprint):
        fechas.append(fecha_actual.strftime('%Y-%m-%d'))
        us_realizadas_dia = sum([item['total'] for item in user_stories_realizados if item['fechaFin'] == fecha_actual])
        us_realizadas.append(us_realizadas_dia)
        dias_sprint.append((fecha_actual - fecha_inicio).days + 1)
        us_restantes.append(user_stories_restantes)
        user_stories_restantes -= us_realizadas_dia
        fecha_actual += timedelta(days=1)

    # Crear un diccionario con los datos del Burndown Chart
    data = {
        'fechas': fechas,
        'us_realizadas': us_realizadas,
        'dias_sprint': dias_sprint,
        'us_restantes': us_restantes,
    }

    # Convertir el diccionario a una cadena JSON
    json_data = json.dumps(data)

    # Renderizar el template del Burndown Chart y pasar los datos JSON al contexto
    return render(request, 'burndown_chart.html', {'chart_data': json_data})


def index(request):
    """
    Función vista para la página inicio del sitio.
    """
    # Genera contadores de algunos de los objetos principales
    num_proyectos = Proyecto.objects.all().count()
    num_storys = UserStory.objects.all().count()
    num_proyectos_iniciados = Proyecto.objects.filter(estado__exact='iniciado').count()

    # Numero de visitas a esta view, como está contado
    # en la variable de sesión.
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    # Renderiza la plantilla HTML index.html con
    # los datos en la variable contexto
    context = {
        'num_proyectos': num_proyectos,
        'num_storys': num_storys,
        'num_proyectos_iniciados': num_proyectos_iniciados,
        'num_visits': num_visits,
    }

    return render(request, 'index.html', context=context)
