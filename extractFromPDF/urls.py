from django.urls import path
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    # EXTRACT TEXT FROM PDF
    # EXTRACT TEXT FROM IMAGE
    # PDF to AUDIObOOK
]

urlpatterns += staticfiles_urlpatterns()