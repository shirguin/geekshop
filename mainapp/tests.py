from django.test import TestCase

from mainapp.models import ProductCategory, Product


class MainappSmokeTest(TestCase):
    status_code_success = 200

    def setUp(self) -> None:
        category = ProductCategory.objects.create(
            name='cat1'
        )
        for i in range(10):
            Product.objects.create(
                category=category,
                name=f'prod#{i}',
                description='qwe'
            )

    def test_mainapp_urls(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, self.status_code_success)

    def test_categories_urls(self):
        for cat in ProductCategory.objects.all():
            response = self.client.get(f'/products/{cat.pk}/')
            self.assertEqual(response.status_code, self.status_code_success)

    def test_products_urls(self):
        for prod in Product.objects.all():
            response = self.client.get(f'/products/product/{prod.pk}/')
            self.assertEqual(response.status_code, self.status_code_success)

    def tearDown(self) -> None:
        pass
