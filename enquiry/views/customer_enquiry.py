# from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta

from ..forms.customer_enquiry import *
from ..forms.review import *
from ..models import CustomerEnquiry


def CustomerEnquiryView(request):
	form = CustomerEnquiryForm()
	storage = messages.get_messages(request)
	storage.used = True

	if request.method == 'POST':
		form = CustomerEnquiryForm(request.POST)
		if form.is_valid():
			form.save()
			
			# try:
			# 	pass
			# 	# send_mail('TEST', 'TESTT', 'jagdishrajalingam010@yahoo.com', ['jagdishrajalingam010@gmail.com'])
			# except BadHeaderError:
			# 	return HttpResponse('Invalid header found.')
			messages.success(request, 'Customer Complain Register Successfully')
			form = CustomerEnquiryForm()
			return render(request, "customer_enquiry/enquiry.html", {'form': form})

	return render(request, "customer_enquiry/enquiry.html", {'form': form})


def EnquiryFeedBackView(request, enquiryID):
	form = EnquiryFeedBackForm(request.POST or None, initial={'enquiry_id': enquiryID})

	storage = messages.get_messages(request)
	storage.used = True

	try:
		cust_q = CustomerEnquiry.objects.get(name=enquiryID)
	except:
		messages.add_message(request, messages.ERROR, 'Customer Enquiry ID is not valid')
	
	if form.is_valid():
		form.save()
		form = EnquiryFeedBackForm(None, initial={'enquiry_id': enquiryID})
		messages.success(request, 'Mail Notification Send Successfully')
	
	return render(request, "customer_enquiry/enquiry_feedback.html", {'form': form})


def EnquiryReviewView(request, feedbackID):
	form = EnquiryReviewForm(request.POST or None)

	storage = messages.get_messages(request)
	storage.used = True

	cust_q = None
	try:
		cust_q = CustomerFeedBack.objects.get(name=feedbackID)
	except:
		messages.add_message(request, messages.ERROR, 'Feedback ID is not valid')

	send_review = 0
	if cust_q:
		if cust_q.feedback_notification:
			expiry_time = cust_q.notify_time + timedelta(minutes=30)
			if (expiry_time < timezone.now()):
				# raise Http404('URL Expired')
				messages.add_message(request, messages.ERROR, 'Review URL is Expired')
			else:
				if int(cust_q.customer_satisfaction) != 0:
					return HttpResponse('Customer Review Already recorded')
				send_review = 1
		else:
			messages.add_message(request, messages.ERROR, 'Notification has not been created to review')
	
	if form.is_valid():
		form.save(feedbackID=feedbackID)

		return HttpResponse('Customer Review is been Updated')
	
	context = {'create_form': send_review, 'form': form}
	return render(request, "customer_enquiry/enquiry_review.html", context)
	
