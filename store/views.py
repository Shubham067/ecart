from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Prefetch

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework_simplejwt.authentication import JWTAuthentication

from .serializers import *
from .models import *
from . import models

from datetime import datetime


class ProductListView(APIView):
    """Get a list of all active products."""

    permission_classes = (AllowAny,)
    serializer_class = ProductSerializer

    def get(self, request):
        products = (
            Product.objects.filter(is_active=True)
            .select_related("product_type", "category", "created_by")
            .prefetch_related(
                "product_image", Prefetch("review_set", to_attr="reviews")
            )
        )

        page = request.query_params.get("page")

        paginator = Paginator(products, 2)

        try:
            products = paginator.page(page)
        except PageNotAnInteger:
            products = paginator.page(1)
        except EmptyPage:
            products = paginator.page(paginator.num_pages)

        if page == None:
            page = 1

        page = int(page)

        serializer = self.serializer_class(
            products, many=True, context={"request": request}
        )
        return Response(
            {
                "products": serializer.data,
                "page": page,
                "pages": paginator.num_pages,
                "status": status.HTTP_200_OK,
            },
            status=status.HTTP_200_OK,
        )


class TopProductListView(APIView):
    """Get a list of top 5 active products."""

    permission_classes = (AllowAny,)
    serializer_class = ProductSerializer

    def get(self, request):
        products = Product.objects.filter(is_active=True, rating__gte=3).order_by(
            "-rating"
        )[0:5]

        serializer = self.serializer_class(
            products, many=True, context={"request": request}
        )
        return Response(
            {"products": serializer.data, "status": status.HTTP_200_OK},
            status=status.HTTP_200_OK,
        )


# class ProductListView(generics.ListAPIView):
#     queryset = Product.objects.all()
#     permission_classes = (AllowAny,)
#     serializer_class = ProductSerializer


class ProductView(generics.RetrieveAPIView):
    """Get individual product details based on slug."""

    lookup_field = "slug"
    queryset = Product.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = ProductSerializer


class CategoryItemView(generics.ListAPIView):
    """Get individual category details based on slug."""

    permission_classes = (AllowAny,)
    serializer_class = ProductSerializer

    def get_queryset(self):
        return models.Product.objects.filter(
            category__in=Category.objects.get(slug=self.kwargs["slug"]).get_descendants(
                include_self=True
            )
        )


class CategoryListView(generics.ListAPIView):
    """Get a list of categories."""

    queryset = Category.objects.filter(level=1)
    permission_classes = (AllowAny,)
    serializer_class = CategorySerializer


class AddOrderItemsView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = OrderSerializer

    def post(self, request):
        user = request.user
        data = request.data

        orderItems = data["orderItems"]

        if orderItems and len(orderItems) == 0:
            Response(
                {"detail": "No Order Items", "status": status.HTTP_400_BAD_REQUEST}
            )
        else:
            # Create Order
            order = Order.objects.create(
                created_by=user,
                transaction_id=data.get("transactionId", user.id),
                payment_method=data["paymentMethod"],
                tax=data["tax"],
                shipping_charge=data["shippingCharge"],
            )

            # Create Shipping Address
            shipping = ShippingAddress.objects.create(
                order=order,
                customer=user,
                name=data["shippingAddress"]["name"],
                address=data["shippingAddress"]["address"],
                city=data["shippingAddress"]["city"],
                state=data["shippingAddress"]["state"],
                zipcode=data["shippingAddress"]["zipcode"],
                country=data["shippingAddress"]["country"],
                shipping_charge=data["shippingCharge"],
            )

            # Create Order Items from "orderItems" list
            for item in orderItems:
                product = Product.objects.get(id=item["product"])

                order_item = OrderItem.objects.create(
                    product=product, order=order, quantity=item["qty"]
                )

                # Update Stock
                product.count_in_stock -= order_item.quantity
                product.save()
        serializer = self.serializer_class(order, many=False)
        return Response({"order": serializer.data, "status": status.HTTP_200_OK})


class GetOrderHistoryView(APIView):
    """Get a list of orders created by a particular user."""

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = OrderSerializer

    def get(self, request):
        user = request.user
        orders = user.order_creator
        serializer = self.serializer_class(
            orders, many=True, context={"request": request}
        )

        return Response(
            {"orders": serializer.data, "status": status.HTTP_200_OK},
            status=status.HTTP_200_OK,
        )


class GetOrderByIdView(APIView):
    """Get order details by id for a particular user."""

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = OrderSerializer

    def get(self, request, pk):
        user = request.user

        try:
            order = Order.objects.get(id=pk)
            if user.is_staff or order.created_by == user:
                serializer = self.serializer_class(
                    order, many=False, context={"request": request}
                )
                return Response(
                    {"order": serializer.data, "status": status.HTTP_200_OK},
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    {
                        "detail": "Not authorized to view this order!",
                        "status": status.HTTP_400_BAD_REQUEST,
                    }
                )
        except:
            return Response(
                {
                    "detail": "Order does not exist!",
                    "status": status.HTTP_400_BAD_REQUEST,
                }
            )


