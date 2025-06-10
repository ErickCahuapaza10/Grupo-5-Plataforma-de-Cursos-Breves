from django.db import models
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
# Create your models here.

class Profesor(models.Model):
    nombre = models.CharField(max_length=30)
    apellido = models.CharField(max_length=30)
    autor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='profesores')
    
    def __str__(self):
        return f"{self.nombre} {self.apellido}"
    
class PerfilUsuario(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    ROL_CHOICES = (
        ('normal', 'Estudiante'),
        ('maestro', 'Maestro'),
    )
    rol = models.CharField(max_length=10, choices=ROL_CHOICES, default='normal')

    def __str__(self):
        return f"{self.usuario.username} - {self.rol}"

class RegistroForm(UserCreationForm):
    rol = forms.ChoiceField(choices=PerfilUsuario.ROL_CHOICES, label="Tipo de usuario")

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'rol']
class Curso(models.Model):
    nom_curso = models.CharField(max_length=30)
    capacidad = models.IntegerField()
    id_profesor = models.ForeignKey(Profesor, on_delete=models.CASCADE, related_name='cursos')
    
    def __str__(self):
        return f"{self.nom_curso}"

class Inscripcion(models.Model):
    fecha = models.DateField(auto_now_add=True)
    autor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='inscripciones')
    id_curso = models.ForeignKey(Curso, on_delete=models.CASCADE, related_name='inscripciones')
    
    def __str__(self):
        return f"{self.autor} {self.id_curso} {self.fecha}"
    
class Material(models.Model):
    nom_material = models.CharField(max_length=30)
    descripcion = models.TextField()
    fecha_subida = models.DateField(auto_now_add=True)
    archivo = models.FileField(upload_to='materiales/', null=True, blank=True)
    id_curso = models.ForeignKey(Curso, on_delete=models.CASCADE, related_name='materiales')
    id_profesor = models.ForeignKey(Profesor, on_delete=models.CASCADE, related_name='materiales_subidos')
    
    def __str__(self):
        return f"{self.nom_material}"
    