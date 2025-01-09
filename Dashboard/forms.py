from django.forms import ModelForm
from django import forms
from .models import Tareas, VacanteActivas, Ubicaciones,SolicitudEmpleo,Noticias, UsuariosGA,Procesos,TipoNoticia,Empresas,Departamentos, TipoDocumento, Promociones

class TaskForm(ModelForm):
    class Meta:
        model = Tareas
        fields = ['title', 'descrpcion','importante']

class VacantesAForm(ModelForm):
    class Meta:
        model = VacanteActivas
        fields = ['vacante', 'descripcion','departamento', 'respon','sueldo' , 'estatus']
        
class UbicacionesForm(ModelForm):
    class Meta:
        model = Ubicaciones
        fields = ['ubicacion', 'empresa','codigo_sucursal','telefono','extension','nombre_tiular','ap_paterno','email','direccion','tipo_cedis','coordenadas']
        
class SolicitudEmpleoForm(ModelForm):
    
    class Meta:
        model = SolicitudEmpleo
        fields = ['puesto','nombres','ap_paterno','ap_materno','escolaridad','correo','numero','likedin','experiencia','curriculum']

class NoticiasForm(ModelForm):
    
    class Meta:
        model = Noticias
        fields = ['titulo','imagen','descripcion','fecha_noticia','tipo_noticia','empresa','user']



class ProcesosForm(forms.Form):
    tipo_documento = forms.ModelChoiceField(queryset=TipoDocumento.objects.all(), required=False, label="Tipo de Documento")
    departamento = forms.ModelChoiceField(queryset=Departamentos.objects.all(), required=False, label="Departamento")
    
    class Meta:
        model = Procesos
        fields = ['titulo','descripcion','documento','departamento','empresa','tipo_documento']


class UsuariosGAForm(ModelForm):
    
    class Meta:
        model = UsuariosGA
        fields = ['nombres','ap_paterno','ap_materno','empresa','sucursal','departamento','puesto','correo','extension','fecha_nacimiento','fecha_ingreso','rfc','numero_empleado','foto']
        
class TipoNoticiaForm(ModelForm):
    class Meta:
        model = TipoNoticia
        fields = ['tipo_noticia']

class PromocionesForm(ModelForm):
    class Meta:
        model = Promociones
        fields = ['nombre','imagen', 'descripcion','precio','cantidad']
