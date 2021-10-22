from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class Category(MPTTModel):
    """
    The Category table implimented using MPTT.
    """

    name = models.CharField(
        verbose_name=_("Category Name"),
        help_text=_("Required and Unique"),
        max_length=255,
        db_index=True,
        unique=True,
    )
    slug = models.SlugField(
        verbose_name=_("Category Safe URL"), max_length=255, unique=True
    )
    parent = TreeForeignKey(
        "self", on_delete=models.CASCADE, null=True, blank=True, related_name="children"
    )
    is_active = models.BooleanField(
        verbose_name=_("Category Visibility"),
        help_text=_("Modify Category Visibility"),
        default=True,
    )

    class MPTTMeta:
        order_insertion_by = ["name"]

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")

    def get_absolute_url(self):
        return reverse("store:category_list", kwargs={"pk": self.pk})

    def __str__(self):
        return self.name


class ProductType(models.Model):
    """
    The Product Type table will provide the list of different types of
    products available for sale.
    """

    name = models.CharField(
        verbose_name=_("Product Type Name"),
        help_text=_("Required and Unique"),
        max_length=255,
        db_index=True,
        unique=True,
    )
    is_active = models.BooleanField(
        verbose_name=_("Product Type Visibility"),
        help_text=_("Modify Product Type Visibility"),
        default=True,
    )

    class Meta:
        verbose_name = _("Product Type")
        verbose_name_plural = _("Product Types")

    def __str__(self):
        return self.name


class ProductSpecification(models.Model):
    """
    The Product Specification table contains product specification/features
    for the product types.
    """

    product_type = models.ForeignKey(ProductType, on_delete=models.RESTRICT)
    name = models.CharField(
        verbose_name=_("Product Specification Name"),
        help_text=_("Required and Unique"),
        max_length=255,
        db_index=True,
        unique=True,
    )

    class Meta:
        verbose_name = _("Product Specification")
        verbose_name_plural = _("Product Specifications")

    def __str__(self):
        return self.name


class Product(models.Model):
    """
    The Product table containing all products.
    """

    product_type = models.ForeignKey(ProductType, on_delete=models.RESTRICT)
    category = models.ForeignKey(
        Category, related_name="product", on_delete=models.CASCADE
    )
    created_by = models.ForeignKey(
        User, related_name="product_creator", on_delete=models.CASCADE
    )
    title = models.CharField(
        verbose_name=_("Title"), help_text=_("Required"), max_length=255
    )
    brand = models.CharField(
        verbose_name=_("Brand"),
        help_text=_("Not Required"),
        max_length=255,
        null=True,
        blank=True,
    )
    description = models.TextField(
        verbose_name=_("Description"), help_text=_("Not Required"), blank=True
    )
    slug = models.SlugField(
        verbose_name=_("Product Safe URL"), max_length=255, unique=True
    )
    regular_price = models.DecimalField(
        verbose_name=_("Regular Price"),
        help_text=_("Required"),
        max_digits=7,
        decimal_places=2,
    )
    discount_price = models.DecimalField(
        verbose_name=_("Discount Price"),
        help_text=_("Required"),
        max_digits=7,
        decimal_places=2,
    )
    rating = models.DecimalField(
        verbose_name=_("Rating"),
        help_text=_("Product Rating"),
        max_digits=7,
        decimal_places=2,
        null=True,
        blank=True,
    )
    num_reviews = models.IntegerField(
        verbose_name=_("Number Of Reviews"),
        help_text=_("Total Number Of Product Reviews"),
        null=True,
        blank=True,
        default=0,
    )
    count_in_stock = models.IntegerField(
        verbose_name=_("Product Count In Stock"),
        help_text=_("Total Number Of Product in Stock"),
        null=True,
        blank=True,
        default=0,
    )
    in_stock = models.BooleanField(
        verbose_name=_("Product Availability"),
        help_text=_("Modify Product Availability"),
        default=True,
    )
    is_active = models.BooleanField(
        verbose_name=_("Product Visibility"),
        help_text=_("Modify Product Visibility"),
        default=True,
    )
    created_at = models.DateTimeField(
        verbose_name=_("Product Created At Timestamp"),
        auto_now_add=True,
        editable=False,
    )
    updated_at = models.DateTimeField(
        verbose_name=_("Product Updated At Timestamp"), auto_now=True
    )

    class Meta:
        verbose_name = _("Product")
        verbose_name_plural = _("Products")
        ordering = ("-created_at",)

    def get_absolute_url(self):
        return reverse("store:product_detail", args=[self.slug])

    def __str__(self):
        return self.title


