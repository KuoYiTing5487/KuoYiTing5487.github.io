from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.core.files.storage import FileSystemStorage
from .forms import ProductForm, RawProductForm
from .models import Product
from partners.forms import CartForm
from partners.models import Cart

# Create your views here.


def product_list_view(request):
    queryset = Product.objects.all()  # list of objects
    context = {
        "object_list": queryset
    }
    return render(request, "products/product_list.html", context)


def product_delete_view(request, p_id):
    obj = get_object_or_404(Product, id=p_id)
    if request.method == "POST":
        obj.delete()
        return redirect('../../')
    context = {
        "object": obj
    }
    return render(request, "products/product_delete.html", context)


def product_create_view(request):
    form = ProductForm(request.POST or None)  # request.FILES
    if form.is_valid():
        form.save()
        return redirect('../')
    context = {
        'state': "新增商品",
        'form': form
    }
    return render(request, "products/product_create.html", context)


def product_detail_view(request, p_id):
    obj = get_object_or_404(Product, id=p_id)  # obj = Product.objects.get(id=p_id)
    form = CartForm(request.POST or None)
    cart_queryset = Cart.objects.filter(account=request.user.id)

    if form.is_valid():  # 我的最愛
        instance = form.save(commit=False)
        instance.account = request.user
        instance.product = obj
        instance.save()

    context = {
        'form': form,
        'object': obj,
        "cart": cart_queryset,
    }
    return render(request, "products/product_detail.html", context)


def cart_delete_view(request, p_id):
    obj = Cart.objects.get(product=p_id, account=request.user.id)
    # if request.method == "POST":
    obj.delete()
    return redirect('../')


def product_update_view(request, p_id):
    obj = get_object_or_404(Product, id=p_id)
    form = ProductForm(request.POST or None, instance=obj)  # , request.FILES
    if request.method == "POST":
        if form.is_valid():
            form.save()
            return redirect('../')
    context = {
        'state': "更新商品",
        'form': form
    }
    return render(request, "products/product_create.html", context)


def product_all_view(request, *args, **kwargs):
    queryset = Product.objects.all()  # list of objects
    cart_queryset = Cart.objects.filter(account=request.user.id)
    form = CartForm(request.POST or None)
    context = {
        "object_list": queryset,
        "cart": cart_queryset,
        "times": 0,
        "form": form,
    }
    return render(request, "products/product_all.html", context)


def wear_a_ring(request, p_id):
    obj = get_object_or_404(Product, id=p_id)
    queryset = Product.objects.all()
    context = {
        "object_list": queryset,
        "object": obj,
    }
    return render(request, "3D_model/3d_js.html", context)

