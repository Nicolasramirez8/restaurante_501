from django.urls import path
from . import views

urlpatterns = [
    # Auth
    path('', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),

    # Clientes
    path('clientes/', views.cliente_list, name='cliente_list'),
    path('clientes/nuevo/', views.cliente_create, name='cliente_create'),
    path('clientes/<int:pk>/editar/', views.cliente_edit, name='cliente_edit'),
    path('clientes/<int:pk>/eliminar/', views.cliente_delete, name='cliente_delete'),

    # Empleados
    path('empleados/', views.empleado_list, name='empleado_list'),
    path('empleados/nuevo/', views.empleado_create, name='empleado_create'),
    path('empleados/<int:pk>/editar/', views.empleado_edit, name='empleado_edit'),
    path('empleados/<int:pk>/eliminar/', views.empleado_delete, name='empleado_delete'),

    # Mesas
    path('mesas/', views.mesa_list, name='mesa_list'),
    path('mesas/nueva/', views.mesa_create, name='mesa_create'),
    path('mesas/<int:pk>/editar/', views.mesa_edit, name='mesa_edit'),
    path('mesas/<int:pk>/eliminar/', views.mesa_delete, name='mesa_delete'),

    # Platos
    path('platos/', views.plato_list, name='plato_list'),
    path('platos/nuevo/', views.plato_create, name='plato_create'),
    path('platos/<int:pk>/editar/', views.plato_edit, name='plato_edit'),
    path('platos/<int:pk>/eliminar/', views.plato_delete, name='plato_delete'),

    # Órdenes
    path('ordenes/', views.orden_list, name='orden_list'),
    path('ordenes/nueva/', views.orden_create, name='orden_create'),
    path('ordenes/<int:pk>/', views.orden_detail, name='orden_detail'),
    path('ordenes/<int:pk>/editar/', views.orden_edit, name='orden_edit'),
    path('ordenes/<int:pk>/eliminar/', views.orden_delete, name='orden_delete'),
    path('ordenes/detalle/<int:pk>/eliminar/', views.detalle_delete, name='detalle_delete'),

    # Facturas
    path('facturas/', views.factura_list, name='factura_list'),
    path('facturas/nueva/', views.factura_create, name='factura_create'),
    path('facturas/nueva/<int:orden_pk>/', views.factura_create, name='factura_create_orden'),
    path('facturas/<int:pk>/eliminar/', views.factura_delete, name='factura_delete'),

    # Usuarios
    path('usuarios/', views.usuario_list, name='usuario_list'),
    path('usuarios/nuevo/', views.usuario_create, name='usuario_create'),
    path('usuarios/<int:pk>/eliminar/', views.usuario_delete, name='usuario_delete'),


    path('ordenes/<int:pk>/cerrar-mesa/', views.cerrar_mesa, name='cerrar_mesa'),
]
