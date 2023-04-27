#from django.conf.urls import re_path
from django.urls import re_path as url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^proyectos/$', views.ProjectListView.as_view(), name='proyectos'),
    url(r'^proyecto/(?P<pk>\d+)$', views.ProyectoDetailView.as_view(), name='proyecto_detail'),
    url(r'^proyecto/create/$', views.ProjectCreateView.as_view(), name='proyecto_create'),
    url(r'^proyecto/(?P<pk>[-\w]+)/agregar_usuario/$', views.AgregarUsuario.as_view(), name='agregar_usuario'),
    url(r'^proyecto/(?P<pk>[-\w]+)/update/$', views.ProjectUpdateView.as_view(), name='update_proyecto'),
    url(r'^proyecto/(?P<pk>[-\w]+)/delete/$', views.ProjectDeleteView.as_view(), name='delete_proyecto'),
    url(r'^users/$', views.UserListView.as_view(), name='users'),
    url(r'^user/(?P<pk>\d+)$', views.UserDetailView.as_view(), name='user_detail'),
    url(r'^user/create/$', views.UserCreateView.as_view(), name='user_create'),
    url(r'^user/(?P<pk>[-\w]+)/update/$', views.UserUpdateView.as_view(), name='update_user'),
    url(r'^user/(?P<pk>[-\w]+)/delete/$', views.UserDeleteView.as_view(), name='delete_user'),
    url(r'^userstorys/$', views.UserStoryListView.as_view(), name='user_story_list'),
    url(r'^userstory/(?P<pk>\d+)$', views.UserStoryDetailView.as_view(), name='userstory_detail'),
    url(r'^userstory/create/$', views.UserStoryCreateView.as_view(), name='create_story'),
    url(r'^userstory/(?P<pk>[-\w]+)/update/$', views.UserStoryUpdateView.as_view(), name='update_story'),
    url(r'^userstory/(?P<pk>[-\w]+)/delete/$', views.UserStoryDeleteView.as_view(), name='delete_story'),
    url(r'^sprints/$', views.SprintListView.as_view(), name='sprint_list'),
    url(r'^sprint/(?P<pk>\d+)$', views.SprintDetailView.as_view(), name='sprint_detail'),
    url(r'^sprint/create/$', views.SprintCreateView.as_view(), name='create_sprint'),
    url(r'^sprint/(?P<pk>[-\w]+)/update/$', views.SprintUpdateView.as_view(), name='update_sprint'),
    url(r'^sprint/(?P<pk>[-\w]+)/delete/$', views.SprintDeleteView.as_view(), name='delete_sprint'),
]
