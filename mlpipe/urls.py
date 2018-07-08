from django.conf.urls import include, url
from django.contrib import admin

import views
from views import (DefaultFormByFieldView, DefaultFormsetView, DefaultFormView,
                   FormHorizontalView, FormInlineView, FormWithFilesView,
                   HomePageView, MiscView, PaginationView, getmodule)

urlpatterns = [
    url(r'^$', HomePageView.as_view(), name='home'),
    url(r'^getmodule$', views.getmodule, name='getmodule'),
    url(r'^setparams$', views.set_parameters, name='setparams'),
    url(r'^openmodal$', views.open_modal, name='openmodal'),
    url(r'^load$', views.load_model, name='load'),
    url(r'^admin/', admin.site.urls),
    url(r'^formset$', DefaultFormsetView.as_view(), name='formset_default'),
    url(r'^form$', DefaultFormView.as_view(), name='form_default'),
    url(r'^form_by_field$', DefaultFormByFieldView.as_view(), name='form_by_field'),
    url(r'^form_horizontal$', FormHorizontalView.as_view(), name='form_horizontal'),
    url(r'^form_inline$', FormInlineView.as_view(), name='form_inline'),
    url(r'^form_with_files$', FormWithFilesView.as_view(), name='form_with_files'),
    url(r'^pagination$', PaginationView.as_view(), name='pagination'),
    url(r'^misc$', MiscView.as_view(), name='misc'),
]
