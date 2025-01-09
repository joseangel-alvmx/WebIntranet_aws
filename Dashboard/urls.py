from django.urls import path
from . import views

urlpatterns = [
    path('', views.Index, name="index"),
    path('about_us/', views.about_us, name="about_us"),
    path('tareas/create/', views.createTarea, name="create_task"),
    path('signup/', views.signup, name="singup"),
    path('tareas/', views.tareas, name="tareas"),
    path('logout/', views.signout, name="logout"),
    path('signin/', views.signin, name="signin"),
    path('alvamex/', views.empresa, name="alvamex"),
    path('cedis/', views.cedis, name="cedis"),
    path('api/lugares/', views.cedisJSON, name="cedisJSON"),
    path('cedis/nueva_Ubicacion/', views.ubicacionesCedis, name="nuevocedis"),
    path('promociones/', views.promociones, name="promociones"),
    path('promociones/SubirVacantes/', views.VacantesActivas, name="CrearPromociones"),
    path('procesos/', views.procesos, name="procesos"),
    path('diamante/dintranet/', views.dintranet, name="dintranet"),
    path('diamante/', views.dintranet, name="diamante"),
    path('diamante/duniversidad/', views.duniversidad, name="duniversidad"),
    path('diamante/dcedis/', views.dcedis, name="dcedis"),
    path('diamante/dprocesos/', views.dprocesos, name="dprocesos"),
    path('trade-polymers/', views.tradepolymers, name="trade-polymers"),
    path('universidad/', views.universidad, name="universidad"),
    path('diamante/dprom/', views.dprom, name="promo"),
    path('trade-polymers/tprom/', views.tprom, name="tprom"),
    path('trade-polymers/tuniversidad/', views.tuniversidad, name="tuniversidad"),
    path('trade-polymers/tcedis/', views.tcedis, name="tcedis"),
    path('trade-polymers/tprocesos/', views.tprocesos, name="tprocesos"),
    path('alvaenvases/', views.alvaenvases, name="alvaenvases"),
    path('alvaenvases/aprom/', views.aprom, name="aprom"),
    path('alvaenvases/auniversidad/', views.auniversidad, name="auniversidad"),
    path('alvaenvases/acedis/', views.acedis, name="acedis"),
    path('alvaenvases/aprocesos/', views.aprocesos, name="aprocesos"),
    path('about_us/bolsa_trabajo/',views.bolsa_trabajo, name="bolsa_de_trabajo"),
    path('inventarios/', views.inventarios, name="inventarios"),
    path('bizagi/', views.bizagi, name="bizagi"),
    path('diamante/duniversidad/dbizagi/', views.dbizagi, name="dbizagi"),
    path('alvaenvases/aprocesos/abizagi/', views.abizagi, name="abizagi"),
    path('trade-polymers/tprocesos/bizagi/', views.tbizagi, name="tbizagi"),
    path('buzoncomite/', views.buzoncomite, name='buzoncomite'),
    path('enviarfelicitacion/', views.enviar_felicitacion, name='enviar_felicitacion'),
    path('aniversario/', views.aniversario, name='aniversario'),
    path('enviar_notificacion/', views.enviar_notificacion, name='enviar_notificacion'),
    path('enviar-promocion/', views.enviar_promocion, name='enviar_promocion'),

]
 
 
 
 
 