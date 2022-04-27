from django.conf import settings
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.shortcuts import render
from django.views import View
from django.views.generic.edit import CreateView

from keytrack.models import Person, SelfRegisterRequest

from .admin import *
from .admin_process_regreqs import *
from .anyprofileview import *

class DashboardView(View):
	def get(self, request, *args, **kwargs):
		cntxt = {}

		if not request.user.is_authenticated:
			return redirect('login/')

		person = get_person_for_user_id(request.user.id)
		if person == None:
			return render(request, 'dashboard_500.html', status=500)

		cntxt['person']  = person
		
		if request.user.is_staff:
			cntxt['regReqCount'] = SelfRegisterRequest.objects.count()

		return render(request, 'dashboard.html', cntxt)

class OwnProfileView(AnyProfileViewBase):
	def get(self, request, *args, **kwargs):
		self.uid = request.user.id
		return super().get(request, *args, **kwargs)

class RegisterView(CreateView):
	model = SelfRegisterRequest
	fields = '__all__'
	template_name = 'user/register_form.html'
	
	def form_valid(self, form):
		form.save()
		
		subject = 'Registration Request Submitted'
		body = 'Your request to open an account on Epixel Keytrack '\
		'has been submitted. The support team will get back soon. '\
		'Make sure to let us know if this was not submitted by you.'\
		'\r\n\r\nThank you.'
		
		email_notif(form.cleaned_data['email'], subject, body)

		# TODO let the user know if error occured

		return render(self.request, 'user/register_success.html')

class SecureLogoutView(View):
	http_method_names = ['post']
	
	def post(self, request):
		auth_logout(request)
		return redirect(settings.LOGOUT_REDIRECT_URL)
