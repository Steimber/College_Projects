from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

admin.site.site_header = "Cafetería Aroma Manabita — Administración"
admin.site.site_title = "Panel Admin Cafetería"
admin.site.index_title = "Gestión de Servicios, Pedidos y Blog"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('servicios.urls')),
    path('blog/', include('blog.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
