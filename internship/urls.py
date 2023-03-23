from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularSwaggerView, SpectacularAPIView, SpectacularRedocView
from rest_framework.routers import DefaultRouter

from users.views import PractiseApiView, CreatePractiseApiView, ListPractiseApiView

router = DefaultRouter()
# router.register(r'Practise', )

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('djoser.urls')),
    path('', include('djoser.urls.authtoken')),

    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    # Optional UI:
    path('api/v1/documentation', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/v1/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),

    path('api', include(router.urls)),
    path('api/practise/<int:pk>', PractiseApiView.as_view()),
    path('api/practise', CreatePractiseApiView.as_view()),
    path('api/practises', ListPractiseApiView.as_view()),

]

admin.site.site_header = 'كشري مان'  # default: "Django Administration"
admin.site.index_title = 'ششش'  # default: "Site administration"
admin.site.site_title = 'موقع تجريبي'  # default: "Django site admin"
