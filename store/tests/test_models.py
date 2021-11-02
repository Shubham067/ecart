from datetime import datetime

from django.utils import timezone
from django.urls import reverse
from django.test import TestCase
from django.contrib.auth.models import User

from django_seed import Seed

from rest_framework.test import APITestCase

from store.models import Category, Product, ProductType

seeder = Seed.seeder()


class TestCategoriesModel(TestCase):
    def setUp(self):
        self.data1 = Category.objects.create(
            name="django", slug="django", is_active=True
        )

    def test_category_model_entry(self):
        """
        Test Category Model data insertion/types/field attributes
        """
        data = self.data1
        self.assertTrue(isinstance(data, Category))

    def test_category_model_entry(self):
        """
        Test Category Model default name
        """
        data = self.data1
        self.assertEqual(str(data), "django")


class TestProductsModel(TestCase):
    def setUp(self):
        Category.objects.create(name="django", slug="django", is_active=True)
        User.objects.create(username="admin")
        ProductType.objects.create(name="book")
        self.data1 = Product.objects.create(
            product_type_id=6,
            category_id=7,
            title="django stars",
            created_by_id=2,
            slug="django-stars",
            regular_price="20.99",
            discount_price="10.99",
            created_at=datetime.now(tz=timezone.utc),
            updated_at=datetime.now(tz=timezone.utc),
        )

    def test_product_model_entry(self):
        """
        Test Product Model data insertion/types/field attributes
        """
        data = self.data1
        self.assertTrue(isinstance(data, Product))
        self.assertEqual(str(data), "django stars")


class ProductsTestCase(APITestCase):
    def test_list_products(self):
        # Add dummy data to the Category and Product Table
        seeder.add_entity(Category, 5)
        seeder.add_entity(ProductType, 5)
        seeder.add_entity(User, 1)
        seeder.add_entity(Product, 10)
        seeder.execute()

        # We expect the result in 4 queries
        with self.assertNumQueries(4):
            response = self.client.get(reverse("store:all_products"), format="json")
