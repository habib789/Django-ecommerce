from django import forms

PAYMENT_CHOICES = (
    ('s', 'Stripe'),
    ('c', 'Cash on delivery'),
)


class BillingForm(forms.Form):
    customer_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    contact_no = forms.CharField(widget=forms.NumberInput(attrs={'class': 'form-control'}))
    street_address = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    country = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    zip = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    payment = forms.ChoiceField(widget=forms.RadioSelect(), choices=PAYMENT_CHOICES)
