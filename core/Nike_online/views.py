from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required, permission_required
from .models import Product, Category, ProductImage
from .forms import ProductForm, ProductImageFormSet


def home(request):
    """Главная страница с избранными товарами и категориями"""
    featured_products = Product.objects.filter(stock_quantity__gt=0)[:4]
    categories = Category.objects.all()
    return render(request, 'nike_online/index.html', {
        'featured_products': featured_products,
        'categories': categories
    })


def product_list(request):
    """Список товаров с пагинацией"""
    product_list = Product.objects.filter(stock_quantity__gt=0).order_by('-created_at')
    paginator = Paginator(product_list, 12)  # 12 товаров на странице
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'nike_online/product_list.html', {
        'page_obj': page_obj,
        'categories': Category.objects.all()
    })


def product_detail(request, product_id):
    """Детальная страница товара с галереей изображений"""
    product = get_object_or_404(Product, pk=product_id)
    images = product.images.all()  # Получаем все изображения товара
    return render(request, 'nike_online/product_detail.html', {
        'product': product,
        'images': images
    })


@login_required
@permission_required('nike_online.change_product', raise_exception=True)
def edit_product(request, pk):
    """Редактирование товара с возможностью загрузки изображений"""
    product = get_object_or_404(Product, pk=pk)

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        formset = ProductImageFormSet(request.POST, request.FILES, instance=product)

        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            return redirect('product_detail', product_id=product.id)
    else:
        form = ProductForm(instance=product)
        formset = ProductImageFormSet(instance=product)

    return render(request, 'nike_online/edit_product.html', {
        'form': form,
        'formset': formset,
        'product': product
    })


@login_required
@permission_required('nike_online.add_product', raise_exception=True)
def add_product(request):
    """Добавление нового товара"""
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        formset = ProductImageFormSet(request.POST, request.FILES)

        if form.is_valid() and formset.is_valid():
            product = form.save()
            instances = formset.save(commit=False)
            for instance in instances:
                instance.product = product
                instance.save()
            return redirect('product_detail', product_id=product.id)
    else:
        form = ProductForm()
        formset = ProductImageFormSet()

    return render(request, 'nike_online/add_product.html', {
        'form': form,
        'formset': formset
    })