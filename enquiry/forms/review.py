from django import forms
from ..models import CustomerFeedBack

_CHOICES = (
	("1", "Satisfied"),
	("2", "Unsatisfied")
)

class EnquiryReviewForm(forms.Form):
	satisfy = forms.ChoiceField(choices = _CHOICES, required=True)

	def save(self, *args, **kwargs):
		cust_q = CustomerFeedBack.objects.get(name=kwargs.get('feedbackID'))

		cust_q.customer_satisfaction = self.cleaned_data['satisfy']
		cust_q.save(update_fields=['customer_satisfaction'])
		
