from django.urls import path
from . import views
# IMPORTInG VIEWS
from convertFromPDFApp import views as convertFromPDFAppViews
    ### PDF to JPG
    ### PDF to WORD
    ### PDF to PPT
    ### PDF to EXCEL
from convertToPDFApp import views as convertToPDFAppViews
    ### JPG to PDF
    ### WORD to PDF
    ### PPT to PDF
    ### EXCEL to PDF
    ### HTML to PDF
from editPDFApp import views as editPDFAppViews
    # ROTATE PDF
    # ADD WATERMARK to PDF
    # ADD PAGE no
from extractFromPDF import views as extractFromPDFViews
    # EXTRACT TEXT FROM PDF
    # EXTRACT TEXT FROM IMAGE
    # PDF to AUDIObOOK
from optimizePDFApp import views as optimizePDFAppViews
    # COMPRESS PDF
from organizePDFApp import views as organizePDFAppViews
    # MERGE PDF
    # SPLIT PDF
    # REMOVE PAGES FROM PDF
from PDFSecurityApp import views as PDFSecurityAppViews
    # UnLOCK PDF
    # PROTECT PDF
    # SIGn PDF
#
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', views.index, name='index'),
    # path('contactUs/', views.contactUs, name='contactUs'),
    # convertToPDFApp
    path('JPGtoPDF/', convertToPDFAppViews.JPGtoPDF, name='JPGtoPDF'),
    path('WORDtoPDF/', convertToPDFAppViews.WORDtoPDF, name='WORDtoPDF'),
    path('PPTtoPDF/', convertToPDFAppViews.PPTtoPDF, name='PPTtoPDF'),
    path('EXCELtoPDF/', convertToPDFAppViews.EXCELtoPDF, name='EXCELtoPDF'),
    path('HTMLtoPDF/', convertToPDFAppViews.HTMLtoPDF, name='HTMLtoPDF'),
    # convertFromPDFApp
    path('PDFtoJPG/', convertFromPDFAppViews.PDFtoJPG, name='PDFtoJPG'),
    path('PDFtoWORD/', convertFromPDFAppViews.PDFtoWORD, name='PDFtoWORD'),
    path('PDFtoPPT/', convertFromPDFAppViews.PDFtoPPT, name='PDFtoPPT'),
    path('PDFtoEXCEL/', convertFromPDFAppViews.PDFtoEXCEL, name='PDFtoEXCEL'),
    # editPDFApp
    path('RotatePDF/', editPDFAppViews.RotatePDF, name='RotatePDF'),
    path('AddWatermarktoPDF/', editPDFAppViews.AddWatermarktoPDF, name='AddWatermarktoPDF'),
    path('AddPageNo/', editPDFAppViews.AddPageNo, name='AddPageNo'),
    # extractFromPDF
    path('ExtractTextFromPDF/', extractFromPDFViews.ExtractTextFromPDF, name='ExtractTextFromPDF'),
    path('ExtractTextFromImage/', extractFromPDFViews.ExtractTextFromImage, name='ExtractTextFromImage'),
    path('PDFtoAudiobook/', extractFromPDFViews.PDFtoAudiobook, name='PDFtoAudiobook'),
    # optimizePDFApp
    path('CompressPDF/', optimizePDFAppViews.CompressPDF, name='CompressPDF'),
    # organizePDFApp
    path('MergePDF/', organizePDFAppViews.MergePDF, name='MergePDF'),
    path('SplitPDF/', organizePDFAppViews.SplitPDF, name='SplitPDF'),
    path('RemovePagesFromPDF/', organizePDFAppViews.RemovePagesFromPDF, name='RemovePagesFromPDF'),
    # PDFSecurityApp
    path('UnlockPDF/', PDFSecurityAppViews.UnlockPDF, name='UnlockPDF'),
    path('ProtectPDF/', PDFSecurityAppViews.ProtectPDF, name='ProtectPDF'),
    path('SignPDF/', PDFSecurityAppViews.SignPDF, name='SignPDF'),
]

urlpatterns += staticfiles_urlpatterns()
