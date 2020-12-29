from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.utils.translation import ugettext_lazy as _

admin.site.site_header = _(f'{settings.SITE["NAME"]} administration')
admin.site.site_title = _(f'{settings.SITE["DESCRIPTION"]} administration')
admin.site.index_title = _('Dashboard')

urlpatterns = i18n_patterns(
    path('admin/', admin.site.urls),
    prefix_default_language=False
)

urlpatterns += [

]

# This is only needed when using runserver.
if settings.DEBUG:
    from drf_yasg import openapi
    from drf_yasg.views import get_schema_view
    from rest_framework.permissions import AllowAny

    schema_view = get_schema_view(
        openapi.Info(
            title=f'{settings.SITE["NAME"]} APIs',
            default_version=f'{settings.REST_FRAMEWORK["DEFAULT_VERSION"]}',
            description=f'{settings.SITE["DESCRIPTION"]}',
            contact=openapi.Contact(email=f'{settings.DEFAULT_FROM_EMAIL}')
        ),
        public=True,
        permission_classes=(AllowAny,)
    )

    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
    urlpatterns += [
        path('api-auth',
             include('rest_framework.urls', namespace='rest_framework')),
        path('swagger', schema_view.with_ui('swagger', cache_timeout=0),
             name='schema-swagger-ui'),
        path('redoc', schema_view.with_ui('redoc', cache_timeout=0),
             name='schema-redoc')
    ]
