from django.shortcuts import render

# Create your views here.

###################################################################################################
##########################################-JPG to PDF-#############################################
###################################################################################################

def JPGToPDF(request):
    if request.method == 'POST' and request.FILES['myfile']:
        uploaded_image = request.FILES['myfile']
        print("uploaded_image : ", uploaded_image)
    else:
        return render(request, 'JPGToPDF.html')