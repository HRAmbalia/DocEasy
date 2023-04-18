#PDFSecurityApp
from django.shortcuts import render

# importing modules
import os
from django.core.files.storage import FileSystemStorage
from datetime import datetime
from django.http import FileResponse
from PyPDF2 import PdfFileWriter, PdfFileReader # to Unlock PDF, to Lock PDF
from homePageApp.models import uploaded_DocDetails
MEDIA_PATH = os.path.join(os.getcwd(), "media", "")

########################################################################################

# Create your views here.
    # PDFSecurityApp : 
    # UnLOCK PDF
    # PROTECT PDF
    # SIGn PDF

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

#Unlock PDF#############################################################################
#DOnE

def UnlockPDF_Func(filename, password):
    pdf_path = MEDIA_PATH + filename
    print("pdf_path : ", pdf_path)
    if '-protected.pdf' in filename:
        decrypted_pdf_name = filename.replace('-protected.pdf','-decrypted.pdf')
    else:
        decrypted_pdf_name = filename.replace('.pdf','-decrypted.pdf')
    print("decrypted_pdf_name : ", decrypted_pdf_name)
    decrypted_pdf_path = MEDIA_PATH + decrypted_pdf_name
    print("decrypted_pdf_path : ", decrypted_pdf_path)
    out = PdfFileWriter()
    file = PdfFileReader(pdf_path)
    if file.isEncrypted:
        file.decrypt(password)
        for idx in range(file.numPages):
            page = file.getPage(idx)
            out.addPage(page)
        with open(decrypted_pdf_path, "wb") as f:
            out.write(f)
        print("File decrypted Successfully.")
    else:
        print("File already decrypted.")
    #
    to_delete_files = []
    to_delete_files.append(filename)
    delete_Files(to_delete_files)  # deletes user uploaded files
    #
    return decrypted_pdf_name, decrypted_pdf_path

def UnlockPDF(request):
    if request.method == 'POST' and request.FILES['myfile']:
        fs = FileSystemStorage()
        uploaded_protected_pdf = request.FILES['myfile']
        password = request.POST['password']
        newFileName = uploaded_protected_pdf.name.replace(".pdf",(return_Time()+".pdf"))
        file_name = fs.save(newFileName, uploaded_protected_pdf) # Saving uploaded file with updated unique names
        unlocked_pdf_name, unlocked_pdf_path = UnlockPDF_Func(file_name, password)
        print("unlocked_pdf_name : ", unlocked_pdf_name)
        print("unlocked_pdf_path : ", unlocked_pdf_path)
        save_DocDetails_to_DB(file_name, request, "PDF")
        # converted_pdf = open(compressed_pdf_path, 'rb')
        # return FileResponse(converted_pdf, content_type='application/pdf')
    else:
        return render(request, 'UnlockPDF.html')

#Protect PDF############################################################################
#DOnE

def ProtectPDF_Func(filename, password):
    pdf_path = MEDIA_PATH + filename
    encrypted_pdf_name = filename.replace('.pdf','-protected.pdf')
    print("encrypted_pdf_name : ", encrypted_pdf_name)
    encrypted_pdf_path = MEDIA_PATH + encrypted_pdf_name
    print("encrypted_pdf_path : ", encrypted_pdf_path)
    print("password : ", password)
    out = PdfFileWriter()
    file = PdfFileReader(pdf_path)
    num = file.numPages
    for idx in range(num):
        page = file.getPage(idx)
        out.addPage(page)
    out.encrypt(password)
    with open(encrypted_pdf_path, "wb") as f:
        out.write(f)
    #
    to_delete_files = []
    to_delete_files.append(filename)
    delete_Files(to_delete_files)  # deletes user uploaded files
    #
    return encrypted_pdf_name, encrypted_pdf_path

def ProtectPDF(request):
    if request.method == 'POST' and request.FILES['myfile']:
        fs = FileSystemStorage()
        uploaded_pdf = request.FILES['myfile']
        password = request.POST['password']
        newFileName = uploaded_pdf.name.replace(".pdf",(return_Time()+".pdf"))
        file_name = fs.save(newFileName, uploaded_pdf) # Saving uploaded file with updated unique names
        encrypted_pdf_name, encrypted_pdf_path = ProtectPDF_Func(file_name, password)
        print("encrypted_pdf_name : ", encrypted_pdf_name)
        print("encrypted_pdf_path : ", encrypted_pdf_path)
        save_DocDetails_to_DB(encrypted_pdf_name, request, "PDF")
        # converted_pdf = open(compressed_pdf_path, 'rb')
        # return FileResponse(converted_pdf, content_type='application/pdf')
    else:
        return render(request, 'ProtectPDF.html')

#Sign PDF###############################################################################

def SignPDF(request):
    if request.method == 'POST' and request.FILES['myfile']:
        uploaded_image = request.FILES['myfile']
    else:
        return render(request, 'SignPDF.html')
