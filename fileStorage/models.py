from django.db import models
from company.models import Company
from authentication.models import UserModel


class FileStorage(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name='user_fileStorage', null=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='company_file')
    to = models.CharField(max_length=50, null=True)
    invoice_no = models.CharField(max_length=25, null=True)
    data = models.TextField(null=True)
    result = models.TextField(null=True)
    gst = models.CharField(max_length=15, null=True, blank=True)
    cgst = models.CharField(max_length=15, null=True, blank=True)
    sgst = models.CharField(max_length=15, null=True, blank=True)
    igst = models.CharField(max_length=15, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'File Storage'
        verbose_name_plural = 'Files Storage'

    def __str__(self):
        return 'FileStorage:{}:{}'.format(self.company.company_name, self.pk)