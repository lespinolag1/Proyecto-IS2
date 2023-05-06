from django.shortcuts import render
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect

from django.contrib.auth.models import User
from .models import Proyecto, Sprint, UserStory, UsuarioProyecto, SprintBacklog
from .forms import ProjectForm, UserStoryForm, SprintForm, UserForm

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
    user_form = UserForm()
    fields = ['username', 'email', 'password', 'first_name', 'last_name']
    success_url = reverse_lazy('users')


class UserUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = User
    fields = ['username', 'email', 'password', 'first_name', 'last_name']
    success_url = reverse_lazy('users')


class UserDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = User
    success_url = reverse_lazy('users')


class UserStoryListView(ListView):
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


class SprintListView(ListView):
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


class AsignarUserStory(LoginRequiredMixin, CreateView):
    model = SprintBacklog
    fields = ['userstory', 'sprint']
    template_name = 'asignar_historia.html'

    def get_success_url(self):
        return reverse_lazy('sprint_detail', args=[self.kwargs['pk']])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        userstory = get_object_or_404(UserStory, pk=self.kwargs['pk'])
        context['userstory'] = userstory
        return context

    def form_valid(self, form):
        sprint = get_object_or_404(Sprint, pk=self.kwargs['pk'])
        sprint_backlog = form.save(commit=False)
        sprint_backlog.sprint = sprint
        sprint_backlog.save()
        return super().form_valid(form)


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
