from django import forms
from .models import Pedido


class PedidoForm(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = [
            'nombre_comprador',
            'correo_comprador',
            'telefono_comprador',
            'cantidad'
        ]

        labels = {
            'nombre_comprador': 'Nombre completo',
            'correo_comprador': 'Correo electrónico',
            'telefono_comprador': 'Teléfono',
            'cantidad': 'Cantidad de unidades'
        }

        widgets = {
            'nombre_comprador': forms.TextInput(
                attrs={'placeholder': 'Ingrese su nombre'}
            ),
            'correo_comprador': forms.EmailInput(
                attrs={'placeholder': 'Ingrese su correo'}
            ),
            'telefono_comprador': forms.TextInput(
                attrs={'placeholder': 'Ingrese su teléfono'}
            ),
            'cantidad': forms.NumberInput(
                attrs={'min': 1, 'max': 5}
            )
        }

    def clean_cantidad(self):
        cantidad = self.cleaned_data['cantidad']

        if cantidad < 1 or cantidad > 5:
            raise forms.ValidationError(
                'La cantidad debe estar entre 1 y 5 unidades.'
            )

        return cantidad