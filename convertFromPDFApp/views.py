#convertFromPDFApp
from django.shortcuts import render

# importing modules
import os
from django.core.files.storage import FileSystemStorage
from datetime import datetime
from django.http import FileResponse
import tabula # to pdf to excel
from pdf2image import convert_from_path # to pdf to image
from homePageApp.models import uploaded_DocDetails
MEDIA_PATH = os.path.join(os.getcwd(), "media", "")

########################################################################################

# Create your views here.
    # convertFromPDFApp : 
    ### PDF to JPG
    ### PDF to WORD
    ### PDF to PPT
    ### PDF to EXCEL

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

#PDF to JPG#############################################################################
#nOT DOnE

def PDFtoJPG_Func(filename):
    pdf_path = MEDIA_PATH + filename
    print("pdf_path : ", pdf_path)
    # excel_file_name = filename.replace('.pdf','.csv')
    # excel_file_path = MEDIA_PATH + excel_file_name
    images = convert_from_path(pdf_path)
    for i in range(len(images)):
        
        iName = images[i].save('page'+ str(i) +'.jpg', 'JPEG')
        print("iName : ", iName)
    #
    to_delete_files = []
    to_delete_files.append(filename)
    delete_Files(to_delete_files)  # deletes user uploaded files
    #
    return filename

def PDFtoJPG(request):
    if request.method == 'POST' and request.FILES['myPDF']:
        fs = FileSystemStorage()
        uploaded_pdf = request.FILES['myPDF']
        newFileName = uploaded_pdf.name.replace(".pdf",(return_Time()+".pdf"))
        file_name = fs.save(newFileName, uploaded_pdf) # Saving uploaded file with updated unique names
        zip_file_name, zip_file_path = PDFtoJPG_Func(file_name)
        print("zip_file_name : ", zip_file_name)
        print("zip_file_path : ", zip_file_path)
        save_DocDetails_to_DB(excel_file_name, request, "ZIP")
        converted_excel = open(excel_file_name, 'rb')
        return FileResponse(excel_file_name, content_type='application')
    else:
        return render(request, 'PDFtoJPG.html')

#PDF to WORD##############################################################################
#nOT DOnE

def PDFtoWORD(request):
    if request.method == 'POST' and request.FILES['myfile']:
        uploaded_image = request.FILES['myfile']
    else:
        return render(request, 'PDFtoWORD.html')

#PDF to PPT###############################################################################
#nOT DOnE

def PDFtoPPT(request):
    if request.method == 'POST' and request.FILES['myfile']:
        uploaded_image = request.FILES['myfile']
    else:
        return render(request, 'PDFtoPPT.html')

#PDF to EXCEL#############################################################################
#DOnE

def PDFtoEXCEL_Func(filename):
    pdf_path = MEDIA_PATH + filename
    print("pdf_path : ", pdf_path)
    excel_file_name = filename.replace('.pdf','.csv')
    excel_file_path = MEDIA_PATH + excel_file_name
    df = tabula.read_pdf(pdf_path, pages='all')[0]
    tabula.convert_into(pdf_path, excel_file_path, output_format="csv", pages='all')
    #
    to_delete_files = []
    to_delete_files.append(filename)
    delete_Files(to_delete_files)  # deletes user uploaded files
    #
    return excel_file_name, excel_file_path

def PDFtoEXCEL(request):
    if request.method == 'POST' and request.FILES['myPDF']:
        fs = FileSystemStorage()
        uploaded_pdf = request.FILES['myPDF']
        newFileName = uploaded_pdf.name.replace(".pdf",(return_Time()+".pdf"))
        file_name = fs.save(newFileName, uploaded_pdf) # Saving uploaded file with updated unique names
        excel_file_name, excel_file_path = PDFtoEXCEL_Func(file_name)
        print("excel_file_name : ", excel_file_name)
        print("excel_file_path : ", excel_file_path)
        save_DocDetails_to_DB(excel_file_name, request, "EXCEL")
        converted_excel = open(excel_file_name, 'rb')
        return FileResponse(excel_file_name, content_type='application')
    else:
        return render(request, 'PDFtoEXCEL.html')

########################################################################################
