from django.urls import path
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    # ROTATE PDF
    # ADD WATERMARK to PDF
    # ADD PAGE no
]

urlpatterns += staticfiles_urlpatterns()