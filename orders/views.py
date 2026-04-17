from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Order
from .forms import OrderForm, OrderItemFormSet
import uuid


def get_user_role(user):
    if user.is_superuser:
        return 'admin'
    if user.groups.filter(name='Менеджеры').exists():
        return 'manager'
    if user.groups.filter(name='Клиенты').exists():
        return 'client'
    return 'client'


@login_required
def order_list(request):
    role = get_user_role(request.user)

    if role in ('admin', 'manager'):
        orders = Order.objects.select_related('customer', 'status', 'pickup_point').all()
    else:
        orders = Order.objects.select_related('customer', 'status', 'pickup_point').filter(customer=request.user)

    return render(request, 'orders/order_list.html', {
        'orders': orders,
        'user_role': role,
    })


@login_required
def order_create(request):
    role = get_user_role(request.user)

    if request.method == 'POST':
        form = OrderForm(request.POST)
        formset = OrderItemFormSet(request.POST)
        if form.is_valid() and formset.is_valid():
            order = form.save(commit=False)
            order.customer = request.user
            order.order_number = f"ORD-{uuid.uuid4().hex[:8].upper()}"
            order.save()
            formset.instance = order
            items = formset.save(commit=False)
            for item in items:
                item.price = item.product.final_price
                item.save()
            messages.success(request, 'Заказ успешно создан.')
            return redirect('orders:order_list')
    else:
        form = OrderForm()
        formset = OrderItemFormSet()

    return render(request, 'orders/order_form.html', {
        'form': form,
        'formset': formset,
        'title': 'Создать заказ',
        'user_role': role,
    })


@login_required
def order_update(request, pk):
    role = get_user_role(request.user)
    order = get_object_or_404(Order, pk=pk)

    if role == 'client' and order.customer != request.user:
        messages.error(request, 'У вас нет прав для редактирования этого заказа.')
        return redirect('orders:order_list')

    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        formset = OrderItemFormSet(request.POST, instance=order)
        if form.is_valid() and formset.is_valid():
            form.save()
            items = formset.save(commit=False)
            for item in items:
                item.price = item.product.final_price
                item.save()
            for item in formset.deleted_objects:
                item.delete()
            messages.success(request, 'Заказ успешно обновлён.')
            return redirect('orders:order_list')
    else:
        form = OrderForm(instance=order)
        formset = OrderItemFormSet(instance=order)

    return render(request, 'orders/order_form.html', {
        'form': form,
        'formset': formset,
        'order': order,
        'title': 'Редактировать заказ',
        'user_role': role,
    })


@login_required
def order_delete(request, pk):
    role = get_user_role(request.user)
    order = get_object_or_404(Order, pk=pk)

    if role == 'client':
        messages.error(request, 'У вас нет прав для удаления заказа.')
        return redirect('orders:order_list')

    if request.method == 'POST':
        order.delete()
        messages.success(request, 'Заказ успешно удалён.')
        return redirect('orders:order_list')

    return render(request, 'orders/order_confirm_delete.html', {
        'order': order,
        'user_role': role,
    })
