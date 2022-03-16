from django.shortcuts import render

# Create your views here.
    # convertToPDFApp : s
    ### JPG to PDF
    ### WORD to PDF
    ### PPT to PDF
    ### EXCEL to PDF
    ### HTML to PDF

def JPGtoPDF(request):
    if request.method == 'POST' and request.FILES['myfile']:
        uploaded_image = request.FILES['myfile']
    else:
        return render(request, 'JPGtoPDF.html')

def WORDtoPDF(request):
    if request.method == 'POST' and request.FILES['myfile']:
        uploaded_image = request.FILES['myfile']
    else:
        return render(request, 'WORDtoPDF.html')

def HTMLtoPDF(request):
    if request.method == 'POST' and request.FILES['myfile']:
        uploaded_image = request.FILES['myfile']
    else:
        return render(request, 'HTMLtoPDF.html')

def PPTtoPDF(request):
    if request.method == 'POST' and request.FILES['myfile']:
        uploaded_image = request.FILES['myfile']
    else:
        return render(request, 'PPTtoPDF.html')

def EXCELtoPDF(request):
    if request.method == 'POST' and request.FILES['myfile']:
        uploaded_image = request.FILES['myfile']
    else:
        return render(request, 'EXCELtoPDF.html')