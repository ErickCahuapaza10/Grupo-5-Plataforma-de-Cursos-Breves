from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout,login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .forms import CursoForm,MaterialForm,RegistroForm,EntregaForm
from .models import Material,Inscripcion,Curso,PerfilUsuario,Profesor,Curso, Inscripcion,Entrega
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.utils import timezone

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
                Profesor.objects.create(
                    nombre=usuario.username,
                    apellido=usuario.last_name,
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
    profesor = curso.id_profesor
    is_profesor = (request.user.perfilusuario.rol == 'maestro')
    is_inscrito = Inscripcion.objects.filter(autor=request.user, id_curso=curso).exists()
    
    entregas_map = {}
    if not is_profesor and is_inscrito:
        qs = Entrega.objects.filter(estudiante=request.user, material__in=materiales)
        entregas_map = { e.material_id: e for e in qs }

    # lista de dicts para el template, incluyendo si está vencido
    materiales_data = []
    now = timezone.now()
    for m in materiales:
        esta_vencido = False
        if m.requiere_entrega and m.fecha_limite:
            esta_vencido = now > m.fecha_limite
        materiales_data.append({
            'material': m,
            'entrega': entregas_map.get(m.id),
            'esta_vencido': esta_vencido,
        })
    
    return render(request, 'aplicacion/detalle_curso.html', {
        'curso': curso,
        'profesor': profesor,
        'is_profesor': is_profesor,
        'is_inscrito': is_inscrito,
        'materiales_data': materiales_data,
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
        return redirect('lista_cursos')  
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
@login_required
def entregar_tarea(request, material_id):
    material = get_object_or_404(Material, pk=material_id)

    if not Inscripcion.objects.filter(autor=request.user, id_curso=material.id_curso).exists():
        return HttpResponseForbidden("Debes estar inscrito para entregar tareas.")

    if material.requiere_entrega and material.fecha_limite and timezone.now() > material.fecha_limite:
        return HttpResponseForbidden("El plazo para entregar esta tarea ha vencido.")

    entrega_existente = Entrega.objects.filter(estudiante=request.user, material=material).first()
    allow_resubmit = request.GET.get('resubmit') == '1'
    if request.method == 'POST':
        form = EntregaForm(request.POST, request.FILES, instance=entrega_existente)
        if form.is_valid():
            entrega = form.save(commit=False)
            entrega.estudiante = request.user
            entrega.material = material
            entrega.save()
            return redirect('detalle_curso', pk=material.id_curso.pk)
    else:
        form = EntregaForm(instance=entrega_existente)

    return render(request, 'aplicacion/entregar_tarea.html', {
        'form': form,
        'material': material,
        'entrega_existente': entrega_existente,
        'allow_resubmit': allow_resubmit,
    })
    
@login_required
def cursos_creados(request):
    if request.user.perfilusuario.rol != 'maestro':
        return HttpResponseForbidden("Solo los profesores pueden acceder.")
    
    profesor = get_object_or_404(Profesor, autor=request.user)
    cursos = Curso.objects.filter(id_profesor=profesor)
    return render(request, 'aplicacion/cursos_creados.html', {'cursos': cursos})

@login_required
def anular_entrega(request, entrega_id):
    entrega = get_object_or_404(Entrega, pk=entrega_id)

    if entrega.estudiante != request.user:
        return HttpResponseForbidden("No tienes permiso para anular esta entrega.")

    curso_id = entrega.material.id_curso.pk
    entrega.delete()
    return redirect('detalle_curso', pk=curso_id)