from django.urls import path
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    # MERGE PDF
    # SPLIT PDF
    # REMOVE PAGES FROM PDF
]

urlpatterns += staticfiles_urlpatterns()