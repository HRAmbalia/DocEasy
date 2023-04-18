#organizePDFApp
from django.shortcuts import render

# importing modules
import os
from django.core.files.storage import FileSystemStorage
from datetime import datetime
from django.http import FileResponse
from pylovepdf.ilovepdf import ILovePdf # to Split PDF
from PyPDF2 import PdfFileMerger, PdfFileReader # to Merge PDF
import fitz # to Remove pages from PDF
import requests, json # to Watermark PDF
from PIL import Image
from homePageApp.models import uploaded_DocDetails
MEDIA_PATH = os.path.join(os.getcwd(), "media", "")

########################################################################################

# Create your views here.
    # organizePDFApp : 
    # MERGE PDF
    # SPLIT PDF
    # REMOVE PAGES FROM PDF
    # WATERMARK PDF

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

#Merge PDF##############################################################################
#DOnE

def MergePDF_Func(uploaded_pdf_list):
    merged_pdf_name = uploaded_pdf_list[0].replace(".pdf","-merged.pdf")
    merged_pdf_path = MEDIA_PATH + merged_pdf_name
    merger = PdfFileMerger()
    for pdf in uploaded_pdf_list:
        pdf_path = MEDIA_PATH + pdf
        merger.append(PdfFileReader(open(pdf_path, 'rb')))
    merger.write(merged_pdf_path)
    delete_Files(uploaded_pdf_list)  # deletes user uploaded files
    return merged_pdf_name, merged_pdf_path

def MergePDF(request):
    if request.method == 'POST' and request.FILES['PDFs']:
        uploaded_pdfs_list = []
        fs = FileSystemStorage()
        uploaded_pdfs = request.FILES.getlist('PDFs')
        for pdf in uploaded_pdfs:
            newFileName = pdf.name.replace(".pdf",(return_Time()+".pdf"))
            filename = fs.save(newFileName, pdf)
            uploaded_pdfs_list.append(newFileName)
        merged_pdf_name, merged_pdf_path = MergePDF_Func(uploaded_pdfs_list)
        print("merged_pdf_name : ", merged_pdf_name)
        print("merged_pdf_path : ", merged_pdf_path)
        save_DocDetails_to_DB(merged_pdf_name, request, "PDF") # Saves pdf details to database
    else:
        return render(request, 'MergePDF.html')

#Split PDF##############################################################################
#DOnE

def SplitPDF_Func(filename):
    pdf_path = MEDIA_PATH + filename
    print("pdf_path : ", pdf_path)
    public_key = 'project_public_0eed65dc44084dc02fccb90b7d4c7f3c_WMfTObe104a679401ae2b10300f3e09ecce2a'
    ilovepdf = ILovePdf(public_key, verify_ssl=True)
    task = ilovepdf.new_task('split')
    task.add_file(pdf_path)
    task.set_output_folder(MEDIA_PATH)
    task.execute()
    splitted_zipfile_name = task.download()
    # print("splitted_zipfile_name : ", splitted_zipfile_name)
    task.delete_current_task()
    splitted_zipfile_path = MEDIA_PATH + splitted_zipfile_name
    # print("splitted_zipfile_path : ", splitted_zipfile_path)
    #
    to_delete_files = []
    to_delete_files.append(filename)
    delete_Files(to_delete_files)  # deletes user uploaded files
    #
    return splitted_zipfile_name, splitted_zipfile_path

def SplitPDF(request):
    if request.method == 'POST' and request.FILES['myPDF']:
        fs = FileSystemStorage()
        uploaded_pdf = request.FILES['myPDF']
        newFileName = uploaded_pdf.name.replace(".pdf",(return_Time()+".pdf"))
        file_name = fs.save(newFileName, uploaded_pdf) # Saving uploaded file with updated unique names
        splitted_zipfile_name, splitted_zipfile_path = SplitPDF_Func(file_name)
        print("splitted_zipfile_name : ", splitted_zipfile_name)
        print("splitted_zipfile_path : ", splitted_zipfile_path)
        save_DocDetails_to_DB(splitted_zipfile_name, request, "ZIP")
        # converted_pdf = open(splitted_zipfile_name, 'rb')
        # return FileResponse(splitted_zipfile_name, content_type='application')
    else:
        return render(request, 'SplitPDF.html')

#Remove Pages From PDF##################################################################
#DOnE

