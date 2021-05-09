from django.urls import path
from .views.customer_enquiry import CustomerEnquiryView, EnquiryReviewView, EnquiryFeedBackView

urlpatterns = [
	path('cust_enquiry/', CustomerEnquiryView, name='customer-enquiry'),
	path('enquiry_feedback/<str:enquiryID>/', EnquiryFeedBackView, name='enquiry-feedback'),
	path('enquiry_review/<str:feedbackID>/', EnquiryReviewView, name='enquiry-review'),
]