class ProductSpecificationValue(models.Model):
    """
    The Product Specification Value table contains each of the products'
    individual specification/features.
    """

    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    specification = models.ForeignKey(ProductSpecification, on_delete=models.RESTRICT)
    value = models.CharField(
        verbose_name=_("Value"),
        help_text=_("Product Specification Value (maximum 255 words)"),
        max_length=255,
    )

    class Meta:
        verbose_name = _("Product Specification Value")
        verbose_name_plural = _("Product Specification Values")

    def __str__(self):
        return self.value


class ProductImage(models.Model):
    """
    The Product Images table.
    """

    product = models.ForeignKey(
        Product, related_name="product_image", on_delete=models.CASCADE
    )
    image = models.ImageField(
        verbose_name=_("Image"),
        help_text=_("Upload a product image"),
        upload_to="images/",
        default="images/default.png",
    )
    alt_text = models.CharField(
        verbose_name=_("Alternate Text"),
        help_text=_("Please add alternative text"),
        null=True,
        blank=True,
        max_length=255,
    )
    is_feature = models.BooleanField(default=False)
    created_at = models.DateTimeField(
        verbose_name=_("Product Image Created At Timestamp"),
        auto_now_add=True,
        editable=False,
    )
    updated_at = models.DateTimeField(
        verbose_name=_("Product Image Updated At Timestamp"), auto_now=True
    )

    class Meta:
        verbose_name = _("Product Image")
        verbose_name_plural = _("Product Images")
        ordering = ("created_at",)


class Review(models.Model):
    """
    The Product Reviews table.
    """

    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    created_by = models.ForeignKey(
        User, related_name="review_creator", on_delete=models.CASCADE
    )
    name = models.CharField(
        verbose_name=_("User Name"),
        help_text=_("Not Required"),
        max_length=255,
        null=True,
        blank=True,
    )
    rating = models.DecimalField(
        verbose_name=_("Rating"),
        help_text=_("Product Rating"),
        max_digits=7,
        decimal_places=2,
        null=True,
        blank=True,
    )
    comment = models.TextField(
        verbose_name=_("Comment"), help_text=_("Not Required"), blank=True, null=True
    )
    created_at = models.DateTimeField(
        verbose_name=_("Review Created At Timestamp"),
        auto_now_add=True,
        editable=False,
    )
    updated_at = models.DateTimeField(
        verbose_name=_("Review Updated At Timestamp"), auto_now=True
    )

    class Meta:
        verbose_name = _("Product Review")
        verbose_name_plural = _("Product Reviews")
        ordering = ("created_at",)

    def __str__(self):
        return str(self.rating)


