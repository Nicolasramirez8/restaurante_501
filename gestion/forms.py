from django import forms
from django.contrib.auth.models import User
from .models import Cliente, Empleado, Mesa, Plato, Orden, DetalleOrden, Factura, PerfilUsuario


class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nombre', 'telefono', 'correo']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={
                'class': 'form-control',
                'pattern': '[0-9]+',
                'inputmode': 'numeric',
                'title': 'Solo se permiten números',
                'oninput': 'this.value = this.value.replace(/[^0-9]/g, "")'
            }),
            'correo': forms.EmailInput(attrs={'class': 'form-control'}),
        }


class EmpleadoForm(forms.ModelForm):
    class Meta:
        model = Empleado
        fields = ['nombre', 'cargo', 'telefono', 'correo']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'cargo': forms.Select(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={
                'class': 'form-control',
                'pattern': '[0-9]+',
                'inputmode': 'numeric',
                'title': 'Solo se permiten números',
                'oninput': 'this.value = this.value.replace(/[^0-9]/g, "")'
            }),
            'correo': forms.EmailInput(attrs={'class': 'form-control'}),
        }


class MesaForm(forms.ModelForm):
    class Meta:
        model = Mesa
        fields = ['numero_mesa', 'capacidad', 'estado_mesa']
        widgets = {
            'numero_mesa': forms.NumberInput(attrs={'class': 'form-control'}),
            'capacidad': forms.NumberInput(attrs={'class': 'form-control'}),
            'estado_mesa': forms.Select(attrs={'class': 'form-control'}),
        }


class PlatoForm(forms.ModelForm):
    class Meta:
        model = Plato
        fields = ['nombre_plato', 'descripcion', 'precio', 'categoria', 'disponible']
        widgets = {
            'nombre_plato': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'precio': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'categoria': forms.TextInput(attrs={'class': 'form-control'}),
            'disponible': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class OrdenForm(forms.ModelForm):
    class Meta:
        model = Orden
        fields = ['cliente', 'empleado', 'mesa', 'estado_orden']
        widgets = {
            'cliente': forms.Select(attrs={'class': 'form-control'}),
            'empleado': forms.Select(attrs={'class': 'form-control'}),
            'mesa': forms.Select(attrs={'class': 'form-control'}),
            'estado_orden': forms.Select(attrs={'class': 'form-control'}),
        }


class DetalleOrdenForm(forms.ModelForm):
    class Meta:
        model = DetalleOrden
        fields = ['plato', 'cantidad']
        widgets = {
            'plato': forms.Select(attrs={'class': 'form-control'}),
            'cantidad': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['plato'].queryset = Plato.objects.filter(disponible=True)


class FacturaForm(forms.ModelForm):
    class Meta:
        model = Factura
        fields = ['orden', 'subtotal', 'impuesto', 'total_factura', 'metodo_pago']
        widgets = {
            'orden': forms.Select(attrs={'class': 'form-control'}),
            'subtotal': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'impuesto': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'total_factura': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'metodo_pago': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['orden'].queryset = Orden.objects.filter(
            estado_orden='Entregada'
        ).exclude(factura__isnull=False)


class RegistroUsuarioForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}), label='Contraseña')
    rol = forms.ChoiceField(choices=PerfilUsuario.ROLES, widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
            rol = self.cleaned_data['rol']
            PerfilUsuario.objects.create(usuario=user, rol=rol)
            if rol in ['mesero', 'cajero']:
                cargo_map = {
                    'mesero': 'Mesero',
                    'cajero': 'Cajero',
                }
                Empleado.objects.create(
                    nombre=user.get_full_name() or user.username,
                    cargo=cargo_map[rol],
                    correo=user.email or None,
                )
        return user
    
class EstadoOrdenForm(forms.ModelForm):
    class Meta:
        model = Orden
        fields = ['estado_orden']
        widgets = {
            'estado_orden': forms.Select(attrs={'class': 'form-control'}),
        }
