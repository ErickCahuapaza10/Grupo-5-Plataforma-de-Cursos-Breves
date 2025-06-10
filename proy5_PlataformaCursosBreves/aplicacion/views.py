from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout,login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.utils import timezone
from .forms import CursoForm,InscripcionForm,MaterialForm,RegistroForm
from .models import Material,Inscripcion,Curso,PerfilUsuario,Profesor
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from .models import Curso, Inscripcion

def home(request):
    return render(request, 'aplicacion/home.html')

def salir(request):
    logout(request)
    return redirect('home')

def registrar(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            usuario = form.save()
            rol = form.cleaned_data['rol']
            PerfilUsuario.objects.create(usuario=usuario, rol=rol)
            if rol == 'maestro':
                # aquí habrías de pedir nombre/apellido en el form, 
                # o usar el username como ambos:
                Profesor.objects.create(
                    nombre=usuario.username,
                    apellido='',
                    autor=usuario
                )
            login(request, usuario)
            return redirect('lista_cursos')
    else:
        form = RegistroForm()
    return render(request, 'registration/registrar.html', {'form': form})
@login_required
def crear_curso(request):
    try:
        profesor = Profesor.objects.get(autor=request.user)
    except Profesor.DoesNotExist:
        return HttpResponseForbidden("Solo los profesores pueden crear cursos.")
    if request.method == 'POST':
        form = CursoForm(request.POST)
        if form.is_valid():
            curso = form.save(commit=False)
            curso.id_profesor = profesor 
            curso.save()
            return redirect('lista_cursos')
    else:
        form = CursoForm()

    return render(request, 'aplicacion/crear_curso.html', {'form': form})

def lista_cursos(request):
    cursos = Curso.objects.all()
    return render(request,'aplicacion/lista_cursos.html', {'cursos':cursos})


def cursos_inscritos(request):
    inscripciones = Inscripcion.objects.filter(autor=request.user).select_related('id_curso')
    cursos = [i.id_curso for i in inscripciones]
    return render(request, 'aplicacion/cursos_inscritos.html', {'cursos': cursos})

@login_required
def detalle_curso(request, pk):
    curso       = get_object_or_404(Curso, pk=pk)
    materiales  = Material.objects.filter(id_curso=curso)
    is_profesor = (request.user.perfilusuario.rol == 'maestro')
    is_inscrito = Inscripcion.objects.filter(autor=request.user, id_curso=curso).exists()
    return render(request, 'aplicacion/detalle_curso.html', {
        'curso': curso,
        'materiales': materiales,
        'is_profesor': is_profesor,
        'is_inscrito': is_inscrito,
    })

def eliminar_curso(request, pk):
    curso = get_object_or_404(Curso, pk=pk)
    if curso.id_profesor.autor != request.user:
        return HttpResponseForbidden("No tienes permiso para eliminar este curso.")
    if request.method == 'POST':
        curso.delete()
        return redirect('lista_cursos')
    return render(request, 'aplicacion/confirmar_eliminacion.html', {'curso': curso})

def editar_material(request, pk):
    material = get_object_or_404(Material, pk=pk)
    if material.id_profesor.autor != request.user:
        return HttpResponseForbidden("No puedes editar este material.")
    if request.method == 'POST':
        form = MaterialForm(request.POST, request.FILES, instance=material)
        if form.is_valid():
            form.save()
            return redirect('detalle_curso', pk=material.id_curso.pk)
    else:
        form = MaterialForm(instance=material)
    return render(request, 'aplicacion/editar_material.html', {'form': form})

def subir_material(request, curso_id):
    curso = get_object_or_404(Curso, pk=curso_id)
    if request.method == 'POST':
        form = MaterialForm(request.POST, request.FILES)
        if form.is_valid():
            mat = form.save(commit=False)
            mat.id_curso = curso
            mat.id_profesor = get_object_or_404(Profesor, autor=request.user)
            mat.save()
            return redirect('detalle_curso', curso.pk)
    else:
        form = MaterialForm()
    return render(request, 'aplicacion/subir_material.html', {
        'form': form,
        'curso': curso
    })
def salirse_curso(request, curso_id):
    inscripcion = get_object_or_404(Inscripcion, autor=request.user, id_curso_id=curso_id)
    if request.method == 'POST':
        inscripcion.delete()
        return redirect('lista_cursos')  # o donde quieras redirigir después
    return render(request, 'aplicacion/confirmar_salida.html', {'curso': inscripcion.id_curso})



@login_required
def inscribirse_curso(request, curso_id):
    curso = get_object_or_404(Curso, pk=curso_id)
    
    if not Inscripcion.objects.filter(autor=request.user, id_curso=curso).exists():
        Inscripcion.objects.create(autor=request.user, id_curso=curso)
    return redirect('detalle_curso', pk=curso.pk)

def editar_curso(request, pk):
    curso = get_object_or_404(Curso, pk = pk)
    if(curso.id_profesor.autor != request.user):
        return HttpResponseForbidden("No tiene permiso para editar el curso.")
    
    if(request.method == 'POST'):
        form = CursoForm(request.POST, instance=curso)
        if(form.is_valid()):
            form.save()
            return redirect('detalle_curso', pk=curso.pk)
        
    else:
        form = CursoForm(instance=curso)
    return render(request, 'aplicacion/editar_curso.html', {'form': form})
@login_required
def lista_estudiantes_curso(request, curso_id):
    curso = get_object_or_404(Curso, pk=curso_id)

    # Solo el profesor que creó el curso puede ver la lista
    if curso.id_profesor.autor != request.user:
        return HttpResponseForbidden("No tienes permiso para ver los inscritos de este curso.")

    estudiantes = (
        Inscripcion.objects
        .filter(id_curso=curso)
        .select_related('autor')
        .order_by('autor__username')
    )
    return render(request, 'aplicacion/lista_estudiantes.html', {
        'curso': curso,
        'estudiantes': estudiantes,
    })
