from django.conf import settings
from django.db import models
from django.utils.functional import cached_property

from mainapp.models import Product


# менеджер объектов
# class BasketQuerySet(models.QuerySet):
#
#     def delete(self, *args, **kwargs):
#         for item in self:
#             item.product.quantity += item.quantity
#             item.product.save()
#         super().delete(*args, **kwargs)


class Basket(models.Model):
    # работа через менеджер объектов
    # objects = BasketQuerySet.as_manager()

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='basket')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity =models.PositiveSmallIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def product_cost(self):
        return self.product.price * self.quantity

    @cached_property
    def get_items_cached(self):
        return self.user.basket.select_related()

    @property
    def total_quantity(self):
        # items = Basket.objects.filter(user=self.user)
        items = self.get_items_cached
        _total_quantity = sum(list(map(lambda x: x.quantity, items)))
        return _total_quantity

    @property
    def total_cost(self):
        # items = Basket.objects.filter(user=self.user)
        items = self.get_items_cached
        _total_cost = sum(list(map(lambda x: x.product_cost, items)))
        return _total_cost

    # работа через менеджер объектов
    # def delete(self, *args, **kwargs):
    #
    #     self.product.quantity += self.quantity
    #     self.product.save()
    #
    #     super().delete(*args, **kwargs)

    @staticmethod
    def get_item(pk):
        return Basket.objects.get(pk=pk)
