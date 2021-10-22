from django.test import TestCase
from django.contrib.auth.models import User

from store.models import Category, Product, ProductType


class TestCategoriesModel(TestCase):

    def setUp(self):
        self.data1 = Category.objects.create(name = 'django', slug = 'django', is_active = True)

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
        self.assertEqual(str(data), 'django')

    
class TestProductsModel(TestCase):

    def setUp(self):
        Category.objects.create(name = 'django', slug = 'django', is_active = True)
        User.objects.create(username = 'admin')
        ProductType.objects.create(name = 'book')
        self.data1 = Product.objects.create(product_type_id = 1, category_id = 1, title = 'django stars', created_by_id = 1,
                                            slug = 'django-stars', regular_price = '20.99', discount_price = '10.99')
        
    def test_product_model_entry(self):
        """
        Test Product Model data insertion/types/field attributes
        """
        data = self.data1
        self.assertTrue(isinstance(data, Product))
        self.assertEqual(str(data), 'django stars')
