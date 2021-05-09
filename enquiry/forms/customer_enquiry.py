from django.forms import ModelForm
from phonenumber_field.formfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberPrefixWidget

from ..models import CustomerEnquiry, CustomerFeedBack


class CustomerEnquiryForm(ModelForm):
	phone = PhoneNumberField(
		widget=PhoneNumberPrefixWidget(initial='IN')
	)
	
	class Meta:
		model = CustomerEnquiry
		fields = '__all__'


class EnquiryFeedBackForm(ModelForm):
	class Meta:
		model = CustomerFeedBack
		fields = ['enquiry_id', 'feedback']