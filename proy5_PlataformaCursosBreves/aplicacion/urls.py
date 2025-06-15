from django.urls import path
from . import views

urlpatterns = [
    path('lista_cursos/', views.lista_cursos, name='lista_cursos'),
    path('detalle_curso/<int:pk>/', views.detalle_curso, name='detalle_curso'),
    path('crear_curso/', views.crear_curso, name='crear_curso'),
    path('editar_curso/<int:pk>/editar/', views.editar_curso, name='editar_curso'),
    path('eliminar_curso/<int:pk>/eliminar/', views.eliminar_curso, name='eliminar_curso'),
    path('editar_material/<int:pk>/comentar/', views.editar_material, name='editar_material'),
    path("subir_material/<int:curso_id>/", views.subir_material, name="subir_material"),
    path('inscribirse_curso/<int:curso_id>/', views.inscribirse_curso, name='inscribirse_curso'),
    path('salirse_curso/<int:curso_id>/', views.salirse_curso, name='salirse_curso'),
    path('curso/<int:curso_id>/estudiantes/', views.lista_estudiantes_curso, name='lista_estudiantes'),
    path('', views.home, name='home'),
    path('salir/', views.salir, name='salir'),
    path('registrar/', views.registrar, name='registrar'),
    path('cursos_inscritos/', views.cursos_inscritos, name='cursos_inscritos'),
    path('material/<int:material_id>/entregar/', views.entregar_tarea, name='entregar_tarea'),
    path('cursos_creados/', views.cursos_creados, name='cursos_creados'),
    path('entrega/<int:entrega_id>/anular/', views.anular_entrega, name='anular_entrega'),
    path('curso/<int:curso_id>/entregas/', views.lista_entregas, name='lista_entregas'),
]
