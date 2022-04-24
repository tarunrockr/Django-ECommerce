from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),

    # Front User urls
    path('', include('store.urls')),
    path('', include('profiles.urls')),
    path('', include('carts.urls')),
    path('', include('orders.urls')),

    # Admin urls
    path('backend/', include('admin_login.urls')),
    path('backend/', include('admin_profile.urls')),
    path('backend/', include('admin_manage_users.urls')),

    # Common urls
    path('', include('emails.urls'))
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,  document_root=settings.MEDIA_ROOT)
