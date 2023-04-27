from django.contrib import admin

# Register your models here.

from .models import Proyecto, Sprint, UserStory, Rol


# Register the admin class with the associated model
# admin.site.register(Proyecto)
# admin.site.register(Sprint)
# admin.site.register(UserStory)


# Define the admin class
class ProyectoAdmin(admin.ModelAdmin):
    pass


# Register the Admin classes for Proyecto using the decorator
admin.site.register(Proyecto, ProyectoAdmin)


@admin.register(Sprint)
class SprintAdmin(admin.ModelAdmin):
    pass


@admin.register(UserStory)
class UserStoryAdmin(admin.ModelAdmin):
    list_display = ('idUserStory', 'nombre', 'usuario', 'estado','proyecto')
    pass


@admin.register(Rol)
class RolAdmin(admin.ModelAdmin):
    pass
