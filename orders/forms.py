from django import forms
from django.forms import inlineformset_factory
from .models import Order, OrderItem


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['status', 'pickup_point', 'delivery_date']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-control'}),
            'pickup_point': forms.Select(attrs={'class': 'form-control'}),
            'delivery_date': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
        }


class OrderItemForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = ['product', 'quantity']
        widgets = {
            'product': forms.Select(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'min': '1'}),
        }


OrderItemFormSet = inlineformset_factory(
    Order, OrderItem,
    form=OrderItemForm,
    extra=1,
    can_delete=True
)
