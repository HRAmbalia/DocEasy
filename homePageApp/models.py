from django.db import models

# Create your models here.
from datetime import date, datetime  

class uploaded_DocDetails(models.Model):
    ID = models.AutoField(primary_key=True) 
    fileName = models.CharField(max_length=1000)
    filePath = models.CharField(max_length=4000)
    typrOfFile = models.CharField(max_length=500)
    uploadedTime = models.DateTimeField(auto_now_add=True, blank=True)
    UserName = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        if self.UserName:
            return self.UserName+' --> '+self.fileName
        else:
            return self.fileName