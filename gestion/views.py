from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Sum, Count
from django.utils import timezone
from functools import wraps
from .models import Cliente, Empleado, Mesa, Plato, Orden, DetalleOrden, Factura
from .forms import (ClienteForm, EmpleadoForm, MesaForm, PlatoForm,
                    OrdenForm, DetalleOrdenForm, FacturaForm, RegistroUsuarioForm, EstadoOrdenForm)

def login_required_custom(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        return view_func(request, *args, **kwargs)
    return wrapper
# ─── Decoradores de rol ───────────────────────────────────────────────────────

def rol_requerido(*roles):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('login')
            perfil = getattr(request.user, 'perfil', None)
            if perfil and perfil.rol in roles:
                return view_func(request, *args, **kwargs)
            messages.error(request, 'No tenés permiso para acceder a esta sección.')
            return redirect('dashboard')
        return _wrapped_view
    return decorator


# ─── Auth ─────────────────────────────────────────────────────────────────────

def login_view(request):
    if request.user.is_authenticated:
        logout(request)
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('dashboard')
        messages.error(request, 'Usuario o contraseña incorrectos.')
    return render(request, 'gestion/login.html')


@login_required
def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def dashboard(request):
    perfil = getattr(request.user, 'perfil', None)
    rol = perfil.rol if perfil else 'administrador'

    context = {'rol': rol}

    if rol == 'administrador':
        context.update({
            'total_clientes': Cliente.objects.count(),
            'total_empleados': Empleado.objects.count(),
            'total_mesas': Mesa.objects.count(),
            'total_platos': Plato.objects.count(),
            'ordenes_activas': Orden.objects.filter(estado_orden='Activa').count(),
            'ingresos_hoy': Factura.objects.filter(
                fecha_factura__date=timezone.now().date()
            ).aggregate(total=Sum('total_factura'))['total'] or 0,
        })
    elif rol == 'mesero':
        context.update({
            'mesas_disponibles': Mesa.objects.filter(estado_mesa='Disponible').count(),
            'mesas_ocupadas': Mesa.objects.filter(estado_mesa='Ocupada').count(),
            'mis_ordenes': Orden.objects.filter(estado_orden__in=['Activa', 'En preparación']).count(),
        })
    elif rol == 'cajero':
        context.update({
            'ordenes_pendientes': Orden.objects.filter(estado_orden='Entregada').count(),
            'facturas_hoy': Factura.objects.filter(fecha_factura__date=timezone.now().date()).count(),
            'ingresos_hoy': Factura.objects.filter(
                fecha_factura__date=timezone.now().date()
            ).aggregate(total=Sum('total_factura'))['total'] or 0,
        })

    return render(request, 'gestion/dashboard.html', context)


# ─── Clientes ─────────────────────────────────────────────────────────────────

@login_required
def cliente_list(request):
    perfil = getattr(request.user, 'perfil', None)
    rol = perfil.rol if perfil else 'administrador'
    if rol not in ['administrador', 'mesero']:
        messages.error(request, 'Acceso denegado.')
        return redirect('dashboard')
    clientes = Cliente.objects.all()
    return render(request, 'gestion/cliente_list.html', {'clientes': clientes, 'rol': rol})


@login_required
@rol_requerido('administrador')
def cliente_create(request):
    form = ClienteForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Cliente creado correctamente.')
        return redirect('cliente_list')
    return render(request, 'gestion/form.html', {'form': form, 'titulo': 'Nuevo Cliente', 'cancelar': 'cliente_list'})


@login_required
@rol_requerido('administrador')
def cliente_edit(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    form = ClienteForm(request.POST or None, instance=cliente)
    if form.is_valid():
        form.save()
        messages.success(request, 'Cliente actualizado.')
        return redirect('cliente_list')
    return render(request, 'gestion/form.html', {'form': form, 'titulo': 'Editar Cliente', 'cancelar': 'cliente_list'})


@login_required
@rol_requerido('administrador')
def cliente_delete(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    if request.method == 'POST':
        cliente.delete()
        messages.success(request, 'Cliente eliminado.')
        return redirect('cliente_list')
    return render(request, 'gestion/confirm_delete.html', {'objeto': cliente, 'cancelar': 'cliente_list'})


# ─── Empleados ────────────────────────────────────────────────────────────────

@login_required
@rol_requerido('administrador')
def empleado_list(request):
    empleados = Empleado.objects.all()
    return render(request, 'gestion/empleado_list.html', {'empleados': empleados})


@login_required
@rol_requerido('administrador')
def empleado_create(request):
    form = EmpleadoForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Empleado creado correctamente.')
        return redirect('empleado_list')
    return render(request, 'gestion/form.html', {'form': form, 'titulo': 'Nuevo Empleado', 'cancelar': 'empleado_list'})


@login_required
@rol_requerido('administrador')
def empleado_edit(request, pk):
    empleado = get_object_or_404(Empleado, pk=pk)
    form = EmpleadoForm(request.POST or None, instance=empleado)
    if form.is_valid():
        form.save()
        messages.success(request, 'Empleado actualizado.')
        return redirect('empleado_list')
    return render(request, 'gestion/form.html', {'form': form, 'titulo': 'Editar Empleado', 'cancelar': 'empleado_list'})


@login_required
@rol_requerido('administrador')
def empleado_delete(request, pk):
    empleado = get_object_or_404(Empleado, pk=pk)
    if request.method == 'POST':
        empleado.delete()
        messages.success(request, 'Empleado eliminado.')
        return redirect('empleado_list')
    return render(request, 'gestion/confirm_delete.html', {'objeto': empleado, 'cancelar': 'empleado_list'})


# ─── Mesas ────────────────────────────────────────────────────────────────────

@login_required
def mesa_list(request):
    perfil = getattr(request.user, 'perfil', None)
    rol = perfil.rol if perfil else 'administrador'
    if rol not in ['administrador', 'mesero']:
        messages.error(request, 'Acceso denegado.')
        return redirect('dashboard')
    mesas = Mesa.objects.all().order_by('numero_mesa')
    return render(request, 'gestion/mesa_list.html', {'mesas': mesas, 'rol': rol})


@login_required
@rol_requerido('administrador')
def mesa_create(request):
    form = MesaForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Mesa creada correctamente.')
        return redirect('mesa_list')
    return render(request, 'gestion/form.html', {'form': form, 'titulo': 'Nueva Mesa', 'cancelar': 'mesa_list'})


@login_required
@rol_requerido('administrador')
def mesa_edit(request, pk):
    mesa = get_object_or_404(Mesa, pk=pk)
    form = MesaForm(request.POST or None, instance=mesa)
    if form.is_valid():
        form.save()
        messages.success(request, 'Mesa actualizada.')
        return redirect('mesa_list')
    return render(request, 'gestion/form.html', {'form': form, 'titulo': 'Editar Mesa', 'cancelar': 'mesa_list'})


@login_required
@rol_requerido('administrador')
def mesa_delete(request, pk):
    mesa = get_object_or_404(Mesa, pk=pk)
    if request.method == 'POST':
        mesa.delete()
        messages.success(request, 'Mesa eliminada.')
        return redirect('mesa_list')
    return render(request, 'gestion/confirm_delete.html', {'objeto': mesa, 'cancelar': 'mesa_list'})


# ─── Platos ───────────────────────────────────────────────────────────────────

@login_required
def plato_list(request):
    perfil = getattr(request.user, 'perfil', None)
    rol = perfil.rol if perfil else 'administrador'
    if rol not in ['administrador', 'mesero']:
        messages.error(request, 'Acceso denegado.')
        return redirect('dashboard')
    platos = Plato.objects.all()
    return render(request, 'gestion/plato_list.html', {'platos': platos, 'rol': rol})


@login_required
@rol_requerido('administrador')
def plato_create(request):
    form = PlatoForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Plato creado correctamente.')
        return redirect('plato_list')
    return render(request, 'gestion/form.html', {'form': form, 'titulo': 'Nuevo Plato', 'cancelar': 'plato_list'})


@login_required
@rol_requerido('administrador')
def plato_edit(request, pk):
    plato = get_object_or_404(Plato, pk=pk)
    form = PlatoForm(request.POST or None, instance=plato)
    if form.is_valid():
        form.save()
        messages.success(request, 'Plato actualizado.')
        return redirect('plato_list')
    return render(request, 'gestion/form.html', {'form': form, 'titulo': 'Editar Plato', 'cancelar': 'plato_list'})


@login_required
@rol_requerido('administrador')
def plato_delete(request, pk):
    plato = get_object_or_404(Plato, pk=pk)
    if request.method == 'POST':
        plato.delete()
        messages.success(request, 'Plato eliminado.')
        return redirect('plato_list')
    return render(request, 'gestion/confirm_delete.html', {'objeto': plato, 'cancelar': 'plato_list'})


# ─── Órdenes ──────────────────────────────────────────────────────────────────

@login_required
def orden_list(request):
    perfil = getattr(request.user, 'perfil', None)
    rol = perfil.rol if perfil else 'administrador'
    if rol == 'cajero':
        ordenes = Orden.objects.filter(estado_orden='Entregada')
    else:
        ordenes = Orden.objects.all()
    return render(request, 'gestion/orden_list.html', {'ordenes': ordenes, 'rol': rol})


@login_required
@rol_requerido('administrador', 'mesero')
def orden_create(request):
    form = OrdenForm(request.POST or None)
    if form.is_valid():
        orden = form.save()
        orden.mesa.estado_mesa = 'Ocupada'
        orden.mesa.save()
        messages.success(request, 'Orden creada correctamente.')
        return redirect('orden_detail', pk=orden.pk)
    return render(request, 'gestion/form.html', {'form': form, 'titulo': 'Nueva Orden', 'cancelar': 'orden_list'})


@login_required
@rol_requerido('administrador', 'mesero')
def orden_edit(request, pk):
    orden = get_object_or_404(Orden, pk=pk)
    perfil = getattr(request.user, 'perfil', None)
    rol = perfil.rol if perfil else 'administrador'
    if rol == 'mesero' and orden.estado_orden in ['Facturada', 'Cancelada']:
        messages.error(request, 'No podés modificar una orden facturada o cancelada.')
        return redirect('orden_list')
    if rol == 'mesero':
        form = EstadoOrdenForm(request.POST or None, instance=orden)
    else:
        form = OrdenForm(request.POST or None, instance=orden)
    if form.is_valid():
        form.save()
        messages.success(request, 'Orden actualizada.')
        return redirect('orden_list')
    return render(request, 'gestion/form.html', {'form': form, 'titulo': 'Editar Orden', 'cancelar': 'orden_list'})




@login_required
def orden_detail(request, pk):
    orden = get_object_or_404(Orden, pk=pk)
    perfil = getattr(request.user, 'perfil', None)
    rol = perfil.rol if perfil else 'administrador'
    detalles = orden.detalles.all()
    form = DetalleOrdenForm(request.POST or None)
    if request.method == 'POST' and rol in ['administrador', 'mesero']:
        if form.is_valid():
            detalle = form.save(commit=False)
            detalle.orden = orden
            detalle.save()
            messages.success(request, 'Plato agregado a la orden.')
            return redirect('orden_detail', pk=pk)
    return render(request, 'gestion/orden_detail.html', {
        'orden': orden, 'detalles': detalles, 'form': form, 'rol': rol
    })


@login_required
@rol_requerido('administrador')
def orden_delete(request, pk):
    orden = get_object_or_404(Orden, pk=pk)
    if request.method == 'POST':
        orden.mesa.estado_mesa = 'Disponible'
        orden.mesa.save()
        orden.delete()
        messages.success(request, 'Orden eliminada.')
        return redirect('orden_list')
    return render(request, 'gestion/confirm_delete.html', {'objeto': orden, 'cancelar': 'orden_list'})


@login_required
@rol_requerido('administrador', 'mesero')
def detalle_delete(request, pk):
    detalle = get_object_or_404(DetalleOrden, pk=pk)
    orden_pk = detalle.orden.pk
    detalle.delete()
    messages.success(request, 'Plato eliminado de la orden.')
    return redirect('orden_detail', pk=orden_pk)


# ─── Facturas ─────────────────────────────────────────────────────────────────

@login_required
@rol_requerido('administrador', 'cajero')
def factura_list(request):
    facturas = Factura.objects.all().order_by('-fecha_factura')
    perfil = getattr(request.user, 'perfil', None)
    rol = perfil.rol if perfil else 'administrador'
    return render(request, 'gestion/factura_list.html', {'facturas': facturas, 'rol': rol})


@login_required
@rol_requerido('administrador', 'cajero')
def factura_create(request, orden_pk=None):
    orden = get_object_or_404(Orden, pk=orden_pk) if orden_pk else None
    if orden and hasattr(orden, 'factura'):
        messages.warning(request, 'Esta orden ya tiene factura.')
        return redirect('factura_list')
    initial = {}
    if orden:
        subtotal = orden.total
        impuesto = subtotal * 19 / 100
        initial = {
            'orden': orden,
            'subtotal': subtotal,
            'impuesto': round(impuesto, 2),
            'total_factura': round(subtotal + impuesto, 2),
        }
    form = FacturaForm(request.POST or None, initial=initial)
    if form.is_valid():
        factura = form.save()
        factura.orden.estado_orden = 'Facturada'
        factura.orden.mesa.estado_mesa = 'Disponible'
        factura.orden.mesa.save()
        factura.orden.save()
        messages.success(request, 'Factura generada correctamente.')
        return redirect('factura_list')
    return render(request, 'gestion/form.html', {'form': form, 'titulo': 'Generar Factura', 'cancelar': 'factura_list'})


@login_required
@rol_requerido('administrador')
def factura_delete(request, pk):
    factura = get_object_or_404(Factura, pk=pk)
    if request.method == 'POST':
        factura.delete()
        messages.success(request, 'Factura eliminada.')
        return redirect('factura_list')
    return render(request, 'gestion/confirm_delete.html', {'objeto': factura, 'cancelar': 'factura_list'})

@login_required

@rol_requerido('administrador', 'cajero')
def cerrar_mesa(request, pk):
    orden = get_object_or_404(Orden, pk=pk)
    if request.method == 'POST':
        orden.mesa.estado_mesa = 'Disponible'
        orden.mesa.save()
        orden.estado_orden = 'Facturada'
        orden.save()
        messages.success(request, f'Mesa {orden.mesa.numero_mesa} cerrada correctamente.')
        return redirect('orden_list')
    return render(request, 'gestion/confirm_delete.html', {'objeto': f'la cuenta de Mesa {orden.mesa.numero_mesa}', 'cancelar': 'orden_list'})


# ─── Usuarios y Roles ─────────────────────────────────────────────────────────

@login_required
@rol_requerido('administrador')
def usuario_list(request):
    usuarios = User.objects.all().select_related('perfil')
    return render(request, 'gestion/usuario_list.html', {'usuarios': usuarios})


@login_required
@rol_requerido('administrador')
def usuario_create(request):
    form = RegistroUsuarioForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Usuario creado correctamente.')
        return redirect('usuario_list')
    return render(request, 'gestion/form.html', {'form': form, 'titulo': 'Nuevo Usuario', 'cancelar': 'usuario_list'})


@login_required
@rol_requerido('administrador')
def usuario_delete(request, pk):
    usuario = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        usuario.delete()
        messages.success(request, 'Usuario eliminado.')
        return redirect('usuario_list')
    return render(request, 'gestion/confirm_delete.html', {'objeto': usuario, 'cancelar': 'usuario_list'})
