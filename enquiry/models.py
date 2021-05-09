from django.db import models
from django.core.validators import validate_email
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField
from django.template.loader import render_to_string

from .controller.e_mail import send_mail

# Create your models here.

class CustomerEnquiry(models.Model):
	# name, phone number, email id and query.
	name = models.AutoField(primary_key=True)
	customer_name = models.CharField(_('Customer Name'), blank=False, max_length=200)
	phone = PhoneNumberField(_('Phone Number'), null=False, blank=False)
	email_id = models.EmailField(_('Email ID'), blank=False, validators=[validate_email])
	
	query = models.TextField(_('Customer Query'), blank=False)

	date_created = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return 'Customer {} enquiry registration {} Created'.format(self.customer_name, self.name)
	

	def save(self, *args, **kwargs):
		# if self.email_id: return
		super(CustomerEnquiry, self).save(*args, **kwargs)

		self.send_notification()

	
	def send_notification(self):
		subject = 'Customer Enquiry: {}'.format(self.name)
		
		message = render_to_string('email/customer_enquiry.html', {'query': self.query, 'customer_name': self.customer_name, 'name': self.name})
		send_mail(subject=subject, message=message, recipient=['abc@gmail.com'], html_content=1)


class CustomerFeedBack(models.Model):
	name = models.AutoField(primary_key=True)
	enquiry_id = models.ForeignKey(CustomerEnquiry, blank=False, on_delete=models.CASCADE)
	feedback = models.TextField(_('Feedback'), blank=False)
	feedback_notification = models.BooleanField(_('Satisfaction Mail'), default=False)
	notify_time = models.DateTimeField(_('Notification Send Time'), blank=True, null=True)
	

	_CHOICES = (
		("0", ''),
		("1", "Satisfied"),
		("2", "Unsatisfied")
	)
	customer_satisfaction = models.CharField(_('Customer Satisfication'), max_length=1, choices=_CHOICES, default=0)

	date_created = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return '{}'.format(self.name)


	def save(self, *args, **kwargs):
		send_email = self._state.adding is True and self.name is None

		super(CustomerFeedBack, self).save(*args, **kwargs)
		
		if send_email:
			self.send_notification()


	def send_notification(self):
		enquiryID = self.enquiry_id.name
		subject = 'Customer Feedback: {}'.format(self.enquiry_id.name)
		
		message = render_to_string('email/feedback.html', {'feedback': self.feedback, 'customer': self.enquiry_id.customer_name})
		send_mail(subject=subject, message=message, recipient=[self.enquiry_id.email_id], html_content=1)