from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Cart, Order, Address, Category, SubCategory
from django.views.generic import ListView, DetailView, View, TemplateView
from django.utils import timezone
from django.contrib import messages
from django.http import Http404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import BillingForm
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags


class ProductView(ListView):
    model = Product
    paginate_by = 8


def product_view(request, pk=None, p_or_c=None):
    if p_or_c is None:
        product_list = Product.objects.all()
    elif p_or_c == 'c':
        sub_cats = SubCategory.objects.get(pk=pk)
        product_list = sub_cats.product_set.all()
    elif p_or_c == 'p':
        product_list = []
        categories = Category.objects.get(pk=pk)
        sub_cats = categories.sub_cat.all()
        for sub_cat in sub_cats:
            product = sub_cat.product_set.all()
            product_list += product
    else:
        product_list = []
    return render(request, 'ecom/product_list.html', {'product_list': product_list})


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
            if order.cart_products.count() == 0:
                order.delete()
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
            html_content = render_to_string('ecom/email_template.html',
                                            {'name': self.request.user.first_name,
                                             'orderNum': order.id})
            if form.is_valid():
                customer_name = form.cleaned_data.get('customer_name')
                contact_no = form.cleaned_data.get('contact_no')
                street_address = form.cleaned_data.get('street_address')
                country = form.cleaned_data.get('country')
                zip = form.cleaned_data.get('zip')
                payment = form.cleaned_data.get('payment')
                billing = Address(
                    user=self.request.user,
                    customer_name=customer_name,
                    contact_no=contact_no,
                    street_address=street_address,
                    country=country,
                    zip=zip,
                )
                billing.save()
                order.order_address = billing
                if payment == 'c':
                    order.order_status = True
                    order.save()
                    text_content = strip_tags(html_content)
                    subject = 'Hi, ' + self.request.user.first_name + ',' + 'ORDER PLACED SUCCESSFULLY!!',
                    order_mail = EmailMultiAlternatives(
                        subject,
                        text_content,
                        settings.EMAIL_HOST_USER,
                        ['rahamanhabib2802@gmail.com']
                    )
                    order_mail.attach_alternative(html_content, "text/html")
                    order_mail.send()
                    messages.info(self.request, 'YOUR ORDER HAS BEEN PLACED')
                    return redirect('products:product_list')
                else:
                    messages.info(self.request, 'Invalid')
                    return redirect('products:checkout')
            else:
                messages.info(self.request, 'Invalid')
                return redirect('products:checkout')
        except:
            messages.warning(self.request, 'Invalid')
            return redirect('products:cart')
