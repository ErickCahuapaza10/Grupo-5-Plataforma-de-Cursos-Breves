from django.contrib import admin
from .models import Curso, Inscripcion, Material, PerfilUsuario, Profesor
# Register your models here.
admin.site.register(Curso)
admin.site.register(Inscripcion)
admin.site.register(Material)
admin.site.register(PerfilUsuario)
admin.site.register(Profesor)
