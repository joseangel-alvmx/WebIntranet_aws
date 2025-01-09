from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404, JsonResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User 
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from .forms import TaskForm, VacantesAForm,UbicacionesForm,SolicitudEmpleoForm,ProcesosForm
from .models import Tareas, VacanteActivas,Cursos,InventarioSoporte,Ubicaciones,Noticias, UsuariosGA,Procesos, Empresas,TipoDocumento,Departamentos,Promociones,BoletinMensual
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import date ,timedelta
from django.db.models.functions import ExtractMonth, ExtractDay
from django.core.mail import send_mail, EmailMessage
from django.conf import settings
from django.shortcuts import get_object_or_404, redirect
from django.db.models import Q

# Create your views here.

def Index(request):
    #return HttpResponse("<h1>Hola Mundo</h1>") #Para linea directa de djnago
    return render(request, "index.html",{
    }) 

@login_required
def createTarea(request):
    if request.method == 'GET':
        return render(request, "Create_task.html",{
            'form': TaskForm
        }) 
    else:
        try:
            form = TaskForm(request.POST)
            new_task =form.save(commit=False)
            new_task.user=request.user
            new_task.save()
            return redirect('tareas')
        except ValueError:
            return render(request, "Create_task.html",{
                'form': TaskForm,
                'error': 'Checar datos ingresados'
            }) 
            
def bolsa_trabajo(request):
    if request.method == 'GET':
        return render(request, "Solicitud_empleo.html", {
            'form': SolicitudEmpleoForm()
        })
    else:
        try:
            # Pasar tanto request.POST como request.FILES al formulario
            form = SolicitudEmpleoForm(request.POST, request.FILES)

            if form.is_valid():  # Validar el formulario antes de guardar
                nueva_solicitud = form.save(commit=False)  # Crear objeto pero no guardar aún
                if 'curriculum' in request.FILES:
                    nueva_solicitud.curriculum = request.FILES['curriculum']  # Asignar archivo
                nueva_solicitud.save()  # Guardar objeto en la base de datos
                return redirect('about_us')  # Redireccionar tras éxito
            else:
                # Si el formulario no es válido, renderizar el formulario con errores
                return render(request, "Solicitud_empleo.html", {
                    'form': form,
                    'error': 'Datos ingresados no son válidos, por favor revisa.'
                })
        except ValueError:
            return render(request, "Solicitud_empleo.html", {
                'form': SolicitudEmpleoForm(),
                'error': 'Ocurrió un error inesperado. Verifica tus datos.'
            })
  
def signup(request):
    if request.method == 'GET':
           return render(request, 'signup.html',{
                'form' : UserCreationForm
            })
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                # Register User
                user = User.objects.create_user(username=request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request,user)
                return redirect('tareas')
            except IntegrityError:
                return render(request, 'signup.html',{
                    'form' : UserCreationForm,
                    'error' : 'Usuario ya existe'
                })
                
        else:
            return render(request, 'signup.html',{
                'form' : UserCreationForm,
                'error' : 'Password no coincide'
            })

@login_required
def tareas(request):
    tareas = Tareas.objects.all()
    return render(request,'tareas.html',{
        'tareas' : tareas
    })


def signout(request):
    logout(request)
    return redirect('index')

def signin(request):
    if request.method == 'GET':
        return render(request, 'signin.html',{
            'form': AuthenticationForm
        })
    else:
        user = authenticate(request,username=request.POST['username'], password=request.POST['password'])
        username = username=request.POST['username']
        if user is None:
           return render(request, 'signin.html',{
            'form': AuthenticationForm,
            'error': 'Username o Password es incorrecto'
            })
           
        else:
            domain = username.split('@')[1]
            login(request,user)              
            if domain == 'alvamex.com.mx' or domain == 'vastro.com.mx' or domain == 'imex.com.mx':
                return redirect('alvamex')
            elif domain == 'diamantepinturas.com.mx':
                return redirect('diamante')
            elif domain == 'tradepolymers.com.mx':
                return redirect('trade-polymers')
            elif domain == 'alvaenvases.com.mx':
                return redirect('alvaenvases')
            elif  domain == 'admin':
                return redirect('/admin/')
            else:
                return render(request, 'signin.html',{
                'form': AuthenticationForm,
                'error': 'Username o Password es incorrecto'
                })

            

            
def about_us(request):
    return render(request,'about_us.html',{
    })
            
            
