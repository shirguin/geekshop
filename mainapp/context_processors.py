from basketapp.models import Basket


def basket(request):
    basket_items = []
    if request.user.is_authenticated:
        # basket_items = Basket.objects.filter(user=request.user)
        basket_items = request.user.basket.select_related()
    return {
        'basket': basket_items
    }
