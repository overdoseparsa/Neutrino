from django.contrib import admin
from django.conf import settings
from django.urls import path, include
from django.conf.urls.static import static
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)
urlpatterns = [
    path("schema/", SpectacularAPIView.as_view(api_version="v1"), name="schema"),
    path("", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    path("redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
    path('admin/', admin.site.urls),
    path('api/', include(('neutrino.api.urls', 'api'))),
    path('auth/' , include(('neutrino.authentication.urls') , 'auths'))  , # TODO will change
    path('account/' , include(('neutrino.account.urls') , 'account')) , 
    path('otp/' , include('neutrino.otp.urls')) , 
    path('post/' , include('neutrino.post.urls')) , 

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