@login_required       
def empresa(request):
    hoy=date.today()
    fecha_limite= hoy + timedelta(days=15)
    messages.success(request, f'¡Bienvenid@, {request.user.first_name} {request.user.last_name}!')
    principales = Noticias.objects.filter(tipo_noticia=1).select_related('user','tipo_noticia').order_by('-fecha_ingreso')[:4]
    secundarias = Noticias.objects.filter(tipo_noticia=2, empresa=1).select_related('user','tipo_noticia').order_by('-fecha_ingreso')[:4]
    relevantes = Noticias.objects.filter(tipo_noticia=3, empresa=1).select_related('user','tipo_noticia').order_by('-fecha_ingreso')[:6]
    anuncios = Noticias.objects.filter(tipo_noticia=4, empresa=1).select_related('user','tipo_noticia').order_by('-fecha_ingreso')[:1]
    nacs = UsuariosGA.objects.filter(empresa=1,fecha_nacimiento__month=hoy.month, fecha_nacimiento__day__gte=hoy.day).order_by('-fecha_nacimiento') | \
        UsuariosGA.objects.filter(empresa=1,fecha_nacimiento__month=fecha_limite.month, fecha_nacimiento__day__lte=fecha_limite.day)
    boletines = BoletinMensual.objects.filter(empresa=1).order_by('-fecha_boletin')[:2]
    print(f'hoy: {hoy} , limite: {fecha_limite}')
    if fecha_limite.month != hoy.month:
        acs = UsuariosGA.objects.annotate(
            mes_nacimiento=ExtractMonth('fecha_nacimiento'),
            dia_nacimiento=ExtractDay('fecha_nacimiento') 
        ).filter(
            empresa=1,
            mes_nacimiento=fecha_limite.month,
            dia_nacimiento__lte=fecha_limite.day
        ).order_by('fecha_nacimiento')
        nacs = nacs | acs
    print(nacs)
    
    anivs = UsuariosGA.objects.filter(empresa=1,fecha_ingreso__month=hoy.month, fecha_ingreso__day__gte=hoy.day).order_by('-fecha_ingreso') | \
        UsuariosGA.objects.filter(empresa=1,fecha_ingreso__month=fecha_limite.month, fecha_ingreso__day__lte=fecha_limite.day)
    if fecha_limite.month != hoy.month:
        anv = UsuariosGA.objects.annotate(
            mes_nacimiento=ExtractMonth('fecha_ingreso'),
            dia_nacimiento=ExtractDay('fecha_ingreso') 
        ).filter(
            empresa=1,
            mes_nacimiento=fecha_limite.month,
            dia_nacimiento__lte=fecha_limite.day
        ).order_by('fecha_ingreso')
        anivs = anivs | anv
    print(anivs)

    
    return render(request,'empresa.html',{
        'principales': principales,
        'secundarias': secundarias,
        'relevantes': relevantes,
        'anuncios': anuncios,
        'nacs': nacs,
        'anivs': anivs,
        'boletines': boletines
    })
    
     
@login_required   
def cedisJSON(request):
    lugares = list(Ubicaciones.objects.values('ubicacion','latitud','longitud','empresa','codigo_sucursal','telefono','extension','nombre_tiular','ap_paterno','email','direccion','tipo_cedis'))
    return JsonResponse(lugares, safe=False)
    
@login_required
def cedis(request):    
    return render(request,'mapa.html',{
    })

@login_required              
def promociones(request):
    vacantes = VacanteActivas.objects.filter(estatus=0,empresa=1).select_related('user')
    promociones = Promociones.objects.filter(empresa=1, inactiva=0).order_by('-fecha_promo')
    return render(request,'promo.html',{
        'vacantes' : vacantes ,
        'promociones' : promociones
    })
    
@login_required
def procesos(request):

    # Obtener todas las empresas, departamentos y tipos de documentos
    empresas = Empresas.objects.all()
    departamentos = Departamentos.objects.all()
    tipos_documento = TipoDocumento.objects.all()

    # Filtrar por los parámetros recibidos del GET
    empresa_id = request.GET.get('empresa')
    tipo_documento_id = request.GET.get('tipo_documento')
    departamento_id = request.GET.get('departamento')

    documentos = Procesos.objects.all()

    # Filtrar los documentos solo para las empresas 'Diamante' (empresa_id=2) y 'Grupo Alva' (empresa_id=1)
    documentos = documentos.filter(
        Q(empresa_id=1) | Q(empresa_id=5)
    )

    # Si se pasa un filtro específico de empresa por GET, se aplica
    if empresa_id:
        documentos = documentos.filter(empresa_id=empresa_id)

    # Filtrar por tipo de documento
    if tipo_documento_id:
        documentos = documentos.filter(tipo_documento_id=tipo_documento_id)

    # Filtrar por departamento
    if departamento_id:
        documentos = documentos.filter(departamento_id=departamento_id)

    # Renderizar la vista con los filtros aplicados
    return render(request, 'procesos.html', {
        'documentos': documentos,
        'empresas': empresas,
        'departamentos': departamentos,
        'tipos_documento': tipos_documento
    })
    
