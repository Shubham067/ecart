# Generated by Django 3.2.6 on 2021-09-03 08:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import mptt.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, help_text='Required and Unique', max_length=255, unique=True, verbose_name='Category Name')),
                ('slug', models.SlugField(max_length=255, unique=True, verbose_name='Category Safe URL')),
                ('is_active', models.BooleanField(default=True, help_text='Modify Category Visibility', verbose_name='Category Visibility')),
                ('lft', models.PositiveIntegerField(editable=False)),
                ('rght', models.PositiveIntegerField(editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(editable=False)),
                ('parent', mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='store.category')),
            ],
            options={
                'verbose_name': 'Category',
                'verbose_name_plural': 'Categories',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(help_text='Required', max_length=255, verbose_name='Title')),
                ('description', models.TextField(blank=True, help_text='Not Required', verbose_name='Description')),
                ('slug', models.SlugField(max_length=255, unique=True, verbose_name='Product Safe URL')),
                ('regular_price', models.DecimalField(decimal_places=2, help_text='Required', max_digits=5, verbose_name='Regular Price')),
                ('discount_price', models.DecimalField(decimal_places=2, help_text='Required', max_digits=5, verbose_name='Discount Price')),
                ('in_stock', models.BooleanField(default=True, help_text='Modify Product Availability', verbose_name='Product Availability')),
                ('is_active', models.BooleanField(default=True, help_text='Modify Product Visibility', verbose_name='Product Visibility')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Product Created At Timestamp')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Product Updated At Timestamp')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product', to='store.category')),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_creator', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Product',
                'verbose_name_plural': 'Products',
                'ordering': ('-created_at',),
            },
        ),
        migrations.CreateModel(
            name='ProductSpecification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, help_text='Required and Unique', max_length=255, unique=True, verbose_name='Product Specification Name')),
            ],
            options={
                'verbose_name': 'Product Specification',
                'verbose_name_plural': 'Product Specifications',
            },
        ),
        migrations.CreateModel(
            name='ProductType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, help_text='Required and Unique', max_length=255, unique=True, verbose_name='Product Type Name')),
                ('is_active', models.BooleanField(default=True, help_text='Modify Product Type Visibility', verbose_name='Product Type Visibility')),
            ],
            options={
                'verbose_name': 'Product Type',
                'verbose_name_plural': 'Product Types',
            },
        ),
        migrations.CreateModel(
            name='ProductSpecificationValue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(help_text='Product Specification Value (maximum 255 words)', max_length=255, verbose_name='Value')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.product')),
                ('specification', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='store.productspecification')),
            ],
            options={
                'verbose_name': 'Product Specification Value',
                'verbose_name_plural': 'Product Specification Values',
            },
        ),
        migrations.AddField(
            model_name='productspecification',
            name='product_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='store.producttype'),
        ),
        migrations.CreateModel(
            name='ProductImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(default='images/default.png', help_text='Upload a product image', upload_to='images/', verbose_name='Image')),
                ('alt_text', models.CharField(blank=True, help_text='Please add alternative text', max_length=255, null=True, verbose_name='Alternate Text')),
                ('is_feature', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Product Image Created At Timestamp')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Product Image Updated At Timestamp')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_image', to='store.product')),
            ],
            options={
                'verbose_name': 'Product Image',
                'verbose_name_plural': 'Product Images',
                'ordering': ('created_at',),
            },
        ),
        migrations.AddField(
            model_name='product',
            name='product_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='store.producttype'),
        ),
    ]