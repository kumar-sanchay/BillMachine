from django.db import models
from django.conf import settings
from PIL import Image
from django.urls import reverse
from django.utils.text import slugify


class Company(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='company_user')
    company_name = models.CharField(max_length=50, verbose_name='Company Name')
    slug = models.SlugField(blank=True, null=True, unique=True)
    company_email = models.EmailField(unique=True, blank=True, null=True, verbose_name='Company Email')
    address = models.TextField(blank=True, null=True, verbose_name='Address')
    mobile = models.DecimalField(max_digits=10, decimal_places=0, verbose_name='Mobile')
    tel = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True, verbose_name='Tel')
    pincode = models.DecimalField(max_digits=6, decimal_places=0, blank=True, null=True, verbose_name='Pincode')
    city = models.CharField(max_length=25, null=True, blank=True, verbose_name='City')
    state = models.CharField(max_length=25, null=True, blank=True, verbose_name='State')
    gstin_no = models.CharField(max_length=15, blank=True, null=True, verbose_name='GSTIN No')
    gst = models.CharField(max_length=15, blank=True, null=True, verbose_name='GST')
    pan_no = models.CharField(max_length=10, blank=True, null=True, verbose_name='Pan No')
    cgst_no = models.CharField(max_length=25, null=True, blank=True, verbose_name='CGST')
    sgst_no = models.CharField(max_length=25, null=True, blank=True, verbose_name='SGST')
    igst_no = models.CharField(max_length=25, null=True, blank=True, verbose_name='IGST')
    bank_name = models.CharField(max_length=50, null=True, blank=True, verbose_name='Bank Name')
    account_no = models.CharField(max_length=12, blank=True, null=True, verbose_name='Account No')
    ifsc_code = models.CharField(max_length=11, blank=True, null=True, verbose_name='IFSC Code')
    state_code = models.CharField(max_length=6, blank=True, null=True, verbose_name='State Code')
    country_code = models.IntegerField(verbose_name='Country Code')
    signature = models.ImageField(upload_to='company/sign/', blank=True, null=True)
    invoice_no = models.IntegerField(default=0, verbose_name='Invoice No')
    created = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Company'
        verbose_name_plural = 'Companies'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.company_name)
        super(Company, self).save(*args, **kwargs)
        if self.signature:
            image = Image.open(self.signature)
            size = (50, 50)
            image = image.resize(size, Image.ANTIALIAS)
            image.save(self.signature.path)

    def get_absolute_url(self):
        return reverse('company:detail_company', args=[self.pk, self.slug])

    def get_search_url(self):
        return reverse('company:search_field_company', args=[self.pk, self.slug])

    def get_fields(self):
        # return [(field.name, field.value_to_string(self)) for field in Company._meta.fields]
        results = []
        for field in Company._meta.fields:
            if not field.name in ['id', 'slug', 'user', 'signature', 'active', 'created', 'invoice_no']:
                # results[field.name] = field.value_to_string(self)
                results.append((field.verbose_name, field.value_to_string(self)))
        return results

    def get_field_values(self):
        # return [(field.name, field.value_to_string(self)) for field in Company._meta.fields]
        results = []
        for field in Company._meta.fields:
            if not field.name in ['id', 'slug', 'user', 'signature', 'active', 'created', 'invoice_no']:
                # results[field.name] = field.value_to_string(self)
                results.append((field.verbose_name, field.value_to_string(self)))
        return results


class BillTitle(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='bill_company_title')
    title1 = models.CharField(max_length=10)
    title2 = models.CharField(max_length=10, blank=True, null=True)
    title3 = models.CharField(max_length=10, blank=True, null=True)
    title4 = models.CharField(max_length=10, blank=True, null=True)
    title5 = models.CharField(max_length=10, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Bill Title'
        verbose_name_plural = 'Bill Titles'

