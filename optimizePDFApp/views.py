# optimizePDFApp
from django.shortcuts import render

# importing modules
import os
from django.core.files.storage import FileSystemStorage
from datetime import datetime
from django.http import FileResponse
from pylovepdf.ilovepdf import ILovePdf # to compress pdf
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

#COMPRESS PDF###########################################################################

# this function will return Ouptut file(compressed pdf) path
def CompressPDF_Func(uploaded_file_name):
    pdf_path = MEDIA_PATH + uploaded_file_name
    public_key = 'project_public_0eed65dc44084dc02fccb90b7d4c7f3c_WMfTObe104a679401ae2b10300f3e09ecce2a'
    ilovepdf = ILovePdf(public_key, verify_ssl=True)
    task = ilovepdf.new_task('compress')
    task.add_file(pdf_path)
    task.set_output_folder(MEDIA_PATH)
    task.execute()
    compressed_pdf_name = task.download()
    task.delete_current_task()
    return MEDIA_PATH + compressed_pdf_name

def CompressPDF(request):
    if request.method == 'POST' and request.FILES['myPDF']:
        fs = FileSystemStorage() # Saving uploaded file with updated names
        uploaded_file = []
        uploaded_pdf = request.FILES['myPDF']
        newFileName = uploaded_pdf.name.replace(".pdf",(return_Time()+".pdf"))
        filename = fs.save(newFileName, uploaded_pdf)
        uploaded_file.append(filename)
        compressed_pdf_path = CompressPDF_Func(uploaded_file[0]) # There's only one file
        print("compressed_pdf_path : ", compressed_pdf_path)
        converted_pdf = open(compressed_pdf_path, 'rb')
        return FileResponse(converted_pdf, content_type='application/pdf')
    else:
        return render(request, 'CompressPDF.html')

########################################################################################

