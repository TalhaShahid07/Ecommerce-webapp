
# Create your views here.
# cart/views.py
from orders.models import Order, OrderItem, render,redirect
from django.contrib.auth.decorators import login_required


@login_required
def checkout(request):
    cart, created = cart.objects.get_or_create(user=request.user)
    items = cart.items.all()
    total = sum(item.total_price() for item in items)

    if request.method == 'POST':
        # Create the order
        order = Order.objects.create(user=request.user, total=total, status='Pending')
        for item in items:
            OrderItem.objects.create(order=order, product=item.product, quantity=item.quantity, price=item.product.price)
        cart.items.all().delete()  # Clear the cart
        return redirect('order-confirmation')  # Redirect to an order confirmation page

    return render(request, 'cart/checkout.html', {'cart': cart, 'items': items, 'total': total})

# orders/views.py

@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'orders/order_history.html', {'orders': orders})
