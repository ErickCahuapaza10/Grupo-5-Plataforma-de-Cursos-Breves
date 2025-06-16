from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout,login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .forms import CursoForm,MaterialForm,RegistroForm,EntregaForm
from .models import Material,Inscripcion,Curso,PerfilUsuario,Profesor,Curso, Inscripcion,Entrega
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib import messages

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

@login_required
def lista_cursos(request):
    cursos = Curso.objects.all()
    return render(request,'aplicacion/lista_cursos.html', {'cursos':cursos})


def cursos_inscritos(request):
    inscripciones = Inscripcion.objects.filter(autor=request.user).select_related('id_curso')
    cursos = [i.id_curso for i in inscripciones]
    return render(request, 'aplicacion/cursos_inscritos.html', {'cursos': cursos})

@login_required
def detalle_curso(request, pk):
    curso = get_object_or_404(Curso, pk=pk)
    materiales = Material.objects.filter(id_curso=curso)
    profesor = curso.id_profesor
    is_profesor = (request.user.perfilusuario.rol == 'maestro')
    is_inscrito = Inscripcion.objects.filter(autor=request.user, id_curso=curso).exists()
    
    entregas_map = {}
    if not is_profesor and is_inscrito:
        qs = Entrega.objects.filter(estudiante=request.user, material__in=materiales)
        entregas_map = { e.material_id: e for e in qs }

    materiales_data = []
    now = timezone.now()
    for m in materiales:
        esta_vencido = False
        if m.requiere_entrega and m.fecha_limite:
            esta_vencido = now > m.fecha_limite
        
        material_info = {
            'material': m,
            'entrega': entregas_map.get(m.id),
            'esta_vencido': esta_vencido,
            'entregas': [],
            'estudiantes_sin_entregar': []
        }
    
        if is_profesor and m.requiere_entrega:
            entregas = Entrega.objects.filter(material=m).select_related('estudiante')
            material_info['entregas'] = entregas
            
            estudiantes_inscritos = [insc.autor for insc in Inscripcion.objects.filter(id_curso=curso).select_related('autor')]
            estudiantes_que_entregaron = [e.estudiante for e in entregas]
            estudiantes_sin_entregar = [est for est in estudiantes_inscritos if est not in estudiantes_que_entregaron]
            material_info['estudiantes_sin_entregar'] = estudiantes_sin_entregar
        
        materiales_data.append(material_info)
    
    
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
        return HttpResponseForbidden()
    if request.method == 'POST':
        curso.delete()
        messages.success(request, f'El curso "{curso.nom_curso}" fue eliminado.')
        return redirect('lista_cursos')
    return render(request, 'aplicacion/confirmar_eliminacion.html', {
        'curso': curso
    })


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
    if Inscripcion.objects.filter(autor=request.user, id_curso=curso).exists():
        messages.warning(request, "Ya estás inscrito en este curso.")
        return redirect('detalle_curso', pk=curso_id)
    total = Inscripcion.objects.filter(id_curso=curso).count()
    if total >= curso.capacidad:
        messages.error(request, "Lo sentimos, el curso ya está lleno.")
        return redirect('detalle_curso', pk=curso_id)
    if request.method == 'POST':
        Inscripcion.objects.create(autor=request.user, id_curso=curso)
        messages.success(request, "¡Te has inscrito correctamente!")
        return redirect('detalle_curso', pk=curso_id)
    return render(request, 'aplicacion/confirmar_inscripcion.html', {
        'curso': curso
    })


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


    inscripciones = (
        Inscripcion.objects
        .filter(id_curso=curso)
        .select_related('autor')
        .order_by('autor__username')
    )
    

    total_tareas = Material.objects.filter(id_curso=curso, requiere_entrega=True).count()
    
   
    estudiantes_data = []
    for inscripcion in inscripciones:
        estudiante = inscripcion.autor
        
        
        entregas_realizadas = Entrega.objects.filter(
            estudiante=estudiante,
            material__id_curso=curso,
            material__requiere_entrega=True
        ).count()
        
     
        if total_tareas > 0:
            porcentaje = round((entregas_realizadas / total_tareas) * 100)
        else:
            porcentaje = 0
        
        estudiantes_data.append({
            'inscripcion': inscripcion,
            'estudiante': estudiante,
            'entregas_realizadas': entregas_realizadas,
            'total_tareas': total_tareas,
            'porcentaje': porcentaje
        })
    
    return render(request, 'aplicacion/lista_estudiantes.html', {
        'curso': curso,
        'estudiantes_data': estudiantes_data,
        'total_tareas': total_tareas,
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

@login_required
def lista_entregas(request, curso_id):
    curso = get_object_or_404(Curso, pk=curso_id)
    
    
    if curso.id_profesor.autor != request.user:
        return HttpResponseForbidden("No tienes permiso para ver las entregas de este curso.")
    
    
    entregas = Entrega.objects.filter(
        material__id_curso=curso
    ).select_related('estudiante', 'material').order_by('-fecha_entrega')
    
    
    materiales_con_entrega = Material.objects.filter(
        id_curso=curso, 
        requiere_entrega=True
    )
    
    return render(request, 'aplicacion/lista_entregas.html', {
        'curso': curso,
        'entregas': entregas,
        'materiales_con_entrega': materiales_con_entrega,
    })