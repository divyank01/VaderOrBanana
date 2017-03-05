from django.db import models
#import scipy

class Upload(models.Model):
    docfile = models.FileField(upload_to='documents',name='data')