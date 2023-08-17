
from django.conf import settings
from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static


from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework.permissions import AllowAny


from wagtail.admin import urls as wagtailadmin_urls
from wagtail import urls as wagtail_urls
from wagtail.documents import urls as wagtaildocs_urls

from search import views as search_views


schema_view = get_schema_view(
   openapi.Info(
      title="BLOG APIs",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="test License"),
   ),
   public=True,
   permission_classes=[AllowAny]
)

urlpatterns = [
   path('admin', admin.site.urls),
   path('user/', include('user.urls'),name = 'user'),
   path('api/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
   path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
   path('wagtail_admin/', include(wagtailadmin_urls)),
   path('documents/', include(wagtaildocs_urls)),
   path('pages/', include(wagtail_urls)),
   path("search/", search_views.search, name="search"),
   path('search/',include('search.urls')),
   path('', include(wagtail_urls)),
] +  static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)