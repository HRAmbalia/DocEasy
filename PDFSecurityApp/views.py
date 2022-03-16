from django.shortcuts import render

# Create your views here.
    # PDFSecurityApp : 
    # UnLOCK PDF
    # PROTECT PDF
    # SIGn PDF

def UnlockPDF(request):
    if request.method == 'POST' and request.FILES['myfile']:
        uploaded_image = request.FILES['myfile']
    else:
        return render(request, 'UnlockPDF.html')

def ProtectPDF(request):
    if request.method == 'POST' and request.FILES['myfile']:
        uploaded_image = request.FILES['myfile']
    else:
        return render(request, 'ProtectPDF.html')

def SignPDF(request):
    if request.method == 'POST' and request.FILES['myfile']:
        uploaded_image = request.FILES['myfile']
    else:
        return render(request, 'SignPDF.html')
