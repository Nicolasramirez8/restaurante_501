from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),

    # Clientes
    path('clientes/', views.clientes_lista, name='clientes_lista'),
    path('clientes/nuevo/', views.clientes_crear, name='clientes_crear'),
    path('clientes/editar/<int:pk>/', views.clientes_editar, name='clientes_editar'),
    path('clientes/eliminar/<int:pk>/', views.clientes_eliminar, name='clientes_eliminar'),

    # Platos
    path('platos/', views.platos_lista, name='platos_lista'),
    path('platos/nuevo/', views.platos_crear, name='platos_crear'),
    path('platos/editar/<int:pk>/', views.platos_editar, name='platos_editar'),
    path('platos/eliminar/<int:pk>/', views.platos_eliminar, name='platos_eliminar'),

    # Empleados
    path('empleados/', views.empleados_lista, name='empleados_lista'),
    path('empleados/nuevo/', views.empleados_crear, name='empleados_crear'),
    path('empleados/editar/<int:pk>/', views.empleados_editar, name='empleados_editar'),
    path('empleados/eliminar/<int:pk>/', views.empleados_eliminar, name='empleados_eliminar'),

    # Mesas
    path('mesas/', views.mesas_lista, name='mesas_lista'),
    path('mesas/nueva/', views.mesas_crear, name='mesas_crear'),
    path('mesas/editar/<int:pk>/', views.mesas_editar, name='mesas_editar'),
    path('mesas/eliminar/<int:pk>/', views.mesas_eliminar, name='mesas_eliminar'),

    # Ordenes
    path('ordenes/', views.ordenes_lista, name='ordenes_lista'),
    path('ordenes/nueva/', views.ordenes_crear, name='ordenes_crear'),
    path('ordenes/editar/<int:pk>/', views.ordenes_editar, name='ordenes_editar'),
    path('ordenes/eliminar/<int:pk>/', views.ordenes_eliminar, name='ordenes_eliminar'),

    # Detalle Ordenes
    path('ordenes/<int:orden_pk>/detalle/', views.detalle_orden_lista, name='detalle_orden_lista'),
    path('ordenes/<int:orden_pk>/detalle/agregar/', views.detalle_orden_crear, name='detalle_orden_crear'),
    path('ordenes/detalle/eliminar/<int:pk>/', views.detalle_orden_eliminar, name='detalle_orden_eliminar'),

    # Facturas
    path('facturas/', views.facturas_lista, name='facturas_lista'),
    path('facturas/nueva/', views.facturas_crear, name='facturas_crear'),
    path('facturas/eliminar/<int:pk>/', views.facturas_eliminar, name='facturas_eliminar'),
]