from django.urls import path
from . import views

urlpatterns = [
    path('lista_cursos/', views.lista_cursos, name='lista_cursos'),
    path('detalle_curso/<int:pk>/', views.detalle_curso, name='detalle_curso'),
    path('crear_curso/', views.crear_curso, name='crear_curso'),
    path('editar_curso/<int:pk>/editar/', views.editar_curso, name='editar_curso'),
    path('eliminar_curso/<int:pk>/eliminar/', views.eliminar_curso, name='eliminar_curso'),
    path("editar_material/<int:pk>/comentar/", views.editar_material, name="editar_material"),
    path("subir_material/", views.subir_material, name="subir_material"),
    path('inscribirse_curso/<int:curso_id>/', views.inscribirse_curso, name='inscribirse_curso'),
    path('salirse_curso/<int:curso_id>/', views.salirse_curso, name='salirse_curso'),
    path('', views.home, name='home'),
    path('salir/', views.salir, name='salir'),
    path('registrar/', views.registrar, name='registrar'),
]