@login_required
def dintranet(request):
    hoy=date.today()
    fecha_limite= hoy + timedelta(days=15)
    messages.success(request, f'¡Bienvenid@, {request.user.first_name} {request.user.last_name}!')
    principales = Noticias.objects.filter(tipo_noticia=1).select_related('user','tipo_noticia').order_by('-fecha_ingreso')[:4]
    secundarias = Noticias.objects.filter(tipo_noticia=2, empresa=2).select_related('user','tipo_noticia').order_by('-fecha_ingreso')[:4]
    relevantes = Noticias.objects.filter(tipo_noticia=3, empresa=2).select_related('user','tipo_noticia').order_by('-fecha_ingreso')[:6]
    anuncios = Noticias.objects.filter(tipo_noticia=4, empresa=2).select_related('user','tipo_noticia').order_by('-fecha_ingreso')[:1]
    nacs = UsuariosGA.objects.filter(empresa=2,fecha_nacimiento__month=hoy.month, fecha_nacimiento__day__gte=hoy.day).order_by('-fecha_nacimiento') | \
        UsuariosGA.objects.filter(empresa=2,fecha_nacimiento__month=fecha_limite.month, fecha_nacimiento__day__lte=fecha_limite.day)
    boletines = BoletinMensual.objects.filter(empresa=2).order_by('-fecha_boletin')[:2]
    print(f'hoy: {hoy} , limite: {fecha_limite}')
    if fecha_limite.month != hoy.month:
        acs = UsuariosGA.objects.annotate(
            mes_nacimiento=ExtractMonth('fecha_nacimiento'),
            dia_nacimiento=ExtractDay('fecha_nacimiento') 
        ).filter(
            empresa=1,
            mes_nacimiento=fecha_limite.month,
            dia_nacimiento__lte=fecha_limite.day
        ).order_by('fecha_nacimiento')
        nacs = nacs | acs
    print(nacs)
    
    anivs = UsuariosGA.objects.filter(empresa=2,fecha_ingreso__month=hoy.month, fecha_ingreso__day__gte=hoy.day).order_by('-fecha_ingreso') | \
        UsuariosGA.objects.filter(empresa=2,fecha_ingreso__month=fecha_limite.month, fecha_ingreso__day__lte=fecha_limite.day)
    if fecha_limite.month != hoy.month:
        anv = UsuariosGA.objects.annotate(
            mes_nacimiento=ExtractMonth('fecha_ingreso'),
            dia_nacimiento=ExtractDay('fecha_ingreso') 
        ).filter(
            empresa=2,
            mes_nacimiento=fecha_limite.month,
            dia_nacimiento__lte=fecha_limite.day
        ).order_by('fecha_ingreso')
        anivs = anivs | anv

    
    return render(request,'dintranet.html',{
        'principales': principales,
        'secundarias': secundarias,
        'relevantes': relevantes,
        'anuncios': anuncios,
        'nacs': nacs,
        'anivs': anivs,
        'boletines': boletines
    })
    
@login_required
def duniversidad(request):
    cursos = Cursos.objects.all().select_related('user')
    return render(request,'duniversidad.html',{
        'cursos' : cursos,
    })
    
@login_required
def dcedis(request):
    return render(request,'dcedis.html',{
    })
    
@login_required
def dprocesos(request):
    # Obtener todas las empresas, departamentos y tipos de documentos
    empresas = Empresas.objects.all()
    departamentos = Departamentos.objects.all()
    tipos_documento = TipoDocumento.objects.all()

    # Filtrar por los parámetros recibidos del GET
    empresa_id = request.GET.get('empresa')
    tipo_documento_id = request.GET.get('tipo_documento')
    departamento_id = request.GET.get('departamento')

    documentos = Procesos.objects.all()

    # Filtrar los documentos solo para las empresas 'Diamante' (empresa_id=2) y 'Grupo Alva' (empresa_id=1)
    documentos = documentos.filter(
        Q(empresa_id=2) | Q(empresa_id=5)
    )

    # Si se pasa un filtro específico de empresa por GET, se aplica
    if empresa_id:
        documentos = documentos.filter(empresa_id=empresa_id)

    # Filtrar por tipo de documento
    if tipo_documento_id:
        documentos = documentos.filter(tipo_documento_id=tipo_documento_id)

    # Filtrar por departamento
    if departamento_id:
        documentos = documentos.filter(departamento_id=departamento_id)

    # Renderizar la vista con los filtros aplicados
    return render(request, 'dprocesos.html', {
        'documentos': documentos,
        'empresas': empresas,
        'departamentos': departamentos,
        'tipos_documento': tipos_documento
    })  
    
