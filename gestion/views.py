from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Cliente, Empleado, Mesa, Plato, Orden, DetalleOrden, Factura

@login_required
def index(request):
    return render(request, 'index.html', {
        'total_clientes': Cliente.objects.count(),
        'total_platos': Plato.objects.count(),
        'total_empleados': Empleado.objects.count(),
        'total_mesas': Mesa.objects.count(),
        'total_ordenes': Orden.objects.count(),
        'total_facturas': Factura.objects.count(),
    })

# ===== CLIENTES =====
@login_required
def clientes_lista(request):
    clientes = Cliente.objects.all()
    return render(request, 'clientes/lista.html', {'object_list': clientes})

@login_required
def clientes_crear(request):
    if request.method == 'POST':
        Cliente.objects.create(
            nombre=request.POST['nombre'],
            telefono=request.POST.get('telefono', ''),
            correo=request.POST.get('correo', '')
        )
        return redirect('clientes_lista')
    return render(request, 'clientes/form.html', {'titulo': 'Nuevo Cliente'})

@login_required
def clientes_editar(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    if request.method == 'POST':
        cliente.nombre = request.POST['nombre']
        cliente.telefono = request.POST.get('telefono', '')
        cliente.correo = request.POST.get('correo', '')
        cliente.save()
        return redirect('clientes_lista')
    return render(request, 'clientes/form.html', {'titulo': 'Editar Cliente', 'objeto': cliente})

@login_required
def clientes_eliminar(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    if request.method == 'POST':
        cliente.delete()
        return redirect('clientes_lista')
    return render(request, 'clientes/confirmar_eliminar.html', {'objeto': cliente, 'nombre': 'cliente'})

# ===== PLATOS =====
@login_required
def platos_lista(request):
    platos = Plato.objects.all()
    return render(request, 'platos/lista.html', {'object_list': platos})

@login_required
def platos_crear(request):
    if request.method == 'POST':
        Plato.objects.create(
            nombre_plato=request.POST['nombre_plato'],
            descripcion=request.POST.get('descripcion', ''),
            precio=request.POST['precio'],
            categoria=request.POST.get('categoria', ''),
            disponible='disponible' in request.POST
        )
        return redirect('platos_lista')
    return render(request, 'platos/form.html', {'titulo': 'Nuevo Plato'})

@login_required
def platos_editar(request, pk):
    plato = get_object_or_404(Plato, pk=pk)
    if request.method == 'POST':
        plato.nombre_plato = request.POST['nombre_plato']
        plato.descripcion = request.POST.get('descripcion', '')
        plato.precio = request.POST['precio']
        plato.categoria = request.POST.get('categoria', '')
        plato.disponible = 'disponible' in request.POST
        plato.save()
        return redirect('platos_lista')
    return render(request, 'platos/form.html', {'titulo': 'Editar Plato', 'objeto': plato})

@login_required
def platos_eliminar(request, pk):
    plato = get_object_or_404(Plato, pk=pk)
    if request.method == 'POST':
        plato.delete()
        return redirect('platos_lista')
    return render(request, 'platos/confirmar_eliminar.html', {'objeto': plato, 'nombre': 'plato'})

# ===== EMPLEADOS =====
@login_required
def empleados_lista(request):
    empleados = Empleado.objects.all()
    return render(request, 'empleados/lista.html', {'object_list': empleados})

@login_required
def empleados_crear(request):
    if request.method == 'POST':
        Empleado.objects.create(
            nombre=request.POST['nombre'],
            cargo=request.POST['cargo'],
            telefono=request.POST.get('telefono', ''),
            correo=request.POST.get('correo', '')
        )
        return redirect('empleados_lista')
    return render(request, 'empleados/form.html', {'titulo': 'Nuevo Empleado'})

@login_required
def empleados_editar(request, pk):
    empleado = get_object_or_404(Empleado, pk=pk)
    if request.method == 'POST':
        empleado.nombre = request.POST['nombre']
        empleado.cargo = request.POST['cargo']
        empleado.telefono = request.POST.get('telefono', '')
        empleado.correo = request.POST.get('correo', '')
        empleado.save()
        return redirect('empleados_lista')
    return render(request, 'empleados/form.html', {'titulo': 'Editar Empleado', 'objeto': empleado})

@login_required
def empleados_eliminar(request, pk):
    empleado = get_object_or_404(Empleado, pk=pk)
    if request.method == 'POST':
        empleado.delete()
        return redirect('empleados_lista')
    return render(request, 'empleados/confirmar_eliminar.html', {'objeto': empleado, 'nombre': 'empleado'})

# ===== MESAS =====
@login_required
def mesas_lista(request):
    mesas = Mesa.objects.all()
    return render(request, 'mesas/lista.html', {'object_list': mesas})

@login_required
def mesas_crear(request):
    if request.method == 'POST':
        Mesa.objects.create(
            numero_mesa=request.POST['numero_mesa'],
            capacidad=request.POST['capacidad'],
            estado_mesa=request.POST['estado_mesa']
        )
        return redirect('mesas_lista')
    return render(request, 'mesas/form.html', {'titulo': 'Nueva Mesa'})

@login_required
def mesas_editar(request, pk):
    mesa = get_object_or_404(Mesa, pk=pk)
    if request.method == 'POST':
        mesa.numero_mesa = request.POST['numero_mesa']
        mesa.capacidad = request.POST['capacidad']
        mesa.estado_mesa = request.POST['estado_mesa']
        mesa.save()
        return redirect('mesas_lista')
    return render(request, 'mesas/form.html', {'titulo': 'Editar Mesa', 'objeto': mesa})

@login_required
def mesas_eliminar(request, pk):
    mesa = get_object_or_404(Mesa, pk=pk)
    if request.method == 'POST':
        mesa.delete()
        return redirect('mesas_lista')
    return render(request, 'mesas/confirmar_eliminar.html', {'objeto': mesa, 'nombre': 'mesa'})

# ===== ORDENES =====
@login_required
def ordenes_lista(request):
    ordenes = Orden.objects.all()
    return render(request, 'ordens/lista.html', {'object_list': ordenes})

@login_required
def ordenes_crear(request):
    if request.method == 'POST':
        Orden.objects.create(
            cliente=get_object_or_404(Cliente, pk=request.POST['cliente']),
            empleado=get_object_or_404(Empleado, pk=request.POST['empleado']),
            mesa=get_object_or_404(Mesa, pk=request.POST['mesa']),
            fecha_hora=request.POST.get('fecha_hora', None),
            estado_orden=request.POST['estado_orden']
        )
        return redirect('ordenes_lista')
    return render(request, 'ordens/form.html', {
        'titulo': 'Nueva Orden',
        'clientes': Cliente.objects.all(),
        'empleados': Empleado.objects.all(),
        'mesas': Mesa.objects.all(),
    })

@login_required
def ordenes_editar(request, pk):
    orden = get_object_or_404(Orden, pk=pk)
    if request.method == 'POST':
        orden.cliente = get_object_or_404(Cliente, pk=request.POST['cliente'])
        orden.empleado = get_object_or_404(Empleado, pk=request.POST['empleado'])
        orden.mesa = get_object_or_404(Mesa, pk=request.POST['mesa'])
        orden.fecha_hora = request.POST.get('fecha_hora', None)
        orden.estado_orden = request.POST['estado_orden']
        orden.save()
        return redirect('ordenes_lista')
    return render(request, 'ordens/form.html', {
        'titulo': 'Editar Orden',
        'objeto': orden,
        'clientes': Cliente.objects.all(),
        'empleados': Empleado.objects.all(),
        'mesas': Mesa.objects.all(),
    })

@login_required
def ordenes_eliminar(request, pk):
    orden = get_object_or_404(Orden, pk=pk)
    if request.method == 'POST':
        orden.delete()
        return redirect('ordenes_lista')
    return render(request, 'ordens/confirmar_eliminar.html', {'objeto': orden, 'nombre': 'orden'})

# ===== DETALLE ORDENES =====
@login_required
def detalle_orden_lista(request, orden_pk):
    orden = get_object_or_404(Orden, pk=orden_pk)
    detalles = orden.detalles.all()
    return render(request, 'detalle_ordens/lista.html', {'orden': orden, 'object_list': detalles})

@login_required
def detalle_orden_crear(request, orden_pk):
    orden = get_object_or_404(Orden, pk=orden_pk)
    if request.method == 'POST':
        DetalleOrden.objects.create(
            orden=orden,
            plato=get_object_or_404(Plato, pk=request.POST['plato']),
            cantidad=request.POST['cantidad']
        )
        return redirect('detalle_orden_lista', orden_pk=orden.pk)
    return render(request, 'detalle_ordens/form.html', {
        'titulo': 'Agregar Plato a Orden',
        'orden': orden,
        'platos': Plato.objects.filter(disponible=True)
    })

@login_required
def detalle_orden_eliminar(request, pk):
    detalle = get_object_or_404(DetalleOrden, pk=pk)
    orden_pk = detalle.orden.pk
    if request.method == 'POST':
        detalle.delete()
        return redirect('detalle_orden_lista', orden_pk=orden_pk)
    return render(request, 'detalle_ordens/confirmar_eliminar.html', {'objeto': detalle, 'nombre': 'detalle'})

# ===== FACTURAS =====
@login_required
def facturas_lista(request):
    facturas = Factura.objects.all()
    return render(request, 'facturas/lista.html', {'object_list': facturas})

@login_required
def facturas_crear(request):
    if request.method == 'POST':
        orden = get_object_or_404(Orden, pk=request.POST['orden'])
        subtotal = orden.total
        impuesto = subtotal * 19 / 100
        Factura.objects.create(
            orden=orden,
            subtotal=subtotal,
            impuesto=impuesto,
            total_factura=subtotal + impuesto,
            metodo_pago=request.POST['metodo_pago'],
            fecha_factura=request.POST.get('fecha_factura', None)
        )
        return redirect('facturas_lista')
    ordenes_sin_factura = Orden.objects.filter(factura__isnull=True)
    return render(request, 'facturas/form.html', {
        'titulo': 'Nueva Factura',
        'ordenes': ordenes_sin_factura
    })

@login_required
def facturas_eliminar(request, pk):
    factura = get_object_or_404(Factura, pk=pk)
    if request.method == 'POST':
        factura.delete()
        return redirect('facturas_lista')
    return render(request, 'facturas/confirmar_eliminar.html', {'objeto': factura, 'nombre': 'factura'})

# Create your views here.
