from django.shortcuts import render

# Create your views here.
    # convertFromPDFApp : 
    ### PDF to JPG
    ### PDF to WORD
    ### PDF to PPT
    ### PDF to EXCEL

def PDFtoJPG(request):
    if request.method == 'POST' and request.FILES['myfile']:
        uploaded_image = request.FILES['myfile']
    else:
        return render(request, 'PDFtoJPG.html')

def PDFtoWORD(request):
    if request.method == 'POST' and request.FILES['myfile']:
        uploaded_image = request.FILES['myfile']
    else:
        return render(request, 'PDFtoWORD.html')

def PDFtoPPT(request):
    if request.method == 'POST' and request.FILES['myfile']:
        uploaded_image = request.FILES['myfile']
    else:
        return render(request, 'PDFtoPPT.html')

def PDFtoEXCEL(request):
    if request.method == 'POST' and request.FILES['myfile']:
        uploaded_image = request.FILES['myfile']
    else:
        return render(request, 'PDFtoEXCEL.html')
