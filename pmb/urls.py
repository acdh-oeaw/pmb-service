from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("apis/", include("apis_core.urls", namespace="apis")),
    path("normdata/", include("normdata.urls", namespace="normdata")),
    path("admin/", admin.site.urls),
    path("arche/", include("archemd.urls", namespace="archemd")),
    path("", include("dumper.urls", namespace="dumper")),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
