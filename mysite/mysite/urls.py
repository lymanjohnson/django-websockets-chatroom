from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("chat/", include(("chat.urls", 'chat'))),
    path("admin/", admin.site.urls),
]