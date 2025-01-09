from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Tareas(models.Model):
    title = models.CharField(max_length=200)
    descrpcion = models.TextField(blank=True)
    creacion = models.DateTimeField(auto_now_add=True)
    fecha_termino = models.DateField(null=True)
    importante = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.title + ' - by ' + self.user.username 
 

class Ubicaciones(models.Model):
    ubicacion = models.CharField(max_length=100)
    empresa = models.CharField(max_length=10)
    codigo_sucursal = models.CharField(max_length=10,null=True)
    telefono = models.CharField(max_length=10,null=True)
    extension = models.CharField(max_length=10,null=True)
    nombre_tiular = models.CharField(max_length=50,null=True)
    ap_paterno = models.CharField(max_length=50,null=True)
    email = models.CharField(max_length=100,null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    direccion = models.CharField(max_length=200)
    tipo_cedis = models.CharField(max_length=10,null=True)
    coordenadas =models.CharField(max_length=50,null=True)
    latitud = models.CharField(max_length=15,null=True)
    longitud = models.CharField(max_length=15,null=True)
    def __str__(self):
        return self.ubicacion + ' - ' + self.nombre_tiular

class VacanteAct(models.Model):
    vacante = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    departamento = models.CharField(max_length=100,null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_termino = models.DateField(null=True)
    estatus = models.BooleanField(default=False)
    sueldo = models.CharField(max_length=100,null=True)
    respon = models.TextField(blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    departamento = models.CharField(max_length=100)
    def __str__(self):
        return self.vacante + ' - ' + self.departamento
    
class Empresas(models.Model):
    empresa = models.CharField(max_length=50)
    def __str__(self):
        return self.empresa

class VacanteActivas(models.Model):
    vacante = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    departamento = models.CharField(max_length=100,null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_termino = models.DateField(null=True)
    estatus = models.BooleanField(default=False)
    sueldo = models.CharField(max_length=100,null=True)
    respon = models.TextField(blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    departamento = models.CharField(max_length=100)
    empresa = models.ForeignKey(Empresas, default=1, on_delete=models.CASCADE)
    def __str__(self):
        return self.vacante + ' - ' + self.departamento

class Vacantes(models.Model):    #NO SIRVE
    vacante = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_termino = models.DateField(null=True)
    estatus = models.BooleanField(default=False)
    sueldo = models.CharField(max_length=100,null=True)
    respon = models.TextField(blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    departamento = models.TextField(blank=True)
    empresa = models.ForeignKey(Empresas, default=1, on_delete=models.CASCADE)
    def __str__(self):
        return self.vacante 
class Cursos(models.Model):
    curso = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    imagen = models.CharField(max_length=100)
    empresa_curso = models.CharField(max_length=50)
    archivo  =models.FileField(upload_to='filesPDF/Cursos/')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        return self.curso + ' - ' + self.empresa_curso
    
class SolicitudEmpleo(models.Model):
    puesto = models.CharField(max_length=100)
    nombres = models.CharField(max_length=80)
    ap_paterno = models.CharField(max_length=80)
    ap_materno = models.CharField(max_length=80)
    escolaridad = models.CharField(max_length=80)
    correo = models.CharField(max_length=100)
    numero = models.CharField(max_length=15)
    likedin = models.CharField(max_length=255)
    experiencia = models.TextField(blank=True)
    curriculum =models.FileField(upload_to='filesPDF/CV/')
    fecha_solicitud = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.nombres + ' - ' + self.puesto
    
class Departamentos(models.Model):
    departamento =models.CharField(max_length=100)
    def __str__(self):
        return self.departamento 
class Puestos(models.Model):
    puesto =models.CharField((""), max_length=100)
    def __str__(self):
        return self.puesto
class UsuariosGA(models.Model):
    nombres = models.CharField(max_length=80)
    ap_paterno = models.CharField(max_length=80)
    ap_materno = models.CharField(max_length=80)
    empresa = models.ForeignKey(Empresas, on_delete=models.CASCADE)
    sucursal = models.CharField(max_length=80)
    departamento = models.ForeignKey(Departamentos, on_delete=models.CASCADE)
    puesto = models.ForeignKey(Puestos, on_delete=models.CASCADE)
    correo = models.CharField(max_length=100)
    extension = models.CharField(max_length=5)
    fecha_nacimiento= models.DateField(null=True)
    fecha_ingreso = models.DateField(null=True)
    rfc =models.CharField(max_length=13)
    numero_empleado = models.BigIntegerField(default=0)
    foto =models.ImageField(upload_to='FotosPlantilla/')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        return self.nombres + ' - ' + self.ap_paterno
    

class TipoNoticia(models.Model):
    tipo_noticia = models.CharField((""), max_length=20)
    def __str__(self):
        return self.tipo_noticia
    
class Noticias(models.Model):
    titulo =models.CharField(max_length=50)
    imagen =models.ImageField(upload_to='FotosNoticia/')
    descripcion = models.TextField(blank=True)
    fecha_noticia = models.DateField(null=True)
    fecha_ingreso = models.DateTimeField(auto_now_add=True)
    tipo_noticia = models.ForeignKey(TipoNoticia, on_delete=models.CASCADE)
    empresa = models.ForeignKey(Empresas, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        return self.titulo 


class TipoEquipos(models.Model):
    tipo_equipo = models.CharField(max_length=50)
    def __str__(self):
        return self.tipo_equipo
class SistemaOperativo(models.Model):
    sistemaOperativo = models.CharField(max_length=50)
    def __str__(self):
        return self.sistemaOperativo
class DominiosRed(models.Model):
    dominio = models.CharField(max_length=50)
    def __str__(self):
        return self.dominio

class MarcaEquipos(models.Model):
    marca = models.CharField(max_length=50)
    def __str__(self):
        return self.marca
class MarcaEquiposMouse(models.Model):
    marca = models.CharField(max_length=50)
    def __str__(self):
        return self.marca
class MarcaEquiposMonitor(models.Model):
    marca = models.CharField(max_length=50)
    def __str__(self):
        return self.marca
class MarcaEquiposTeclado(models.Model):
    marca = models.CharField(max_length=50)
    def __str__(self):
        return self.marca

class MemoriasRam(models.Model):
    memoria = models.CharField(max_length=50)
    def __str__(self):
        return self.memoria
class TipoDiscoC(models.Model):
    disco = models.CharField(max_length=50)
    capacidad = models.CharField(max_length=20)
    def __str__(self):
        return self.disco +'-'+self.capacidad
class TipoDiscoD(models.Model):
    disco = models.CharField(max_length=50)
    capacidad = models.CharField(max_length=20)
    def __str__(self):
        return self.disco +'-'+self.capacidad

class VersionesOffice(models.Model):
    office = models.CharField(max_length=50)
    def __str__(self):
        return self.office

class InventarioSoporte(models.Model):
    equipo =models.CharField(max_length=100)
    area = models.ForeignKey(Departamentos, on_delete=models.CASCADE)
    puesto=models.ForeignKey(Puestos,  on_delete=models.CASCADE)
    usuario =models.ForeignKey(UsuariosGA, on_delete=models.CASCADE)
    tipo_equipo = models.ForeignKey(TipoEquipos, on_delete=models.CASCADE)
    hostname = models.CharField(max_length=50)
    dominio = models.ForeignKey(DominiosRed,on_delete=models.CASCADE)
    sufijo_DNS = models.CharField(max_length=20)
    marca = models.ForeignKey(MarcaEquipos, on_delete=models.CASCADE)
    modelo=models.CharField(max_length=50)
    num_Serie_Equipo= models.CharField(max_length=50)
    teclado = models.ForeignKey(MarcaEquiposTeclado, on_delete=models.CASCADE)
    mouse = models.ForeignKey(MarcaEquiposMouse, on_delete=models.CASCADE)
    monitor = models.ForeignKey(MarcaEquiposMonitor, on_delete=models.CASCADE)
    modelo_monitor = models.CharField(max_length=50)
    monitor_serie = models.CharField(max_length=50)
    procesador = models.CharField(max_length=100)
    memoria = models.ForeignKey(MemoriasRam, on_delete=models.CASCADE)
    tipo_disco_C = models.ForeignKey(TipoDiscoC, on_delete=models.CASCADE)
    tipo_disco_D = models.ForeignKey(TipoDiscoD, on_delete=models.CASCADE)
    particion = models.BooleanField(default=False)
    adaptador_USB_RJ45 = models.BooleanField(default=False)
    mac_Ethernet = models.CharField(max_length=100)
    mac_WIFI = models.CharField(max_length=100)
    ip_activa= models.CharField(max_length=50)
    nombre_usuario_pc= models.CharField(max_length=50)
    sistema_operativo =models.ForeignKey(SistemaOperativo, on_delete=models.CASCADE)
    version_office = models.ForeignKey(VersionesOffice, on_delete=models.CASCADE)
    antivirus = models.BooleanField(default=False)
    pdf  = models.BooleanField(default=False)
    sygnology = models.BooleanField(default=False)
    anydesk = models.BooleanField(default=False)
    one_drive = models.BooleanField(default=False)
    mba3 = models.BooleanField(default=False)
    netsuite = models.BooleanField(default=False)
    bizagi = models.BooleanField(default=False)
    tsplus = models.BooleanField(default=False)
    impresora_b_n = models.BooleanField(default=False)
    impresora_color = models.BooleanField(default=False)
    responsiva =models.FileField(upload_to='filesPDF/Responsivas_Soporte/')

class TipoDocumento(models.Model):
    tipo_documento = models.CharField((""), max_length=20)
    def __str__(self):
        return self.tipo_documento
    
class Procesos(models.Model):
    titulo = models.CharField(max_length=50)
    descripcion = models.TextField(blank=True)
    documento =models.FileField(upload_to='filesPDF/ISO/')
    departamento = models.ForeignKey(Departamentos, on_delete=models.CASCADE)
    empresa = models.ForeignKey(Empresas, on_delete=models.CASCADE)
    tipo_documento = models.ForeignKey(TipoDocumento, on_delete=models.CASCADE)
    def __str__(self):
        return self.titulo
    
class Promociones(models.Model):
    nombre = models.CharField((""), max_length=20)
    imagen = models.FileField(upload_to='Promociones/')
    descripcion = models.TextField(blank=True)
    precio = models.DecimalField(max_digits = 10,decimal_places = 2)
    cantidad = models.IntegerField(default=0)
    empresa = models.ForeignKey(Empresas, on_delete=models.CASCADE, default=1)
    inactiva = models.BooleanField(default=False)
    fecha_promo = models.DateField(null=True)
    def __str__(self):
        return self.nombre
    
class BoletinMensual(models.Model):
        mes_boletin = models.CharField(max_length=50)
        empresa = models.ForeignKey(Empresas, on_delete=models.CASCADE, default=1)
        boletin = models.FileField(upload_to='Boletins/')
        fecha_carga = models.DateTimeField(auto_now_add=True)
        fecha_boletin= models.DateField(null=True)
        nombre_planta = models.CharField(max_length=50)
        def __str__(self):
            return self.mes_boletin + '-' +self.nombre_planta
        