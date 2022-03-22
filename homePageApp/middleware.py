import os
from datetime import datetime
from django.db import connection
from homePageApp.models import uploaded_DocDetails
MEDIA_PATH = os.path.join(os.getcwd(), "media", "")

def deleteUserDocuments(get_response):
    def middleware(request):
        # print("It's from deleteUserDocuments middleware")
        # uploaded_docDetails = uploaded_DocDetails.objects.all()
        # print("uploaded_docDetails : ", uploaded_docDetails)
        for p in uploaded_DocDetails.objects.raw('SELECT * from homePageApp_uploaded_docdetails where uploadedTime < now() - interval 7 hour'):
            print("p.filePath : ", p.filePath)
            os.remove(p.filePath) # takes path from DB and removes files from media folder
        cursor = connection.cursor()
        # deletes data which have upload time less than 7hours from now before
        # keeps data which haven't crossed 7 hours from upload time
        cursor.execute('''DELETE from homePageApp_uploaded_docdetails where uploadedTime < now() - interval 7 hour''') # removes tuple from DB itself
        response = get_response(request)
        return response
    return middleware
