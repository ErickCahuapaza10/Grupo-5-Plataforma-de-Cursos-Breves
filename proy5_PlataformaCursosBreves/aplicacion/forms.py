from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profesor, Curso, Inscripcion, Material,PerfilUsuario,Entrega

class RegistroForm(UserCreationForm):
    rol = forms.ChoiceField(choices=PerfilUsuario.ROL_CHOICES, label="Tipo de usuario")
    last_name = forms.CharField(label='Apellido', max_length=30, required=True)
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'last_name', 'email','password1', 'password2', 'rol','first_name','last_name']
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'rol']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'  
class ProfesorForm(forms.ModelForm):
    class Meta:
        model = Profesor
        fields = ['nombre', 'apellido']

class CursoForm(forms.ModelForm):
    class Meta:
        model = Curso
        fields = ['nom_curso', 'capacidad'] 

class InscripcionForm(forms.ModelForm):
    class Meta:
        model = Inscripcion
        fields = ['id_curso'] 

class MaterialForm(forms.ModelForm):
    class Meta:
        model = Material
        fields = ['nom_material', 'descripcion', 'archivo', 'requiere_entrega', 'fecha_limite']
        widgets = {'fecha_limite': forms.DateTimeInput(attrs={'type': 'datetime-local'}),}


class EntregaForm(forms.ModelForm):
    class Meta:
        model = Entrega
        fields = ['archivo']
