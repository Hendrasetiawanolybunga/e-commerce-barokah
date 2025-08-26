# core/views.py
from django.shortcuts import render, redirect, get_object_or_404
from .models import Product
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Product, Order, OrderItem
import datetime

def product_list(request):
    products = Product.objects.filter(is_available=True)
    context = {
        'products': products
    }
    return render(request, 'core/product_list.html', context)

def add_to_cart(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    cart = request.session.get('cart', {})
    product_id_str = str(product_id)

    if product_id_str in cart:
        cart[product_id_str]['quantity'] += 1
    else:
        cart[product_id_str] = {
            'name': product.name,
            'price': float(product.price),
            'quantity': 1,
            'image': str(product.image.url) if product.image else None,
        }

    request.session['cart'] = cart
    return redirect('product_list')

def cart(request):
    cart = request.session.get('cart', {})
    cart_items = []
    total_price = 0
    for product_id_str, item in cart.items():
        subtotal = item['price'] * item['quantity']
        total_price += subtotal
        cart_items.append({
            'product_id': int(product_id_str),
            'name': item['name'],
            'quantity': item['quantity'],
            'price': item['price'],
            'subtotal': subtotal,
            'image': item['image'],
        })
    
    context = {
        'cart_items': cart_items,
        'total_price': total_price
    }
    return render(request, 'core/cart.html', context)


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'core/register.html', {'form': form})


@login_required
def checkout(request):
    cart = request.session.get('cart', {})
    if not cart:
        return redirect('product_list') # Redirect jika keranjang kosong

    if request.method == 'POST':
        # Simpan bukti bayar
        proof_image = request.FILES.get('payment_proof')
        
        # Buat objek Order baru
        new_order = Order.objects.create(
            customer=request.user,
            total_price=request.session['total_price'],
            payment_proof_image=proof_image
        )

        # Buat objek OrderItem dari data keranjang
        for product_id_str, item in cart.items():
            product = get_object_or_404(Product, pk=int(product_id_str))
            OrderItem.objects.create(
                order=new_order,
                product=product,
                quantity=item['quantity'],
                price=item['price']
            )

        # Kosongkan keranjang setelah checkout berhasil
        del request.session['cart']
        del request.session['total_price']
        
        return render(request, 'core/order_success.html', {'order_id': new_order.id})

    # Logika untuk menampilkan halaman checkout (GET request)
    cart_items = []
    total_price = 0
    for product_id_str, item in cart.items():
        subtotal = item['price'] * item['quantity']
        total_price += subtotal
        cart_items.append({
            'name': item['name'],
            'quantity': item['quantity'],
            'price': item['price'],
            'subtotal': subtotal,
        })
    
    # Simpan total price di sesi agar bisa diakses saat POST
    request.session['total_price'] = total_price

    context = {
        'cart_items': cart_items,
        'total_price': total_price
    }
    return render(request, 'core/checkout.html', context)



def remove_from_cart(request, product_id):
    cart = request.session.get('cart', {})
    product_id_str = str(product_id)

    if product_id_str in cart:
        del cart[product_id_str]
        request.session['cart'] = cart
    return redirect('cart')

def update_cart(request, product_id):
    cart = request.session.get('cart', {})
    product_id_str = str(product_id)

    if request.method == 'POST':
        try:
            quantity = int(request.POST.get('quantity'))
            if quantity > 0:
                cart[product_id_str]['quantity'] = quantity
            else:
                del cart[product_id_str]
        except (ValueError, KeyError):
            pass # Lakukan sesuatu jika input tidak valid

    request.session['cart'] = cart
    return redirect('cart')



from django.shortcuts import get_object_or_404
from .forms import ReviewForm
from django.contrib import messages

# ... (views sebelumnya) ...

def product_detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    reviews = product.reviews.all().order_by('-created_at')
    
    review_form = ReviewForm()
    
    if request.method == 'POST':
        if not request.user.is_authenticated:
            messages.error(request, 'Anda harus login untuk memberikan ulasan.')
            return redirect('login')
        
        review_form = ReviewForm(request.POST)
        if review_form.is_valid():
            new_review = review_form.save(commit=False)
            new_review.product = product
            new_review.user = request.user
            new_review.save()
            messages.success(request, 'Ulasan Anda berhasil ditambahkan!')
            return redirect('product_detail', product_id=product.id)

    context = {
        'product': product,
        'reviews': reviews,
        'review_form': review_form,
    }
    return render(request, 'core/product_detail.html', context)