from django.urls import path
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    # PDF to JPG
    # PDF to WORD
    # PDF to PPT
    # PDF to EXCEL
]

urlpatterns += staticfiles_urlpatterns()