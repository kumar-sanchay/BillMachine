from django import forms
from .models import Company


class CreateCompanyForm(forms.ModelForm):
    company_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'input'}), label='Company Name*')
    company_email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'input'}), label='Company Email*')
    mobile = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'input'}), label='Mobile*')
    tel = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'input'}), required=False)
    gstin_no = forms.CharField(widget=forms.TextInput(attrs={'class': 'input'}), required=False)
    pan_no = forms.CharField(widget=forms.TextInput(attrs={'class': 'input'}), required=False)
    bank_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'input'}), required=False)
    account_no = forms.CharField(widget=forms.TextInput(attrs={'class': 'input'}), required=False)
    gst = forms.CharField(widget=forms.TextInput(attrs={'class': 'input', 'placeholder': 'in Percentage(%)'}),
                          required=False, label='GST')
    cgst_no = forms.CharField(widget=forms.TextInput(attrs={'class': 'input', 'placeholder': 'in Percentage(%)'}),
                              required=False, label='CGST')
    sgst_no = forms.CharField(widget=forms.TextInput(attrs={'class': 'input', 'placeholder': 'in Percentage(%)'}),
                              required=False, label='SGST')
    igst_no = forms.CharField(widget=forms.TextInput(attrs={'class': 'input', 'placeholder': 'in Percentage(%)'}),
                              required=False, label='IGST')
    ifsc_code = forms.CharField(widget=forms.TextInput(attrs={'class': 'input'}), required=False)
    state_code = forms.CharField(widget=forms.TextInput(attrs={'class': 'input'}), required=False)
    country_code = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'input'}), required=False)
    invoice_no = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'input',
                                                                    'placeholder': 'Initial invoice no. Default is 0'})
                                    , required=False)
    city = forms.CharField(widget=forms.TextInput(attrs={'class': 'input'}), label='City*')
    state = forms.CharField(widget=forms.TextInput(attrs={'class': 'input'}), label='State*')
    pincode = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'input'}), label='Pincode*')
    address = forms.CharField(widget=forms.Textarea(attrs={'class': 'input-address'}), required=False)

    class Meta:
        model = Company
        exclude =['user', 'active', 'slug', 'signature']

    def __init__(self, *args, **kwargs):
        super(CreateCompanyForm, self).__init__(*args, **kwargs)
    #     for x, y in kwargs['data'].items():
    #         if x in self.fields.keys():
    #             # self.fields[x] = y
    #             print(self.fields[x])


class SearchFieldForm(forms.Form):
    choices = ()

    def __init__(self, choice):
        super().__init__()
        SearchFieldForm.choices = choice

    radio = forms.ChoiceField(label='', widget=forms.RadioSelect(choices=choices))
