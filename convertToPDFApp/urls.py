from django.urls import path
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    ### JPG to PDF
    ### WORD to PDF
    ### PPT to PDF
    ### EXCEL to PDF
    ### HTML to PDF
]

urlpatterns += staticfiles_urlpatterns()