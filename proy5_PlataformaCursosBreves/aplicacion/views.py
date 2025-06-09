from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout,login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.utils import timezone
from .forms import CursoForm,InscripcionForm,MaterialForm,RegistroForm
from .models import Material,Inscripcion,Curso,PerfilUsuario,Profesor

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
            # Crear el perfil con el rol
            PerfilUsuario.objects.create(usuario=usuario, rol=rol)
            login(request, usuario)
            return redirect('lista_cursos')
    else:
        form = RegistroForm()
    return render(request, 'registration/registrar.html', {'form': form})

@login_required
def crear_curso(request):
    if request.method == 'POST':
        form = CursoForm(request.POST)
        if form.is_valid():
            curso = form.save(commit=False)
            profesor = Profesor.objects.filter(autor=request.user).first()
            if not profesor:
                return HttpResponseForbidden("Debes ser profesor para crear cursos.")
            curso.id_profesor = profesor
            curso.save()
            return redirect('lista_cursos')
    else:
        form = CursoForm()
    return render(request, 'aplicacion/crear_curso.html', {'form': form})

def lista_cursos(request):
    cursos = Curso.objects.all()
    return render(request,'aplicacion/lista_cursos.html', {'cursos':cursos})

def detalle_curso(request, pk):
    curso = get_object_or_404(Curso,pk=pk)
    materiales = Material.objects.filter(curso = curso)
    form_Material = MaterialForm() if request.user.is_authenticated else None
    contexto ={
        'curso':curso,
        'material':materiales,
        'form_material':form_Material,
    }
    return render(request, 'aplicacion/detalle_curso.html',contexto)

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

def subir_material(request):
    if request.method == 'POST':
        form = MaterialForm(request.POST, request.FILES)
        if form.is_valid():
            material = form.save(commit=False)
            material.fecha_subida = timezone.now()
            material.save()
            return redirect('detalle_curso')
    else:
        form = MaterialForm()
    return render(request, 'aplicacion/subir_material.html', {'form': form})

def salirse_curso(request, curso_id):
    inscripcion = get_object_or_404(Inscripcion, autor=request.user, id_curso_id=curso_id)
    if request.method == 'POST':
        inscripcion.delete()
        return redirect('lista_cursos')  # o donde quieras redirigir después
    return render(request, 'aplicacion/confirmar_salida.html', {'curso': inscripcion.id_curso})

def inscribirse_curso(request):
    if request.method == 'POST':
        form = InscripcionForm(request.POST)
        if form.is_valid():
            inscripcion = form.save(commit=False)
            inscripcion.autor = request.user 
            inscripcion.save()
            return redirect('lista_cursos') 
    else:
        form = InscripcionForm()
    return render(request, 'aplicacion/inscripcion.html', {'form': form})

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

