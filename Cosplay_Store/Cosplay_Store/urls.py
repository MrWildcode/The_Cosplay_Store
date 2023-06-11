
from django.contrib import admin
from django.urls import path, re_path, include
from rest_framework.routers import SimpleRouter

from store.views import ProductsViewSet, oauth

router = SimpleRouter()

router.register(r'products', ProductsViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    re_path('', include('social_django.urls', namespace='social')),
    path('auth/', oauth)
]

urlpatterns += router.urls