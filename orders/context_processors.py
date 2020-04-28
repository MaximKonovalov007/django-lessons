from .models import ProductInBasket


def getting_basket_info(request):
    session_key = request.session.session_key

    if not session_key:
        request.session.cycle_key()

    products_total_nmb = ProductInBasket.objects.filter(session_key=session_key, is_active=True).count()
    products_in_basket = ProductInBasket.objects.filter(session_key=session_key, is_active=True)

    for product_in_basket in products_in_basket:
        print(product_in_basket)


    return locals()