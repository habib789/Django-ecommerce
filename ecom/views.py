from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Cart, Order, Address
from django.views.generic import ListView, DetailView, View, TemplateView
from django.utils import timezone
from django.contrib import messages
from django.http import Http404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import BillingForm


class ProductView(ListView):
    model = Product
    paginate_by = 6


class ProductDetailView(DetailView):
    model = Product


class CartView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            cart = Order.objects.get(user=self.request.user, order_status=False)
        except:
            # raise Http404
            return render(self.request, 'ecom/cart.html', {})
        else:
            context = {'objects': cart}
        return render(self.request, 'ecom/cart.html', context)


def item_search(request):
    if request.method == 'POST':
        search_item = request.POST['searched']
        if search_item != '':
            search_title = Product.objects.filter(title__icontains=search_item)
            return render(request, 'ecom/search.html', {'search_item': search_item,
                                                        'search_title': search_title})
        else:
            return redirect('products:product_list')


@login_required
def add_to_cart(request, pk):
    product = get_object_or_404(Product, pk=pk)
    order_product, created = Cart.objects.get_or_create(products=product,
                                                        user=request.user,
                                                        status='pending')
    order_qs = Order.objects.filter(user=request.user, order_status=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.cart_products.filter(products__pk=product.pk).exists():
            order_product.quantity += 1
            order_product.save()
            messages.success(request, 'Product Quantity updated')
            return redirect('products:cart')
        else:
            messages.success(request, 'Product added to the cart')
            order.cart_products.add(order_product)
            return redirect('products:product_list')
    else:
        order = Order.objects.create(user=request.user, order_date=timezone.now())
        order.cart_products.add(order_product)
        messages.success(request, 'Product added to the cart')
        return redirect('products:product_list')


@login_required
def remove_from_cart(request, pk):
    product = get_object_or_404(Product, pk=pk)
    order_product = Cart.objects.get(products=product, user=request.user, status='pending')
    order_qs = Order.objects.filter(user=request.user, order_status=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.cart_products.filter(products__pk=product.pk).exists():
            order_product.delete()
            messages.info(request, 'Product Removed')
            return redirect('products:cart')
        else:
            messages.error(request, 'This product is not in your cart')
            return redirect('products:cart')
    else:
        messages.error(request, "You don't have an active order!!")
        return redirect('products:product_list')


@login_required
def reduce_from_cart(request, pk):
    product = get_object_or_404(Product, pk=pk)
    order_product = Cart.objects.get(products=product, user=request.user, status='pending')
    order_qs = Order.objects.filter(user=request.user, order_status=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.cart_products.filter(products__pk=product.pk).exists():
            if order_product.quantity > 1:
                order_product.quantity -= 1
                order_product.save()
                messages.info(request, 'Product Quantity Updated')
                # alert('updated')
                return redirect('products:cart')
            else:
                order_product.delete()
                messages.info(request, 'Product Removed')
                return redirect('products:cart')
        else:
            messages.error(request, 'This product is not in your cart')
            return redirect('products:cart')
    else:
        messages.error(request, "You don't have an active order!!")
        return redirect('products:product_list')


class Checkout(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        form = BillingForm()
        try:
            cart = Order.objects.get(user=self.request.user, order_status=False)
        except:
            raise Http404
        else:
            context = {'objects': cart, 'form': form}
        return render(self.request, 'ecom/checkout.html', context)

    def post(self, *args, **kwargs):
        form = BillingForm(self.request.POST or None)
        try:
            order = Order.objects.get(user=self.request.user, order_status=False)
            if form.is_valid():
                customer_name = form.cleaned_data.get('customer_name')
                contact_no = form.cleaned_data.get('contact_no')
                street_address = form.cleaned_data.get('street_address')
                country = form.cleaned_data.get('country')
                zip = form.cleaned_data.get('zip')
                payment = form.cleaned_data.get('payment')
                # print(contact_no)
                billing = Address(
                    user=self.request.user,
                    customer_name=customer_name,
                    contact_no=contact_no,
                    street_address=street_address,
                    country=country,
                    zip=zip,
                )
                # print(form.cleaned_data)
                billing.save()
                order.order_address = billing
                if payment == 'c':
                    order.order_status = True
                order.save()
                messages.info(self.request, 'YOUR ORDER HAS BEEN PLACED')
                if payment == 'c':
                    return redirect('products:product_list')
                else:
                    return redirect('products:checkout')
            else:
                messages.info(self.request, 'Invalid')
                return redirect('products:checkout')
        except:
            messages.warning(self.request, 'Invalid')
            return redirect('products:cart')

