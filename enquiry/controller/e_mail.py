from django.core.mail import EmailMessage, BadHeaderError
from django.conf import settings


def send_mail(**kwargs):
	email = EmailMessage(
		kwargs.get('subject'),
		kwargs.get('message'),
		settings.EMAIL_HOST_USER,
		kwargs.get('recipient')
		)
	
	if int(kwargs.get('html_content') or 0):
		email.content_subtype = "html"  # Main content is now text/html


	email.fail_silently = False

	try:
		email.send()
	except BadHeaderError:
		return HttpResponse('Invalid header found.')
