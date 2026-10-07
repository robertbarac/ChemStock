from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("admin/", admin.site.urls),
    # Autenticación y recuperación de contraseñas de Django
    path("cuentas/", include("django.contrib.auth.urls")),
    # Atajos directos amigables
    path("login/", auth_views.LoginView.as_view(), name="login_alias"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout_alias"),
    # Sistema de inventario
    path("", include("inventario.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
