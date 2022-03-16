from django.shortcuts import render

# Create your views here.
    # organizePDFApp : 
    # MERGE PDF
    # SPLIT PDF
    # REMOVE PAGES FROM PDF

def MergePDF(request):
    if request.method == 'POST' and request.FILES['myfile']:
        uploaded_image = request.FILES['myfile']
    else:
        return render(request, 'MergePDF.html')

def SplitPDF(request):
    if request.method == 'POST' and request.FILES['myfile']:
        uploaded_image = request.FILES['myfile']
    else:
        return render(request, 'SplitPDF.html')

def RemovePagesFromPDF(request):
    if request.method == 'POST' and request.FILES['myfile']:
        uploaded_image = request.FILES['myfile']
    else:
        return render(request, 'RemovePagesFromPDF.html')