@login_required    
def tradepolymers(request):
    hoy=date.today()
    fecha_limite= hoy + timedelta(days=30)
    messages.success(request, f'¡Bienvenid@, {request.user.first_name} {request.user.last_name}!')
    principales = Noticias.objects.filter(tipo_noticia=1).select_related('user','tipo_noticia').order_by('-fecha_ingreso')[:4]
    secundarias = Noticias.objects.filter(tipo_noticia=2, empresa=4).select_related('user','tipo_noticia').order_by('-fecha_ingreso')[:4]
    relevantes = Noticias.objects.filter(tipo_noticia=3, empresa=4).select_related('user','tipo_noticia').order_by('-fecha_ingreso')[:6]
    anuncios = Noticias.objects.filter(tipo_noticia=4, empresa=4).select_related('user','tipo_noticia').order_by('-fecha_ingreso')[:1]
    nacs = UsuariosGA.objects.filter(empresa=4,fecha_nacimiento__month=hoy.month, fecha_nacimiento__day__gte=hoy.day).order_by('-fecha_nacimiento') | \
        UsuariosGA.objects.filter(empresa=4,fecha_nacimiento__month=fecha_limite.month, fecha_nacimiento__day__lte=fecha_limite.day)
    boletines = BoletinMensual.objects.filter(empresa=4).order_by('-fecha_boletin')[:2]
    print(f'hoy: {hoy} , limite: {fecha_limite}')
    if fecha_limite.month != hoy.month:
        acs = UsuariosGA.objects.annotate(
            mes_nacimiento=ExtractMonth('fecha_nacimiento'),
            dia_nacimiento=ExtractDay('fecha_nacimiento') 
        ).filter(
            empresa=1,
            mes_nacimiento=fecha_limite.month,
            dia_nacimiento__lte=fecha_limite.day
        ).order_by('fecha_nacimiento')
        nacs = nacs | acs
    print(nacs)
    
    anivs = UsuariosGA.objects.filter(empresa=4,fecha_ingreso__month=hoy.month, fecha_ingreso__day__gte=hoy.day).order_by('-fecha_ingreso') | \
        UsuariosGA.objects.filter(empresa=4,fecha_ingreso__month=fecha_limite.month, fecha_ingreso__day__lte=fecha_limite.day)
    if fecha_limite.month != hoy.month:
        anv = UsuariosGA.objects.annotate(
            mes_nacimiento=ExtractMonth('fecha_ingreso'),
            dia_nacimiento=ExtractDay('fecha_ingreso') 
        ).filter(
            empresa=4,
            mes_nacimiento=fecha_limite.month,
            dia_nacimiento__lte=fecha_limite.day
        ).order_by('fecha_ingreso')
        anivs = anivs | anv

    
    return render(request,'trade_polymers.html',{
        'principales': principales,
        'secundarias': secundarias,
        'relevantes': relevantes,
        'anuncios': anuncios,
        'nacs': nacs,
        'anivs': anivs,
        'boletines': boletines,
    })

@login_required     
def VacantesActivas(request):
    if request.method == 'GET':
        return render(request, "Crear_Proms.html",{
            'form': VacantesAForm
        }) 
    else:
        try:
            form = VacantesAForm(request.POST)
            new_task =form.save(commit=False)
            new_task.user=request.user
            new_task.save()
            return redirect('promociones')
        except ValueError:
            return render(request, "Crear_proms.html",{
                'form': VacantesAForm,
                'error': 'Checar datos ingresados'
            })  
            
@login_required     
def ubicacionesCedis(request):
    if request.method == 'GET':
        return render(request, "NuevaUbicacion.html",{
            'form': UbicacionesForm
        }) 
    else:
        try:
            form = UbicacionesForm(request.POST)
            new_ubicacion =form.save(commit=False)
            new_ubicacion.user=request.user
            new_ubicacion.save()
            return redirect('cedis')
        except ValueError:
            return render(request, "NuevaUbicacion.html",{
                'form': UbicacionesForm,
                'error': 'Checar datos ingresados'
            })     

@login_required
def universidad(request):
    cursos = Cursos.objects.all()
    print(cursos)
    return render(request,'universidad.html',{
        'cursos' : cursos
    })
    
    
@login_required
def dprom(request):
    vacantes = VacanteActivas.objects.filter(estatus=0,empresa=2).select_related('user')
    promociones = Promociones.objects.filter(empresa=2, inactiva=0).order_by('-fecha_promo')
    return render(request,'dprom.html',{
        'vacantes' : vacantes,
        'promociones' : promociones 
    })


@login_required
def tprom(request):
        vacantes = VacanteActivas.objects.filter(estatus=0,empresa=4).select_related('user')
        promociones = Promociones.objects.filter(empresa=4, inactiva=0).order_by('-fecha_promo')
        return render(request,'tprom.html',{
            'vacantes' : vacantes,
            'promociones' : promociones
    })

@login_required
def tuniversidad(request):
    cursos = Cursos.objects.all().select_related('user')
    return render(request,'tuniversidad.html',{
        'cursos' : cursos,
    })
@login_required
def tcedis(request):
    return render(request,'tcedis.html',{
    })

