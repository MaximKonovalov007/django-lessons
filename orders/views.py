from django.shortcuts import render
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from .models import *
from .forms import CheckoutProductForm
from django.contrib.auth.models import User


def basket_adding(request):
    return_dict = dict()
    session_key = request.session.session_key
    print(request.POST)
    data =request.POST
    product_id = data.get("product_id")
    nmb = float(data.get("nmb"))
    is_delete = data.get("is_delete")

    if is_delete == "true":
         ProductInBasket.objects.filter(id=product_id).update(is_active=False)
    else:
        new_product, created = ProductInBasket.objects.get_or_create(session_key=session_key, product_id=product_id,
                                                                     is_active=True, defaults={"nmb": nmb})
        if not created:
            print(new_product.nmb)
            print(nmb)
            new_product.nmb += nmb
            new_product.save(force_update=True)

    #common code for 2 cases

    products_in_basket = ProductInBasket.objects.filter(session_key=session_key, is_active=True)
    product_total_nmb = ProductInBasket.objects.filter(session_key=session_key, is_active=True).count()
    return_dict["product_total_nmb"] = product_total_nmb
    return_dict["products"] = list()

    for item in products_in_basket:
        product_dict = dict()
        product_dict["id"] = item.id
        product_dict["name"] = item.product.name
        product_dict["price_per_item"] = item.price_per_item
        product_dict["nmb"] = item.nmb
        return_dict["products"].append(product_dict)

    return JsonResponse(return_dict)


def checkout(request):
    session_key = request.session.session_key
    products_in_order = ProductInBasket.objects.filter(session_key=session_key, is_active=True)
    form = CheckoutProductForm(request.POST or None)
    if form.is_valid():
        data = request.POST
        name = data.get("name")
        phone = data.get("phone")

        user, created = User.objects.get_or_create(username=phone, defaults={"first_name": name})

        order = Order.objects.create(user=user, customer_name=name, customer_phone=phone, status_id=1)

        for name, value in data.items():
            if name.startswith("product_in_basket_"):
                products_in_basket_id = name.split("product_in_basket_")[1]
                products_in_basket = ProductInBasket.objects.get(id=products_in_basket_id)

                products_in_basket.nmb = int(value)
                products_in_basket.save(force_update=True)

                ProductInOrder.objects.create(product=products_in_basket.product, count=products_in_basket.nmb, amount_per_item=products_in_basket.price_per_item, order=order, total_amount=products_in_basket.total_price)


        return HttpResponseRedirect(request.META['HTTP_REFERER'])
    else:
        print("no")
    return render(request, "orders/checkout.html", locals())


