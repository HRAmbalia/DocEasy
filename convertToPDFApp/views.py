# convertToPDFApp :
from django.shortcuts import render

# importing modules
import os
from django.core.files.storage import FileSystemStorage
from datetime import datetime
from django.http import FileResponse
from PIL import Image # to JPG to PDF
import pdfkit # to HTML to PDF
import groupdocs_conversion_cloud # to EXCEL to PDF
from shutil import copyfile # to EXCEL to PDF 
import requests, json # to PPT to PDF, to WORD to PDF
from homePageApp.models import uploaded_DocDetails
MEDIA_PATH = os.path.join(os.getcwd(), "media", "")

########################################################################################

# Create your views here.
    ### JPG to PDF
    ### WORD to PDF
    ### PPT to PDF
    ### EXCEL to PDF
    ### HTML to PDF

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
        docDetails_Object = uploaded_DocDetails(fileName=file_name, filePath=file_path, typrOfFile=fileType, UserName=request.user.username)
    else:
        docDetails_Object = uploaded_DocDetails(fileName=file_name, filePath=file_path, typrOfFile=fileType)
    docDetails_Object.save()

#JPG TO PDF#############################################################################
#DOnE

def JPGtoPDF_Func(images):
    image_path = MEDIA_PATH + images[0]
    image = Image.open(image_path)
    im1 = image.convert('RGB')
    image_list = []
    if ".jpg" in images[0]:
        pdf_name = images[0].replace(".jpg",".pdf")
    elif ".JPG" in images[0]:
        pdf_name = images[0].replace(".JPG",".pdf")
    elif ".jpeg" in images[0]:
        pdf_name = images[0].replace(".jpeg",".pdf")
    elif ".JPEG" in images[0]:
        pdf_name = images[0].replace(".JPEG",".pdf")
    elif ".png" in images[0]:
        pdf_name = images[0].replace(".png",".pdf")
    elif ".PNG" in images[0]:
        pdf_name = images[0].replace(".PNG",".pdf")
    pdf_path = MEDIA_PATH + pdf_name
    for img in images:
        image_path = MEDIA_PATH + img
        image = Image.open(image_path)
        im = image.convert('RGB')
        image_list.append(im)
    image_list.pop(0)
    im1.save(pdf_path, save_all=True, append_images=image_list)
    delete_Files(images) # deletes user uploaded files
    return pdf_name, pdf_path

def JPGtoPDF(request):
    if request.method == 'POST' and request.FILES['images']:
        uploaded_file = []
        fs = FileSystemStorage()
        images = request.FILES.getlist('images')
        for img in images:
            if ".jpg" in img.name:
                newFileName = img.name.replace(".jpg",(return_Time()+".jpg"))
            elif ".JPG" in img.name: 
                newFileName = img.name.replace(".JPG",(return_Time()+".JPG"))
            elif ".jpeg" in img.name: 
                newFileName = img.name.replace(".jpeg",(return_Time()+".jpeg"))
            elif ".JPEG" in img.name: 
                newFileName = img.name.replace(".JPEG",(return_Time()+".JPEG"))
            elif ".png" in img.name: 
                newFileName = img.name.replace(".png",(return_Time()+".png"))
            elif ".PNG" in img.name: 
                newFileName = img.name.replace(".PNG",(return_Time()+".PNG"))
            filename = fs.save(newFileName, img)
            uploaded_file.append(filename)
        # print("Uploaded File : ", uploaded_file)       
        converted_pdf_name, converted_pdf_path = JPGtoPDF_Func(uploaded_file)
        print("converted_pdf_name : ", converted_pdf_name)
        print("converted_pdf_path : ", converted_pdf_path)
        save_DocDetails_to_DB(converted_pdf_name, request, "PDF") # Saves pdf details to database
    else:
        return render(request, 'JPGtoPDF.html')

#WORD to PDF############################################################################
#DOnE

def WORDToPDF_Func(filename):
    word_path = MEDIA_PATH + filename
    pdf_name = filename.replace(".docx",".pdf")
    pdf_path = MEDIA_PATH + pdf_name
    instructions = {
        'parts': [
            {
                'file': 'document'
            }
        ]
    }
    response = requests.request(
        'POST',
        'https://api.pspdfkit.com/build',
        headers={
            'Authorization': 'Bearer pdf_live_dM9fhAsWkOXv2ctQsusElVRhESAu41mTwtU5WrtA1sF'
        },
        files={
            'document': open(word_path, 'rb')
        },
        data={
            'instructions': json.dumps(instructions)
        },
        stream=True
    )
    if response.ok:
        with open(pdf_path, 'wb') as fd:
            for chunk in response.iter_content(chunk_size=8096):
                fd.write(chunk)
    else:
        print(response.text)
        exit()
    #
    to_delete_files = []
    to_delete_files.append(filename)
    delete_Files(to_delete_files)  # deletes user uploaded files
    #
    return pdf_name, pdf_path

def WORDtoPDF(request):
    if request.method == 'POST' and request.FILES['myWordFile']:
        uploaded_file = []
        fs = FileSystemStorage()
        uploaded_word_file = request.FILES['myWordFile']
        newFileName = uploaded_word_file.name.replace(".docx",(return_Time()+".docx"))
        file_name = fs.save(newFileName, uploaded_word_file)
        converted_pdf_name, converted_pdf_path = WORDToPDF_Func(file_name)
        print("converted_pdf_name : ", converted_pdf_name)
        print("converted_pdf_path : ", converted_pdf_path)
        save_DocDetails_to_DB(converted_pdf_name, request, "PDF") # Saves pdf details to database
    else:
        return render(request, 'WORDtoPDF.html')

