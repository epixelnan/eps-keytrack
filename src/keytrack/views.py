from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import redirect
from django.shortcuts import render
from django.views import View
from django.views.generic.edit import CreateView

from .models import Person, SelfRegisterRequest, SSHKey

class DashboardView(View):
	def get(self, request, *args, **kwargs):
		if not request.user.is_authenticated:
			return redirect('login/')

		person = Person.objects.get(user=request.user.id)
		
		cntxt = {}

		cntxt['person']  = person
		cntxt['sshkeys'] = SSHKey.objects.filter(owner=person.id)
		
		return render(request, 'dashboard.html', cntxt)

class RegisterView(CreateView):
	model = SelfRegisterRequest
	fields = '__all__'
	
	def form_valid(self, form):
		form.save()
	
		sentCount = send_mail(
			'Registration Request Submitted',
			'Your request to open an account on Epixel Keytrack has been submitted. '
				'The support team will get back soon. Make sure to let us know if this '
				'was not submitted by you.\r\n\r\nThank you.',
			settings.EPS_EMAIL_FROM,
			[form.cleaned_data['email']],
			fail_silently=True,
		)

		# TODO proper logging
		if sentCount != 1:
			'error: could not send email to: ' + form.cleaned_data['email']

		# TODO let the user know if error occured

		return render(self.request, 'user/register_success.html')

class RegisterRequestsView(View):
	def get(self, request, *args, **kwargs):
		cntxt = { 'regreqs': SelfRegisterRequest.objects.all() }
		
		return render(request, 'admin/regreqs.html', cntxt)
