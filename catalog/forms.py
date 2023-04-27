from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from .models import Proyecto, UserStory, Sprint


class ProjectForm(forms.ModelForm):

    class Meta:
        model = Proyecto
        fields = ['nombre', 'descripcion', 'fechaInicio',
                  'fechaFin', 'estado']

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('fechaInicio…')
        end_date = cleaned_data.get('fechaFin')
       
        if start_date and end_date and end_date < start_date:
            raise ValidationError('La fecha fin debe ser luego de la fecha de inicio.')

        return cleaned_data


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'first_name', 'last_name']


class UserStoryForm(forms.ModelForm):
    class Meta:
        model = UserStory
        fields = ['nombre', 'descripcion', 'proyecto', 'storyPoints', 'hecho',
                  'prioridad', 'estado', 'usuario', 'fechaInicio', 'fechaFin']

    def clean_points(self):
        points = self.cleaned_data['storyPoints']
        if points <= 0:
            raise forms.ValidationError("Los puntos de historia deben ser mayor que cero.")
        return points


class SprintForm(forms.ModelForm):
    class Meta:
        model = Sprint
        fields = ['nombre', 'idBacklog', 'fechaInicio',
                  'fechaFin', 'idBacklog']

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        if start_date and end_date and end_date <= start_date:
            raise forms.ValidationError("End date must be after start date.")
        return cleaned_data
