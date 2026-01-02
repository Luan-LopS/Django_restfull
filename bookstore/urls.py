import debug_toolbar
from django.contrib import admin
from django.urls import path, re_path, include
from rest_framework.authtoken.views import obtain_auth_token
from bookstore import views
from django.conf import settings
import sys

urlpatterns = [
    path("admin/", admin.site.urls),
    re_path(r"^bookstore/(?P<version>(v1|v2))/", include("order.urls")),
    re_path(r"^bookstore/(?P<version>(v1|v2))/", include("product.urls")),
    path("api-token-auth/", obtain_auth_token, name="api_token_auth"),
    path("update_server/", views.update, name="update"),
    path("hello/", views.hello_world, name="hello_word"),
]

if settings.DEBUG and "test" not in sys.argv:
    urlpatterns = [
        path("__debug__/", include(debug_toolbar.urls))
        ] + urlpatterns
