from .models import Product


def index(request):
    products = Product.objects.all()
