# optimizePDFApp
from django.shortcuts import render

# importing modules
import os
from django.core.files.storage import FileSystemStorage
from datetime import datetime
from django.http import FileResponse
from pylovepdf.ilovepdf import ILovePdf # to compress pdf
from homePageApp.models import uploaded_DocDetails
MEDIA_PATH = os.path.join(os.getcwd(), "media", "")

########################################################################################

# Create your views here.
    ### COMPRESS PDF

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
    print("uploaded_docDetails : ", uploaded_docDetails)
    file_path = MEDIA_PATH + file_name
    print("file_path : ", file_path)
    if request.user.is_authenticated:
        print("datetime.now() : ", datetime.now())
        docDetails_Object = uploaded_DocDetails(fileName=file_name, filePath=file_path, typrOfFile=fileType, UserName=request.user.username)
    else:
        print("datetime.now() : ", datetime.now())
        docDetails_Object = uploaded_DocDetails(fileName=file_name, filePath=file_path, typrOfFile=fileType)
    docDetails_Object.save()

#COMPRESS PDF###########################################################################
#DOnE

def CompressPDF_Func(filename):
    pdf_path = MEDIA_PATH + filename
    public_key = 'project_public_0eed65dc44084dc02fccb90b7d4c7f3c_WMfTObe104a679401ae2b10300f3e09ecce2a'
    ilovepdf = ILovePdf(public_key, verify_ssl=True)
    task = ilovepdf.new_task('compress')
    task.add_file(pdf_path)
    task.set_output_folder(MEDIA_PATH)
    task.execute()
    compressed_pdf_name = task.download()
    task.delete_current_task()
    #
    to_delete_files = []
    to_delete_files.append(filename)
    delete_Files(to_delete_files)  # deletes user uploaded files
    #
    return compressed_pdf_name, MEDIA_PATH + compressed_pdf_name

def CompressPDF(request):
    if request.method == 'POST' and request.FILES['myPDF']:
        fs = FileSystemStorage()
        uploaded_pdf = request.FILES['myPDF']
        newFileName = uploaded_pdf.name.replace(".pdf",(return_Time()+".pdf"))
        file_name = fs.save(newFileName, uploaded_pdf) # Saving uploaded file with updated names
        compressed_pdf_name, compressed_pdf_path = CompressPDF_Func(file_name)
        print("converted_pdf_name : ", compressed_pdf_name)
        print("converted_pdf_path : ", compressed_pdf_path)
        save_DocDetails_to_DB(compressed_pdf_name, request, "PDF")
        # converted_pdf = open(compressed_pdf_path, 'rb')
        # return FileResponse(converted_pdf, content_type='application/pdf')
    else:
        return render(request, 'CompressPDF.html')

########################################################################################

