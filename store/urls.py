from django.urls import path

from .views import *

app_name = "store"

urlpatterns = [
    path("products/", ProductListView.as_view(), name="all_products"),
    path("products/top/", TopProductListView.as_view(), name="top_products"),
    path("products/create/", CreateProductView.as_view(), name="create_product"),
    path(
        "products/upload/",
        UploadProductImageView.as_view(),
        name="upload_product_image",
    ),
    path("categories/", CategoryListView.as_view(), name="all_top_level_categories"),
    path("orders/", GetOrdersView.as_view(), name="get_all_orders_list"),
    path("orders/history/", GetOrderHistoryView.as_view(), name="get_order_history"),
    path(
        "products/<str:pk>/reviews/",
        CreateProductReviewView.as_view(),
        name="create_product_review",
    ),
    path("products/<slug:slug>/", ProductView.as_view(), name="get_individual_product"),
    path(
        "products/delete/<str:pk>/",
        DeleteProductView.as_view(),
        name="delete_product_by_id",
    ),
    path(
        "products/update/<str:pk>/",
        UpdateProductView.as_view(),
        name="update_product_by_id",
    ),
    path(
        "categories/<slug:slug>/",
        CategoryItemView.as_view(),
        name="get_products_by_category",
    ),
    path("orders/add/", AddOrderItemsView.as_view(), name="add_order_items"),
    path("orders/<str:pk>/", GetOrderByIdView.as_view(), name="get_order_by_id"),
    path(
        "orders/<str:pk>/pay/",
        UpdateOrderToPaidView.as_view(),
        name="update_order_to_paid",
    ),
    path(
        "orders/<str:pk>/deliver/",
        UpdateOrderToDeliveredView.as_view(),
        name="update_order_to_delivered",
    ),
]