#HTML to PDF############################################################################
#DOnE

def HTMLToPDF_Func(filename):
    html_path = MEDIA_PATH + filename
    pdf_name = filename.replace(".html",".pdf")
    pdf_path = MEDIA_PATH + pdf_name
    pdfkit.from_file(html_path, pdf_path)
    #
    to_delete_files = []
    to_delete_files.append(filename)
    delete_Files(to_delete_files)  # deletes user uploaded files
    #
    return pdf_name, pdf_path

def HTMLtoPDF(request):
    if request.method == 'POST' and request.FILES['myHtmlFile']:
        uploaded_file = []
        fs = FileSystemStorage()
        html_file = request.FILES['myHtmlFile']
        newFileName = html_file.name.replace(".html",(return_Time()+".html"))
        file_name = fs.save(newFileName, html_file)
        converted_pdf_name, converted_pdf_path = HTMLToPDF_Func(file_name)
        print("converted_pdf_name : ", converted_pdf_name)
        print("converted_pdf_path : ", converted_pdf_path)
        save_DocDetails_to_DB(converted_pdf_name, request, "PDF") # Saves pdf details to database
    else:
        return render(request, 'HTMLtoPDF.html')

#PPT to PDF#############################################################################
#DOnE

def PPTtoPDF_Func(filename):
    ppt_path = MEDIA_PATH + filename
    if ".pptx" in filename:
        pdf_name = filename.replace(".pptx",".pdf")
    elif ".ppt" in filename:
        pdf_name = filename.replace(".ppt",".pdf")
    pdf_path = MEDIA_PATH + pdf_name
    instructions = {
        'parts': [
            {
            'file': 'document'
            }
        ]
    }
    response = requests.request(
    'POST',
    'https://api.pspdfkit.com/build',
    headers = {
        'Authorization': 'Bearer pdf_live_dM9fhAsWkOXv2ctQsusElVRhESAu41mTwtU5WrtA1sF'
    },
    files = {
        'document': open(ppt_path, 'rb')
    },
    data = {
        'instructions': json.dumps(instructions)
    },
    stream = True
    )
    if response.ok:
        with open(pdf_path, 'wb') as fd:
            for chunk in response.iter_content(chunk_size=8096):
                fd.write(chunk)
    else:
        print(response.text)
        exit()
    #
    to_delete_files = []
    to_delete_files.append(filename)
    delete_Files(to_delete_files)  # deletes user uploaded files
    #
    return pdf_name, pdf_path

def PPTtoPDF(request):
    if request.method == 'POST' and request.FILES['myPPT']:
        uploaded_file = []
        fs = FileSystemStorage()
        uploaded_ppt = request.FILES['myPPT']
        if ".pptx" in uploaded_ppt.name:
            newFileName = uploaded_ppt.name.replace(".pptx",(return_Time()+".pptx"))
        elif ".ppt" in uploaded_ppt.name:
            newFileName = uploaded_ppt.name.replace(".ppt",(return_Time()+".ppt"))
        file_name = fs.save(newFileName, uploaded_ppt)
        converted_pdf_name, converted_pdf_path = PPTtoPDF_Func(file_name)
        print("converted_pdf_name : ", converted_pdf_name)
        print("converted_pdf_path : ", converted_pdf_path)
        save_DocDetails_to_DB(converted_pdf_name, request, "PDF") # Saves pdf details to database
    else:
        return render(request, 'PPTtoPDF.html')

#EXCEL to PDF###########################################################################
#DOnE

def excelToPDF_Func(filename):
    excel_path = MEDIA_PATH + filename
    if ".xlsx" in filename:
        pdf_name = filename.replace(".xlsx",".pdf")
    elif ".xls" in filename:
        pdf_name = filename.replace(".xls",".pdf")
    pdf_path = MEDIA_PATH + pdf_name
    client_id = "2e818d52-2be0-4ef1-97c1-1778fb591bef"
    client_key = "a898e4b606d84a88d4bca3e2476394c2"
    convert_api = groupdocs_conversion_cloud.ConvertApi.from_keys(client_id, client_key)
    try:
        request = groupdocs_conversion_cloud.ConvertDocumentDirectRequest("pdf", excel_path)
        result = convert_api.convert_document_direct(request)       
        copyfile(result, pdf_path)
    except groupdocs_conversion_cloud.ApiException as e:
        print("Exception when calling get_supported_conversion_types: {0}".format(e.message))
    #
    to_delete_files = []
    to_delete_files.append(filename)
    delete_Files(to_delete_files)  # deletes user uploaded files
    #
    return pdf_name, pdf_path

def EXCELtoPDF(request):
    if request.method == 'POST' and request.FILES['myExcelFile']:
        uploaded_file = []
        fs = FileSystemStorage()
        origial_excel = request.FILES['myExcelFile']
        if ".xlsx" in origial_excel.name:
            newFileName = origial_excel.name.replace(".xlsx",(return_Time()+".xlsx"))
        elif ".xls" in origial_excel.name:
            newFileName = origial_excel.name.replace(".xls",(return_Time()+".xls"))
        file_name = fs.save(newFileName, origial_excel)
        converted_pdf_name, converted_pdf_path = excelToPDF_Func(file_name)
        print("converted_pdf_name : ", converted_pdf_name)
        print("converted_pdf_path : ", converted_pdf_path)
        save_DocDetails_to_DB(converted_pdf_name, request, "PDF")
    else:
        return render(request, 'EXCELtoPDF.html')

########################################################################################
