from django import forms


class EmployeeForm(forms.Form):
    first_name = forms.CharField(max_length=100, required=True)
    last_name = forms.CharField(max_length=100, required=True)
    date_of_birth = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), required=True)
    email = forms.EmailField(required=True)
    position = forms.CharField(max_length=100, required=True)
    phone_number = forms.CharField(max_length=15, required=True)
    passport_expiry_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), required=True)
    brp_expiry_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), required=True)
    passport_document = forms.FileField(required=True)
    brp_document = forms.FileField(required=True)
