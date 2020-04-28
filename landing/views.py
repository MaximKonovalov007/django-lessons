from django.shortcuts import render
import datetime
from .forms import SubscriberForm
from products.models import *

def landing(request):
    current_date = datetime.date.today()
    form = SubscriberForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        print(request.POST)
        data = form.cleaned_data
        print(data['name'])

        form.save()

    return render(request, 'landing/landing.html', locals())


def home(request):
    products_images = ProductImage.objects.filter(is_active=True, is_main=True)
    products_images_phones = ProductImage.objects.filter(is_active=True, is_main=True, product__category__id=1)
    products_images_laptops = ProductImage.objects.filter(is_active=True, is_main=True, product__category__id=3)
    products_images_computers = ProductImage.objects.filter(is_active=True, is_main=True, product__category__id=2)
    return render(request, 'landing/home.html', locals())



