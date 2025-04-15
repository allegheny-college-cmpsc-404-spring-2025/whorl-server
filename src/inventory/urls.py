from django.urls import path
from .views import (
    AddInventoryView,
    ReduceInventoryView,
    ListInventoryView,
    SearchInventoryView,
    GiveInventoryView,
    BackpackAddItemView,
    BackpackRemoveItemView,
    BackpackListContentsView,
)
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="Inventory API",
        default_version='v1',
        description="API documentation for the Termunda Inventory service.",
        contact=openapi.Contact(email="dluman@allegheny.edu"),
        license=openapi.License(name="CC0"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

app_name = 'inventory'

urlpatterns = [
    path('add/', AddInventoryView.as_view(), name='inventory-add'),
    path('reduce/', ReduceInventoryView.as_view(), name='inventory-reduce'),
    path('list/', ListInventoryView.as_view(), name='inventory-list'),
    path('search/', SearchInventoryView.as_view(), name='inventory-search'),
    path('transfer/<str:to_charname>/', GiveInventoryView.as_view(), name='inventory-transfer'),
    path('backpack/add/', BackpackAddItemView.as_view(), name='backpack-add'),
    path('backpack/remove/', BackpackRemoveItemView.as_view(), name='backpack-remove'),
    path('backpack/contents/', BackpackListContentsView.as_view(), name='backpack-contents'),
    path('docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]