@login_required
def tprocesos(request):
    # Obtener todas las empresas, departamentos y tipos de documentos
    empresas = Empresas.objects.all()
    departamentos = Departamentos.objects.all()
    tipos_documento = TipoDocumento.objects.all()

    # Filtrar por los parámetros recibidos del GET
    empresa_id = request.GET.get('empresa')
    tipo_documento_id = request.GET.get('tipo_documento')
    departamento_id = request.GET.get('departamento')

    documentos = Procesos.objects.all()

    # Filtrar los documentos solo para las empresas 'Diamante' (empresa_id=2) y 'Grupo Alva' (empresa_id=1)
    documentos = documentos.filter(
        Q(empresa_id=4) | Q(empresa_id=5)
    )

    # Si se pasa un filtro específico de empresa por GET, se aplica
    if empresa_id:
        documentos = documentos.filter(empresa_id=empresa_id)

    # Filtrar por tipo de documento
    if tipo_documento_id:
        documentos = documentos.filter(tipo_documento_id=tipo_documento_id)

    # Filtrar por departamento
    if departamento_id:
        documentos = documentos.filter(departamento_id=departamento_id)

    # Renderizar la vista con los filtros aplicados
    return render(request, 'tprocesos.html', {
        'documentos': documentos,
        'empresas': empresas,
        'departamentos': departamentos,
        'tipos_documento': tipos_documento
    })

    
    
@login_required    
def alvaenvases(request):
    hoy=date.today()
    fecha_limite= hoy + timedelta(days=15)
    messages.success(request, f'¡Bienvenid@, {request.user.first_name} {request.user.last_name}!')
    principales = Noticias.objects.filter(tipo_noticia=1).select_related('user','tipo_noticia').order_by('-fecha_ingreso')[:4]
    secundarias = Noticias.objects.filter(tipo_noticia=2, empresa=3).select_related('user','tipo_noticia').order_by('-fecha_ingreso')[:4]
    relevantes = Noticias.objects.filter(tipo_noticia=3, empresa=3).select_related('user','tipo_noticia').order_by('-fecha_ingreso')[:6]
    anuncios = Noticias.objects.filter(tipo_noticia=4, empresa=3).select_related('user','tipo_noticia').order_by('-fecha_ingreso')[:1]
    nacs = UsuariosGA.objects.filter(empresa=3,fecha_nacimiento__month=hoy.month, fecha_nacimiento__day__gte=hoy.day).order_by('-fecha_nacimiento') | \
        UsuariosGA.objects.filter(empresa=3,fecha_nacimiento__month=fecha_limite.month, fecha_nacimiento__day__lte=fecha_limite.day)
    boletines = BoletinMensual.objects.filter(empresa=3).order_by('-fecha_boletin')[:2]
    print(f'hoy: {hoy} , limite: {fecha_limite}')
    if fecha_limite.month != hoy.month:
        acs = UsuariosGA.objects.annotate(
            mes_nacimiento=ExtractMonth('fecha_nacimiento'),
            dia_nacimiento=ExtractDay('fecha_nacimiento') 
        ).filter(
            empresa=1,
            mes_nacimiento=fecha_limite.month,
            dia_nacimiento__lte=fecha_limite.day
        ).order_by('fecha_nacimiento')
        nacs = nacs | acs
    print(nacs)
    
    anivs = UsuariosGA.objects.filter(empresa=3,fecha_ingreso__month=hoy.month, fecha_ingreso__day__gte=hoy.day).order_by('-fecha_ingreso') | \
        UsuariosGA.objects.filter(empresa=3,fecha_ingreso__month=fecha_limite.month, fecha_ingreso__day__lte=fecha_limite.day)
    if fecha_limite.month != hoy.month:
        anv = UsuariosGA.objects.annotate(
            mes_nacimiento=ExtractMonth('fecha_ingreso'),
            dia_nacimiento=ExtractDay('fecha_ingreso') 
        ).filter(
            empresa=3,
            mes_nacimiento=fecha_limite.month,
            dia_nacimiento__lte=fecha_limite.day
        ).order_by('fecha_ingreso')
        anivs = anivs | anv

    
    return render(request,'alvaenvases.html',{
        'principales': principales,
        'secundarias': secundarias,
        'relevantes': relevantes,
        'anuncios': anuncios,
        'nacs': nacs,
        'anivs': anivs,
        'boletines': boletines
    })
    
    
@login_required
def aprom(request):
    vacantes = VacanteActivas.objects.filter(estatus=0,empresa=3).select_related('user')
    promociones = Promociones.objects.filter(empresa=3, inactiva=0).order_by('-fecha_promo')
    return render(request,'aprom.html',{
        'vacantes' : vacantes,
        'promociones' : promociones
    })
@login_required
def auniversidad(request):
    cursos = Cursos.objects.all().select_related('user')
    return render(request,'auniversidad.html',{
        'cursos' : cursos,
    })
