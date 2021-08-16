from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from django.conf.urls.i18n import i18n_patterns
from django.views.i18n import JavaScriptCatalog
from django.utils.translation import gettext_lazy as _


admin.site.index_title = _('Admin Panel')
admin.site.site_header = _('Company Admin Panel')
admin.site.site_title = _('Company')


urlpatterns = [
    path('lang/', include('lang_ctrl.urls', namespace='lang')),
]

if settings.DEBUG :
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += i18n_patterns(
    path('admin/', admin.site.urls),
    path('', include('introduction.urls', namespace='introduction')),
    path('shop/', include('store.urls', namespace='store')),
    path('account/', include('accounts.urls', namespace='accounts')),  
    path('basket/', include('basket.urls', namespace='basket')),
    path('orders/', include('orders.urls', namespace='orders')),
    path('addresses/', include('addresses.urls', namespace='addresses')),
    path('checkout/', include('checkout.urls', namespace='checkout')),
    path('preorder/', include('preorder.urls', namespace='preorder')),
    path('jsi18n/', JavaScriptCatalog.as_view(), name='js-cat'),
)