class Order(models.Model):
    """
    The Product Order Table.
    """

    created_by = models.ForeignKey(
        User, related_name="order_creator", on_delete=models.CASCADE
    )
    transaction_id = models.CharField(
        verbose_name=_("Transaction Id"),
        help_text=_("Required"),
        max_length=255,
        null=True,
    )
    payment_method = models.CharField(
        verbose_name=_("Payment Method"),
        help_text=_("Not Required"),
        max_length=255,
        null=True,
        blank=True,
    )
    tax = models.DecimalField(
        verbose_name=_("Tax"),
        help_text=_("Total Tax Charged For Order"),
        max_digits=7,
        decimal_places=2,
        null=True,
        blank=True,
    )
    shipping_charge = models.DecimalField(
        verbose_name=_("Shipping Charge"),
        help_text=_("Total Shipping Charge For Order"),
        max_digits=7,
        decimal_places=2,
        null=True,
        blank=True,
    )
    is_paid = models.BooleanField(
        verbose_name=_("Order Amount Paid Status"),
        help_text=_("Is Order Amount Paid By User"),
        default=False,
    )
    is_delivered = models.BooleanField(
        verbose_name=_("Order Delivery Status"),
        help_text=_("Is Order Delivered To User"),
        default=False,
    )
    paid_at = models.DateTimeField(
        verbose_name=_("Order Amount Paid At Timestamp"),
        auto_now_add=False,
        null=True,
        blank=True,
    )
    delivered_at = models.DateTimeField(
        verbose_name=_("Order Delivered At Timestamp"),
        auto_now_add=False,
        null=True,
        blank=True,
    )
    created_at = models.DateTimeField(
        verbose_name=_("Order Created At Timestamp"),
        auto_now_add=True,
        editable=False,
    )

    @property
    def total_price(self):
        orderitems = self.orderitem_set.all()
        total_price = (
            sum([item.total_price for item in orderitems])
            + self.shipping_charge
            + self.tax
        )
        return total_price

    @property
    def total_items(self):
        orderitems = self.orderitem_set.all()
        total_items = sum([item.quantity for item in orderitems])
        return total_items

    class Meta:
        verbose_name = _("Order")
        verbose_name_plural = _("Orders")
        ordering = ("created_at",)

    def __str__(self):
        return str(self.id)


class OrderItem(models.Model):
    """
    The Order Items table.
    """

    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    quantity = models.IntegerField(
        verbose_name=_("Quantity Of Order Item"),
        help_text=_("Total Quantity Of Order Item"),
        null=True,
        blank=True,
        default=0,
    )
    created_at = models.DateTimeField(
        verbose_name=_("Order Item Created At Timestamp"),
        auto_now_add=True,
        editable=False,
    )

    @property
    def total_price(self):
        total_price = self.product.discount_price * self.quantity
        return total_price

    @property
    def name(self):
        name = self.product.title
        return name

    @property
    def price(self):
        price = self.product.discount_price
        return price

    @property
    def image(self):
        image = self.product.product_image.first().image.url
        return image

    @property
    def slug(self):
        slug = self.product.slug
        return slug

    @property
    def brand(self):
        brand = self.product.brand
        return brand

    class Meta:
        verbose_name = _("Order Item")
        verbose_name_plural = _("Order Items")
        ordering = ("created_at",)

    def __str__(self):
        return self.name


class ShippingAddress(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(
        verbose_name=_("Customer Name"),
        help_text=_("Not Required"),
        max_length=255,
        null=True,
        blank=True,
    )
    address = models.CharField(
        verbose_name=_("Shipping Address"),
        help_text=_("Required"),
        max_length=255,
    )
    city = models.CharField(
        verbose_name=_("City Name"),
        help_text=_("Required"),
        max_length=255,
    )
    state = models.CharField(
        verbose_name=_("State Name"),
        help_text=_("Required"),
        max_length=255,
    )
    zipcode = models.CharField(
        verbose_name=_("Postal Code"),
        help_text=_("Required"),
        max_length=255,
    )
    country = models.CharField(
        verbose_name=_("Country Name"),
        help_text=_("Required"),
        max_length=255,
    )
    shipping_charge = models.DecimalField(
        verbose_name=_("Shipping Charge"),
        help_text=_("Total Shipping Charge For Order"),
        max_digits=7,
        decimal_places=2,
        null=True,
        blank=True,
    )
    created_at = models.DateTimeField(
        verbose_name=_("Shipping Address Created At Timestamp"),
        auto_now_add=True,
        editable=False,
    )

    class Meta:
        verbose_name = _("Shipping Address")
        verbose_name_plural = _("Shipping Address")
        ordering = ("created_at",)

    def __str__(self):
        return self.address
