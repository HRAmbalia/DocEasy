from django.shortcuts import render

# Create your views here.
    # editPDFApp :
    # ROTATE PDF
    # ADD WATERMARK to PDF
    # ADD PAGE no

def RotatePDF(request):
    if request.method == 'POST' and request.FILES['myfile']:
        uploaded_image = request.FILES['myfile']
    else:
        return render(request, 'RotatePDF.html')
    
def AddWatermarktoPDF(request):
    if request.method == 'POST' and request.FILES['myfile']:
        uploaded_image = request.FILES['myfile']
    else:
        return render(request, 'AddWatermarktoPDF.html')

def AddPageNo(request):
    if request.method == 'POST' and request.FILES['myfile']:
        uploaded_image = request.FILES['myfile']
    else:
        return render(request, 'AddPageNo.html')