@login_required
def acedis(request):
    return render(request,'acedis.html',{
    })
@login_required
def aprocesos(request):
    # Obtener todas las empresas, departamentos y tipos de documentos
    empresas = Empresas.objects.all()
    departamentos = Departamentos.objects.all()
    tipos_documento = TipoDocumento.objects.all()

    # Filtrar por los parámetros recibidos del GET
    empresa_id = request.GET.get('empresa')
    tipo_documento_id = request.GET.get('tipo_documento')
    departamento_id = request.GET.get('departamento')

    documentos = Procesos.objects.all()

    # Filtrar los documentos solo para las empresas 'Diamante' (empresa_id=2) y 'Grupo Alva' (empresa_id=1)
    documentos = documentos.filter(
        Q(empresa_id=3) | Q(empresa_id=5)
    )

    # Si se pasa un filtro específico de empresa por GET, se aplica
    if empresa_id:
        documentos = documentos.filter(empresa_id=empresa_id)

    # Filtrar por tipo de documento
    if tipo_documento_id:
        documentos = documentos.filter(tipo_documento_id=tipo_documento_id)

    # Filtrar por departamento
    if departamento_id:
        documentos = documentos.filter(departamento_id=departamento_id)

    # Renderizar la vista con los filtros aplicados
    return render(request, 'aprocesos.html', {
        'documentos': documentos,
        'empresas': empresas,
        'departamentos': departamentos,
        'tipos_documento': tipos_documento
    }) 
    
@login_required
def inventarios(request):
    inventarios = InventarioSoporte.objects.all()
    return render(request,'inventario.html',{
       'inventarios' : inventarios
    })


@login_required
def bizagi(request):
    return render(request, 'bizagi.html',{
        
    })

@login_required
def dbizagi(request):
    return render(request, 'dbizagi.html',{
        
    })

@login_required
def tbizagi(request):
    return render(request, 'tbizagi.html',{
        
    })
    
@login_required
def abizagi(request):
    return render(request, 'abizagi.html',{
        
    })

@login_required
def bizagi(request):
    return render(request, 'bizagi.html',{
        
    })

@login_required
def dbizagi(request):
    return render(request, 'dbizagi.html',{
        
    })

@login_required
def tbizagi(request):
    return render(request, 'tbizagi.html',{
        
    })
    
@login_required
def abizagi(request):
    return render(request, 'abizagi.html',{
        
    })
def buzoncomite(request):
    if request.method == 'POST':
        usuario=request.user
        nombre = request.POST.get('name', 'Anónimo')
        mensaje = request.POST.get('message')
        destinatario = 'cynthya.ramirez@alvamex.com.mx'
        

        asunto = f"Mensaje del Buzón de Ética - {nombre}"
        mensaje_correo = f"""
        <p Comite de Etica</p>
        <blockquote style="font-style: italic; color: #555;">{nombre}</blockquote>
        <blockquote style="font-style: italic; color: #555;">{mensaje}</blockquote>
        <p>Gracias por su atencion</p>
        <p>Saludos</p>
        """

        try:
            email = EmailMessage(asunto, mensaje_correo, to=[destinatario])
            email.content_subtype = "html"  # Esto asegura que se envíe como HTML
            email.send()
            domain = usuario.username.split('@')[1]             
            if domain == 'alvamex.com.mx' or domain == 'vastro.com.mx' or domain == 'imex.com.mx':
                return redirect('alvamex')
            elif domain == 'diamantepinturas.com.mx':
                return redirect('diamante')
            elif domain == 'tradepolymers.com.mx':
                return redirect('trade-polymers')
            elif domain == 'alvaenvases.com.mx':
                return redirect('alvaenvases')
            elif  domain == 'admin':
                return redirect('alvamex')
        except Exception as e:
            domain = usuario.username.split('@')[1]             
            if domain == 'alvamex.com.mx' or domain == 'vastro.com.mx' or domain == 'imex.com.mx':
                return redirect(request,'alvamex',{
                'error':'Error al enviar intente nuevamente'
            })
            elif domain == 'diamantepinturas.com.mx':
                return redirect(request,'diamante',{
                'error':'Error al enviar intente nuevamente'
            })
            elif domain == 'tradepolymers.com.mx':
                return redirect(request,'trade-polymers',{
                'error':'Error al enviar intente nuevamente'
            })
            elif domain == 'alvaenvases.com.mx':
                return redirect(request,'alvaenvases',{
                'error':'Error al enviar intente nuevamente'
            })
            elif  domain == 'admin':
                return redirect(request,'alvamex',{
                'error':'Error al enviar intente nuevamente'
            })

