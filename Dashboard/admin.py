from django.contrib import admin
from .models import Tareas, VacanteActivas, Ubicaciones,  Empresas, Cursos,SolicitudEmpleo,Puestos,Departamentos,UsuariosGA,Noticias,TipoNoticia,TipoEquipos,SistemaOperativo,DominiosRed,MarcaEquipos,MarcaEquiposMonitor,MarcaEquiposMouse,MarcaEquiposTeclado,MemoriasRam,TipoDiscoC,TipoDiscoD,VersionesOffice,InventarioSoporte,TipoDocumento,Procesos,Promociones,BoletinMensual
class TareaAdmin(admin.ModelAdmin):
    readonly_fields = ("creacion",)
    
    
admin.site.register(Tareas,TareaAdmin)


class UbicacionAdmin(admin.ModelAdmin):
    readonly_fields = ()
    
admin.site.register(Ubicaciones, UbicacionAdmin)


class VacanteActAdmin(admin.ModelAdmin):
    readonly_fields = ("fecha_creacion",)
    
admin.site.register(VacanteActivas, VacanteActAdmin)
class EmpresasAdmin(admin.ModelAdmin):
    readonly_fields = ()
    
admin.site.register(Empresas, EmpresasAdmin)

class CursosAdmin(admin.ModelAdmin):
    readonly_fields = ()
    
admin.site.register(Cursos, CursosAdmin)

class SolicitudEmpleosAdmin(admin.ModelAdmin):
    readonly_fields = ("fecha_solicitud",)
    
admin.site.register(SolicitudEmpleo, SolicitudEmpleosAdmin)

class PuestosAdmin(admin.ModelAdmin):
    readonly_fields = ()
    
admin.site.register(Puestos, PuestosAdmin)

class DepartamentosAdmin(admin.ModelAdmin):
    readonly_fields = ()
    
admin.site.register(Departamentos, DepartamentosAdmin)
class UsuariosGAAdmin(admin.ModelAdmin):
    readonly_fields = ()
    
admin.site.register(UsuariosGA, UsuariosGAAdmin)

class Tipo_NoticiaAdmin(admin.ModelAdmin):
    readonly_fields = ()
    
admin.site.register(TipoNoticia, Tipo_NoticiaAdmin)

class NoticiasAdmin(admin.ModelAdmin):
    readonly_fields = ()
    
admin.site.register(Noticias, NoticiasAdmin)

class TipoEquiposAdmin(admin.ModelAdmin):
    readonly_fields = ()
    
admin.site.register(TipoEquipos, TipoEquiposAdmin)

class SistemaOperativoAdmin(admin.ModelAdmin):
    readonly_fields = ()
    
admin.site.register(SistemaOperativo, SistemaOperativoAdmin)

class DominiosRedAdmin(admin.ModelAdmin):
    readonly_fields = ()
    
admin.site.register(DominiosRed, DominiosRedAdmin)

class MarcaEquiposAdmin(admin.ModelAdmin):
    readonly_fields = ()
    
admin.site.register(MarcaEquipos, MarcaEquiposAdmin)

class MarcaEquiposMouseAdmin(admin.ModelAdmin):
    readonly_fields = ()
    
admin.site.register(MarcaEquiposMouse, MarcaEquiposMouseAdmin)

class MarcaEquiposMonitorAdmin(admin.ModelAdmin):
    readonly_fields = ()
    
admin.site.register(MarcaEquiposMonitor, MarcaEquiposMonitorAdmin)

class MarcaEquiposTecladoAdmin(admin.ModelAdmin):
    readonly_fields = ()
    
admin.site.register(MarcaEquiposTeclado, MarcaEquiposTecladoAdmin)


class MemoriasRAMAdmin(admin.ModelAdmin):
    readonly_fields = ()
    
admin.site.register(MemoriasRam, MemoriasRAMAdmin)

class TipoDiscoCAdmin(admin.ModelAdmin):
    readonly_fields = ()
    
admin.site.register(TipoDiscoC, TipoDiscoCAdmin)
class TipoDiscoDAdmin(admin.ModelAdmin):
    readonly_fields = ()
    
admin.site.register(TipoDiscoD, TipoDiscoDAdmin)

class VersionesOfficeAdmin(admin.ModelAdmin):
    readonly_fields = ()
    
admin.site.register(VersionesOffice, VersionesOfficeAdmin)

class InventarioSoporteAdmin(admin.ModelAdmin):
    readonly_fields = ()
    
admin.site.register(InventarioSoporte, InventarioSoporteAdmin)

class TipoDocumentoAdmin(admin.ModelAdmin):
    readonly_fields = ()
    
admin.site.register(TipoDocumento, TipoDocumentoAdmin)

class ProcesosAdmin(admin.ModelAdmin):
    readonly_fields = ()
    
admin.site.register(Procesos, ProcesosAdmin)

class PromocionesAdmin(admin.ModelAdmin):
    readonly_fields = ()
    
admin.site.register(Promociones, PromocionesAdmin)

class BoletinMensualAdmin(admin.ModelAdmin):
    readonly_fields = ()
    
admin.site.register(BoletinMensual, BoletinMensualAdmin)
