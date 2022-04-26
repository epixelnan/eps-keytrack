from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.shortcuts import render
from django.views import View
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView

from keytrack.models import Person, SelfRegisterRequest, SSHKey

from .admin_process_regreqs import *

def get_person_for_user(user):
	try:
		return Person.objects.get(user=user.id)
	except Exception as e:
		logger.error('could not get Person object for user=' +
			str(user.id) + ': ' + e.message)

	return None

class DashboardView(View):
	def get(self, request, *args, **kwargs):
		if not request.user.is_authenticated:
			return redirect('login/')

			person = get_person_for_user(request.user)
			if person == None:
				return render(request, 'dashboard_500.html', status=500)
		
		cntxt = {}

		cntxt['person']  = person
		cntxt['sshkeys'] = SSHKey.objects.filter(owner=person.id)
		
		if request.user.is_staff:
			cntxt['regReqCount'] = SelfRegisterRequest.objects.count()

		return render(request, 'dashboard.html', cntxt)

class ProfileView(DetailView):
	model = Person
	template_name = 'dashboard-profile.html'
	
	def get(self, request, *args, **kwargs):
		person = get_person_for_user(request.user)
		if person == None:
			return render(request, 'dashboard_500.html', status=500)

		self.object = person

		# I referred the django source
		cntxt = self.get_context_data(object=person)
		cntxt['fields'] = self.model._meta.fields
		return self.render_to_response(cntxt)

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
