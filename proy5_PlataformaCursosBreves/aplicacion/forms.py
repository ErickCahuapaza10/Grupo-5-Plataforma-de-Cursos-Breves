from django import forms
from .models import Curso
from .models import Inscripcion
from .models import Profesor
from .models import Material

class CursoForm(forms.ModelForm):
    class Meta:
        model = Curso
        fields = ['titulo','contenido']
        
class InscripcionForm(forms.ModelForm):
    class Meta:
        model = Inscripcion
        fields = ['contenido']

class ProfesorForm(forms.ModelForm):
    class Meta:
        model = Profesor
        fields = ['contenido']
        
class MaterialForm(forms.ModelForm):
    class Meta:
        model = Material
        fields = ['contenido']