def RemovePagesFromPDF_Func(filename, pageno):
    pdf_path = MEDIA_PATH + filename
    new_pdf_name = filename.replace('.pdf','-new.pdf')
    new_pdf_path = MEDIA_PATH + new_pdf_name
    print("pageno : ", pageno)
    #finding total number of pages in PDF
    with open(pdf_path, 'rb') as fl:
        reader = PdfFileReader(fl)
        total_pages = reader.getNumPages()
    #finding pages to keep
    pages_to_keep = []
    for i in range(0, total_pages):
        pages_to_keep.append(i)
    #removing given page
    if (pageno <= total_pages and pageno > 0):
        pages_to_keep.remove(pageno-1)
    #if pageno is not valid then returns original pdf
    print("pages_to_keep : ", pages_to_keep)
    f = fitz.open(pdf_path)
    pgls = pages_to_keep
    f.select(pgls)
    f.save(new_pdf_path)
    #
    to_delete_files = []
    to_delete_files.append(filename)
    delete_Files(to_delete_files)  # deletes user uploaded files
    #
    return new_pdf_name, new_pdf_path
    

def RemovePagesFromPDF(request):
    if request.method == 'POST' and request.FILES['myfile']:
        fs = FileSystemStorage()
        uploaded_pdf = request.FILES['myfile']
        pageno = int(request.POST['pageno'])
        newFileName = uploaded_pdf.name.replace(".pdf",(return_Time()+".pdf"))
        file_name = fs.save(newFileName, uploaded_pdf) # Saving uploaded file with updated unique name
        new_pdf_name, new_pdf_path = RemovePagesFromPDF_Func(file_name, pageno)
        print("new_pdf_name : ", new_pdf_name)
        print("new_pdf_path : ", new_pdf_path)
        save_DocDetails_to_DB(new_pdf_name, request, "PDF")
        # converted_pdf = open(new_pdf_path, 'rb')
        # return FileResponse(converted_pdf, content_type='application/pdf')
    else:
        return render(request, 'RemovePagesFromPDF.html')

#Watermark PDF##########################################################################
#DOnE

def WatermarkPDF_Func(filename, imagename):
    pdf_path = MEDIA_PATH + filename
    image_path = MEDIA_PATH + imagename
    watermarked_pdf_name = filename.replace('.pdf','-watermarked.pdf')
    watermarked_pdf_path = MEDIA_PATH + watermarked_pdf_name
    instructions = {
        'parts': [
            {
                'file': 'document'
            }
        ],
        'actions': [
            {
                'type': 'watermark',
                'image': 'logo',
                'width': '25%'
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
            'document': open(pdf_path, 'rb'),
            'logo': open(image_path, 'rb')
        },
        data={
            'instructions': json.dumps(instructions)
        },
        stream=True
    )
    if response.ok:
        with open(watermarked_pdf_path, 'wb') as fd:
            for chunk in response.iter_content(chunk_size=8096):
                fd.write(chunk)
    else:
        print(response.text)
        exit()
    #
    to_delete_files = []
    to_delete_files.append(filename)
    to_delete_files.append(imagename)
    delete_Files(to_delete_files)  # deletes user uploaded files
    #
    return watermarked_pdf_name, watermarked_pdf_path

def WatermarkPDF(request):
    if request.method == 'POST' and request.FILES['myPDF']:
        fs = FileSystemStorage()
        uploaded_pdf = request.FILES['myPDF']
        uploaded_watermark = request.FILES['mywatermark']
        # img = Image.open(uploaded_watermark)
        # image_format = img.format
        newFileName = uploaded_pdf.name.replace(".pdf",(return_Time()+".pdf"))
        file_name = fs.save(newFileName, uploaded_pdf) # Saving uploaded pdf file with updated unique name
        image_name = fs.save(uploaded_watermark.name, uploaded_watermark)
        watermarked_pdf_name, watermarked_pdf_path = WatermarkPDF_Func(file_name, image_name)
        print("watermarked_pdf_name : ", watermarked_pdf_name)
        print("watermarked_pdf_path : ", watermarked_pdf_path)
        save_DocDetails_to_DB(watermarked_pdf_name, request, "PDF")
        # converted_pdf = open(new_pdf_path, 'rb')
        # return FileResponse(converted_pdf, content_type='application/pdf')
    else:
        return render(request, 'WatermarkPDF.html')

########################################################################################
