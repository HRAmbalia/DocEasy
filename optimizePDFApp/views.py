from django.shortcuts import render

# Create your views here.
    # optimizePDFApp
    # COMPRESS PDF

def CompressPDF(request):
    if request.method == 'POST' and request.FILES['myfile']:
        uploaded_image = request.FILES['myfile']
    else:
        return render(request, 'CompressPDF.html')
        