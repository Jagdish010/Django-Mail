from django.db.models import F, ExpressionWrapper, fields
from django.template.loader import render_to_string
from datetime import datetime
from datetime import timedelta

from enquiry.models import CustomerFeedBack
from enquiry.controller.e_mail import send_mail

# from ..models import CustomerFeedBack
# from .controller.e_mail import send_mail

notify = ExpressionWrapper(
	F('date_created') + timedelta(minutes=60),
	output_field=fields.DateTimeField()
)

def send_review_notification():
	sys_time = datetime.now()
	feedback_list = CustomerFeedBack.objects.annotate(notify=notify).filter(feedback_notification=False, notify__lte=sys_time)
	
	for row in feedback_list:
		subject = 'Review for service provided for enquiry: {}'.format(row.enquiry_id.name)
		message = render_to_string('email/review.html', {'customer': row.enquiry_id.customer_name, 'name': row.name})
		send_mail(subject=subject, message=message, recipient=[row.enquiry_id.email_id], html_content=1)
		
		row.feedback_notification = True
		row.notify_time = sys_time
		row.save(update_fields=['feedback_notification', 'notify_time'])


# from enquiry.cron.review import send_review_notification
# send_review_notification()