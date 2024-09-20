from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Cart, CartItem
from products.models import Product

@login_required
def checkout(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    items = cart.items.all()
    total = sum(item.total_price() for item in items)

    if request.method == 'POST':
        # Handle checkout logic here
        # For example, process payment and create an order
        # Then clear the cart
        cart.items.all().delete()
        return redirect('order-confirmation')  # Redirect to an order confirmation page

    return render(request, 'cart/checkout.html', {'cart': cart, 'items': items, 'total': total})

@login_required
def view_cart(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    items = cart.items.all()
    total = sum(item.total_price() for item in items)
    return render(request, 'cart/view_cart.html', {'cart': cart, 'items': items, 'total': total})

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    return redirect('view-cart')

@login_required
def remove_from_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = Cart.objects.get(user=request.user)
    CartItem.objects.filter(cart=cart, product=product).delete()
    return redirect('view-cart')

@login_required
def update_cart(request, product_id, quantity):
    product = get_object_or_404(Product, id=product_id)
    cart = Cart.objects.get(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if quantity > 0:
        cart_item.quantity = quantity
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('view-cart')


def order_confirmation(request):
    return render(request, 'cart/order_confirmation.html')


