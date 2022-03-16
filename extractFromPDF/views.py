from django.shortcuts import render

# Create your views here.
    # extractFromPDF : 
    # EXTRACT TEXT FROM PDF
    # EXTRACT TEXT FROM IMAGE
    # PDF to AUDIObOOK

def ExtractTextFromPDF(request):
    if request.method == 'POST' and request.FILES['myfile']:
        uploaded_image = request.FILES['myfile']
    else:
        return render(request, 'ExtractTextFromPDF.html')

def ExtractTextFromImage(request):
    if request.method == 'POST' and request.FILES['myfile']:
        uploaded_image = request.FILES['myfile']
    else:
        return render(request, 'ExtractTextFromImage.html')

def PDFtoAudiobook(request):
    if request.method == 'POST' and request.FILES['myfile']:
        uploaded_image = request.FILES['myfile']
    else:
        return render(request, 'PDFtoAudiobook.html')
      