class UpdateOrderToPaidView(APIView):
    """Update 'is_paid' status of a particular order."""

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def put(self, request, pk):
        order = Order.objects.get(id=pk)

        order.is_paid = True
        order.paid_at = datetime.now()
        order.save()

        return Response(
            {"detail": "Order was paid successfully", "status": status.HTTP_200_OK},
            status=status.HTTP_200_OK,
        )


class UpdateOrderToDeliveredView(APIView):
    """Update 'is_delivered' status of a particular order."""

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser]

    def put(self, request, pk):
        order = Order.objects.get(id=pk)

        order.is_delivered = True
        order.delivered_at = datetime.now()
        order.save()

        return Response(
            {
                "detail": "Order was delivered successfully",
                "status": status.HTTP_200_OK,
            },
            status=status.HTTP_200_OK,
        )


class DeleteProductView(APIView):
    """Delete a particular product by id."""

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser]

    def delete(self, request, pk):

        productToDelete = Product.objects.get(id=pk)
        productToDelete.delete()

        return Response(
            {
                "detail": "Product got deleted successfully",
                "status": status.HTTP_200_OK,
            },
            status=status.HTTP_200_OK,
        )


class CreateProductView(APIView):
    """Create a new product."""

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser]
    serializer_class = ProductSerializer

    def post(self, request):
        user = request.user

        product = Product.objects.create(
            product_type=ProductType.objects.get(id=1),
            category=Category.objects.get(id=1),
            created_by=user,
            title="New Product",
            brand="Generic",
            description="description",
            slug="slug" + str(datetime.now()).split(".")[1],
            regular_price="899.00",
            discount_price="499.00",
        )

        ProductImage.objects.create(product=product)

        serializer = self.serializer_class(product, many=False)

        return Response(
            {
                "product": serializer.data,
                "status": status.HTTP_200_OK,
            },
            status=status.HTTP_200_OK,
        )


class UpdateProductView(APIView):
    """Update a particular product details by id."""

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser]
    serializer_class = ProductSerializer

    def put(self, request, pk):
        data = request.data

        product = Product.objects.get(id=pk)

        product.title = data["title"]
        product.brand = data["brand"]
        product.description = data["description"]
        product.slug = data["slug"]
        product.regular_price = data["regular_price"]
        product.discount_price = data["discount_price"]
        product.count_in_stock = data["count_in_stock"]

        product.save()

        serializer = self.serializer_class(product, many=False)

        return Response(
            {
                "product": serializer.data,
                "status": status.HTTP_200_OK,
            },
            status=status.HTTP_200_OK,
        )


class UploadProductImageView(APIView):
    """Upload product image."""

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser]

    def post(self, request):
        data = request.data

        product_id = data["id"]

        product = Product.objects.get(id=product_id)

        ProductImage.objects.create(
            product=product,
            image=request.FILES.get("image"),
            alt_text=product.title,
            is_feature=data["is_feature"],
        )

        return Response(
            {
                "detail": "Product image got uploaded successfully",
                "status": status.HTTP_200_OK,
            },
            status=status.HTTP_200_OK,
        )


class GetOrdersView(APIView):
    """Get a list of all orders."""

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser]
    serializer_class = OrderSerializer

    def get(self, request):
        orders = Order.objects.all()
        serializer = self.serializer_class(
            orders, many=True, context={"request": request}
        )

        return Response(
            {"orders": serializer.data, "status": status.HTTP_200_OK},
            status=status.HTTP_200_OK,
        )


class CreateProductReviewView(APIView):
    """Create a review for a particular product."""

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        user = request.user
        data = request.data

        product = Product.objects.get(id=pk)

        alreadyExists = product.review_set.filter(created_by=user).exists()

        if alreadyExists:
            return Response(
                {
                    "detail": "Product review has already been submitted!",
                    "status": status.HTTP_400_BAD_REQUEST,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        elif data["rating"] == 0:
            return Response(
                {
                    "detail": "Please select product rating!",
                    "status": status.HTTP_400_BAD_REQUEST,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        else:
            review = Review.objects.create(
                product=product,
                created_by=user,
                name=user.first_name,
                rating=data["rating"],
                comment=data["comment"],
            )

            reviews = product.review_set.all()
            product.num_reviews = len(reviews)

            total_rating = 0
            for i in reviews:
                total_rating += i.rating

            product.rating = total_rating / len(reviews)
            product.save()

            return Response(
                {
                    "detail": "Product review got added successfully",
                    "status": status.HTTP_200_OK,
                },
                status=status.HTTP_200_OK,
            )
