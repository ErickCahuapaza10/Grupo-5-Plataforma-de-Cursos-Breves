from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profesor, Curso, Inscripcion, Material,PerfilUsuario

class RegistroForm(UserCreationForm):
    rol = forms.ChoiceField(choices=PerfilUsuario.ROL_CHOICES, label="Tipo de usuario")
    email = forms.EmailField(required=True)
    
    class Meta:
        model = User
        fields = ['username', 'email','password1', 'password2', 'rol','first_name','last_name']
        
class ProfesorForm(forms.ModelForm):
    class Meta:
        model = Profesor
        fields = ['nombre', 'apellido']

class CursoForm(forms.ModelForm):
    class Meta:
        model = Curso
        fields = ['nom_curso', 'capacidad', 'id_profesor']

class InscripcionForm(forms.ModelForm):
    class Meta:
        model = Inscripcion
        fields = ['id_curso'] 

class MaterialForm(forms.ModelForm):
    class Meta:
        model = Material
        fields = ['nom_material', 'descripcion', 'archivo', 'id_curso', 'id_profesor']
