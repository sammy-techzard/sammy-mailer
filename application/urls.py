from django.conf import settings
from django.urls import include, path
from django.contrib import admin

from wagtail.admin import urls as wagtailadmin_urls
from wagtail import urls as wagtail_urls
from wagtail.documents import urls as wagtaildocs_urls

from search import views as search_views
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
# Define the Swagger UI view

schema_view = get_schema_view(
   openapi.Info(
      title="Kiin Mailer API Documentation",
      default_version='v1',
      description="""
        **Authentication Instructions:**  
        This API uses **Bearer Token authentication**.  
        1. Obtain a token from administrators  
        2. Include the token in the `Authorization` header as follows:  
        ```
        Authorization: Bearer <your_access_token>
        ```
        3. Some endpoints require authentication. Ensure you send a valid token.  
        """,
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="nisammy@gmail.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path("django-admin/", admin.site.urls),
    path("admin/", include(wagtailadmin_urls)),
    path("documents/", include(wagtaildocs_urls)),
    path("search/", search_views.search, name="search"),
    path('api/', include('main.urls')),
    # Swagger UI docs
   path('', schema_view.with_ui('swagger', cache_timeout=0), name='swagger-ui'),
   path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='redoc-ui'),

]


if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    # Serve static and media files from development server
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns = urlpatterns + [
    # For anything not caught by a more specific rule above, hand over to
    # Wagtail's page serving mechanism. This should be the last pattern in
    # the list:
    path("", include(wagtail_urls)),
    # Alternatively, if you want Wagtail pages to be served from a subpath
    # of your site, rather than the site root:
    #    path("pages/", include(wagtail_urls)),
]
