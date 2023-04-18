#extractFromPDF
from django.shortcuts import render

# importing modules
import os
from django.core.files.storage import FileSystemStorage
from datetime import datetime
from django.http import FileResponse
from homePageApp.models import uploaded_DocDetails
MEDIA_PATH = os.path.join(os.getcwd(), "media", "")

########################################################################################

# Create your views here.
    # extractFromPDF : 
    # EXTRACT TEXT FROM PDF
    # EXTRACT TEXT FROM IMAGE
    # PDF to AUDIObOOK

########################################################################################

# this function will return current timeStamp to differenciate pdf names
def return_Time():
    dateTimeObj = datetime.now()
    timestampStr = dateTimeObj.strftime("%d-%b-%Y (%H:%M:%S.%f)")
    return timestampStr

########################################################################################

# this function will DELETE the files which are  sent as parameter from media folder
def delete_Files(file_list):
    for file_name in file_list:
        file_path = MEDIA_PATH + file_name
        print("file_path : ", file_path)
        if os.path.exists(file_path):
            os.remove(file_path)

########################################################################################

# this function will Save document details to database
def save_DocDetails_to_DB(file_name, request, fileType):
    uploaded_docDetails = uploaded_DocDetails.objects.all()
    # print("uploaded_docDetails : ", uploaded_docDetails)
    file_path = MEDIA_PATH + file_name
    print("file_path : ", file_path)
    if request.user.is_authenticated:
        print("datetime.now() : ", datetime.now())
        docDetails_Object = uploaded_DocDetails(fileName=file_name, filePath=file_path, typrOfFile=fileType, UserName=request.user.username)
    else:
        print("datetime.now() : ", datetime.now())
        docDetails_Object = uploaded_DocDetails(fileName=file_name, filePath=file_path, typrOfFile=fileType)
    docDetails_Object.save()

#Extract Text From PDF##################################################################

def ExtractTextFromPDF(request):
    if request.method == 'POST' and request.FILES['myfile']:
        uploaded_image = request.FILES['myfile']
    else:
        return render(request, 'ExtractTextFromPDF.html')

#Extract Text From Image################################################################

def ExtractTextFromImage(request):
    if request.method == 'POST' and request.FILES['myfile']:
        uploaded_image = request.FILES['myfile']
    else:
        return render(request, 'ExtractTextFromImage.html')

#PDF to Audiobook#######################################################################

def PDFtoAudiobook(request):
    if request.method == 'POST' and request.FILES['myfile']:
        uploaded_image = request.FILES['myfile']
    else:
        return render(request, 'PDFtoAudiobook.html')
      
########################################################################################