def enviar_felicitacion(request):
    if request.method == 'POST':

        usuario = request.user 
        mensaje = request.POST.get('mensaje')
        destinatario = request.POST.get('recipientEmail')
        nombre = request.POST.get('recipientName')


        asunto = f"¡Feliz Cumpleaños, {nombre}!"
        mensaje_correo = f"""
            <p>Querido/a </p>
            <blockquote style="font-style: italic; color: #555;">{nombre}</blockquote>
            <blockquote style="font-style: italic; color: #555;">{mensaje}</blockquote>
            <p>Gracias por compartir tu talento un año mas</p>
            <p>Enviado por:</p>
            <ul>
                <li><strong>Nombre:</strong> {usuario.first_name} {usuario.last_name}</li>
            </ul>
            <p>Saludos,<br> {usuario.username}</p>
            """
        try:
            email = EmailMessage(asunto, mensaje_correo, to=[destinatario])
            email.content_subtype = "html"  # Esto asegura que se envíe como HTML
            email.send()
            domain = usuario.username.split('@')[1]             
            if domain == 'alvamex.com.mx' or domain == 'vastro.com.mx' or domain == 'imex.com.mx':
                return redirect('alvamex')
            elif domain == 'diamantepinturas.com.mx':
                return redirect('diamante')
            elif domain == 'tradepolymers.com.mx':
                return redirect('trade-polymers')
            elif domain == 'alvaenvases.com.mx':
                return redirect('alvaenvases')
            elif  domain == 'admin':
                return redirect('alvamex')
        except Exception as e:
            domain = usuario.username.split('@')[1]             
            if domain == 'alvamex.com.mx' or domain == 'vastro.com.mx' or domain == 'imex.com.mx':
                return redirect(request,'alvamex',{
                'error':'Error al enviar intente nuevamente'
            })
            elif domain == 'diamantepinturas.com.mx':
                return redirect(request,'diamante',{
                'error':'Error al enviar intente nuevamente'
            })
            elif domain == 'tradepolymers.com.mx':
                return redirect(request,'trade-polymers',{
                'error':'Error al enviar intente nuevamente'
            })
            elif domain == 'alvaenvases.com.mx':
                return redirect(request,'alvaenvases',{
                'error':'Error al enviar intente nuevamente'
            })
            elif  domain == 'admin':
                return redirect(request,'alvamex',{
                'error':'Error al enviar intente nuevamente'
            })

def aniversario(request):
    if request.method == 'POST':

        usuario = request.user 
        mensaje = request.POST.get('mensaje')
        destinatario = request.POST.get('recipientEmail')
        nombre = request.POST.get('recipientName')


        asunto = f"¡Feliz Aniversario, {nombre}!"
        mensaje_correo = f"""
            <p>Querido/a </p>
            <blockquote style="font-style: italic; color: #555;">{nombre}</blockquote>
            <blockquote style="font-style: italic; color: #555;">{mensaje}</blockquote>
            <p>Gracias por compartir tu talento un año mas</p>
            <p>Enviado por:</p>
            <ul>
                <li><strong>Nombre:</strong> {usuario.first_name} {usuario.last_name}</li>
            </ul>
            <p>Saludos,<br> {usuario.username}</p>
            """
        try:
            email = EmailMessage(asunto, mensaje_correo, to=[destinatario])
            email.content_subtype = "html"  # Esto asegura que se envíe como HTML
            email.send()
            domain = usuario.username.split('@')[1]             
            if domain == 'alvamex.com.mx' or domain == 'vastro.com.mx' or domain == 'imex.com.mx':
                return redirect('alvamex')
            elif domain == 'diamantepinturas.com.mx':
                return redirect('diamante')
            elif domain == 'tradepolymers.com.mx':
                return redirect('trade-polymers')
            elif domain == 'alvaenvases.com.mx':
                return redirect('alvaenvases')
            elif  domain == 'admin':
                return redirect('alvamex')
        except Exception as e:
            domain = usuario.username.split('@')[1]             
            if domain == 'alvamex.com.mx' or domain == 'vastro.com.mx' or domain == 'imex.com.mx':
                return redirect(request,'alvamex',{
                'error':'Error al enviar intente nuevamente'
            })
            elif domain == 'diamantepinturas.com.mx':
                return redirect(request,'diamante',{
                'error':'Error al enviar intente nuevamente'
            })
            elif domain == 'tradepolymers.com.mx':
                return redirect(request,'trade-polymers',{
                'error':'Error al enviar intente nuevamente'
            })
            elif domain == 'alvaenvases.com.mx':
                return redirect(request,'alvaenvases',{
                'error':'Error al enviar intente nuevamente'
            })
            elif  domain == 'admin':
                return redirect(request,'alvamex',{
                'error':'Error al enviar intente nuevamente'
            })
def enviar_notificacion(request):
    if request.method == 'POST':
        usuario = request.user 
        consulta = request.POST.get('consulta')
        asunto = "Consulta de Noticias Pasadas"
        mensaje = f"""
            <p>Se ha recibido una solicitud de búsqueda de la noticia:</p>
            <blockquote style="font-style: italic; color: #555;">{consulta}</blockquote>
            <p>Detalles del usuario:</p>
            <ul>
                <li><strong>Nombre:</strong> {usuario.first_name} {usuario.last_name}</li>
                <li><strong>Correo Electrónico:</strong> {usuario.username}</li>
            </ul>
            <p>Saludos,<br>Equipo de Intranet</p>
        """
        destinatario = "intranet@alvamex.com.mx"
        
        # Crear el objeto de correo y especificar que el contenido es HTML
        domain = usuario.username.split('@')[1]  

        try:
            email = EmailMessage(asunto, mensaje, to=[destinatario])
            email.content_subtype = "html"  # Esto asegura que se envíe como HTML
            email.send()
           
            if domain == 'alvamex.com.mx' or domain == 'vastro.com.mx' or domain == 'imex.com.mx':
                return redirect('alvamex')
            elif domain == 'diamantepinturas.com.mx':
                return redirect('diamante')
            elif domain == 'tradepolymers.com.mx':
                return redirect('trade-polymers')
            elif domain == 'alvaenvases.com.mx':
                return redirect('alvaenvases')
            elif  domain == 'admin':
                return redirect('alvamex')
        except Exception as e:
         
            if domain == 'alvamex.com.mx' or domain == 'vastro.com.mx' or domain == 'imex.com.mx':
                return redirect(request,'alvamex',{
                'error':'Error al enviar intente nuevamente'
            })
            elif domain == 'diamantepinturas.com.mx':
                return redirect(request,'diamante',{
                'error':'Error al enviar intente nuevamente'
            })
            elif domain == 'tradepolymers.com.mx':
                return redirect(request,'trade-polymers',{
                'error':'Error al enviar intente nuevamente'
            })
            elif domain == 'alvaenvases.com.mx':
                return redirect(request,'alvaenvases',{
                'error':'Error al enviar intente nuevamente'
            })
            elif  domain == 'admin':
                return redirect(request,'alvamex',{
                'error':'Error al enviar intente nuevamente'
            })
def enviar_promocion(request):
    if request.method == 'POST':
        usuario = request.user 
        promocion_id =int(request.POST.get('promocion_id'))
        promocion_name =request.POST.get('promocion_name')
        promocion_precio =request.POST.get('promocion_precio')
        
        print(f'{promocion_id}')
        promocion = Promociones.objects.filter(id=promocion_id)
        print(promocion)
        cantidad = request.POST.get('cantidad')
        asunto = "Consulta de Noticias Pasadas"
        mensaje = f"""
                
                Se ha solicitado la promoción: {promocion_name}
                <br>Cantidad solicitada: {cantidad}
                <br>Precio por unidad: ${promocion_precio}
                <br><strong>Total: ${float(cantidad) * float(promocion_precio)}</strong>
                <li><strong>Nombre:</strong> {usuario.first_name} {usuario.last_name}</li>
                <li><strong>Correo Electrónico:</strong> {usuario.username}</li>
            </ul>
            <p>Saludos,<br>Equipo de Intranet</p>
        """
        destinatario = "intranet@alvamex.com.mx"
        
        # Crear el objeto de correo y especificar que el contenido es HTML
        domain = usuario.username.split('@')[1]  

        try:
            #promocion = Promociones.objects.get(id=promocion_id)
            email = EmailMessage(asunto, mensaje, to=[destinatario])
            email.content_subtype = "html"  # Esto asegura que se envíe como HTML
            email.send()
           
            if domain == 'alvamex.com.mx' or domain == 'vastro.com.mx' or domain == 'imex.com.mx':
                return redirect('alvamex')
            elif domain == 'diamantepinturas.com.mx':
                return redirect('diamante')
            elif domain == 'tradepolymers.com.mx':
                return redirect('trade-polymers')
            elif domain == 'alvaenvases.com.mx':
                return redirect('alvaenvases')
            elif  domain == 'admin':
                return redirect('alvamex')
        except Exception as e:
         
            if domain == 'alvamex.com.mx' or domain == 'vastro.com.mx' or domain == 'imex.com.mx':
                return redirect(request,'alvamex',{
                'error':'Error al enviar intente nuevamente'
            })
            elif domain == 'diamantepinturas.com.mx':
                return redirect(request,'diamante',{
                'error':'Error al enviar intente nuevamente'
            })
            elif domain == 'tradepolymers.com.mx':
                return redirect(request,'trade-polymers',{
                'error':'Error al enviar intente nuevamente'
            })
            elif domain == 'alvaenvases.com.mx':
                return redirect(request,'alvaenvases',{
                'error':'Error al enviar intente nuevamente'
            })
            elif  domain == 'admin':
                return redirect(request,'alvamex',{
                'error':'Error al enviar intente nuevamente'
            })