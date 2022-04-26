from django import forms
from django.contrib.auth.models import User
from django.conf import settings
from django.core.mail import send_mail
from django.http import HttpResponse
from django.forms import ModelForm
from django.shortcuts import redirect
from django.shortcuts import render
from django.views import View
from django.views.generic.edit import CreateView, UpdateView
from django.urls import reverse

from .models import Person, SelfRegisterRequest, SSHKey

import logging

logger = logging.getLogger(__name__)

class DashboardView(View):
	def get(self, request, *args, **kwargs):
		if not request.user.is_authenticated:
			return redirect('login/')

		try:
			person = Person.objects.get(user=request.user.id)
		except Exception as e:
			logger.error('could not get Person object for user=' +
				str(request.user.id) + ': ' + e.message)
			return render(request, 'dashboard_500.html', status=500)
		
		cntxt = {}

		cntxt['person']  = person
		cntxt['sshkeys'] = SSHKey.objects.filter(owner=person.id)
		
		if request.user.is_staff:
			cntxt['regReqCount'] = SelfRegisterRequest.objects.count()

		return render(request, 'dashboard.html', cntxt)

def email_notif(to, subject, body):
	if not settings.EPS_EMAIL_ENABLED:
		logger.warning('not sending email because disabled by EPS_EMAIL_ENABLED: ' + to)
		return False

	if not to.split('@')[1] in settings.EPS_EMAIL_OK_DOMAINS:
		logger.warning('not sending email to disallowed domain: ' + to)
		
		return False

	sentCount = send_mail(
		subject,
		body,
		settings.EPS_EMAIL_FROM,
		[to],
		fail_silently=True,
	)

	if sentCount != 1:
		logger.error('could not send email to: ' + to)
		return False
	
	return True

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

class ProcessRegisterForm(ModelForm):
	CHOICES_REGPROCTYPE = [
		('update', 'Update'),
		('register', 'Update & Register'),
		('reject', 'Reject'),
	]

	submit_type = forms.ChoiceField(choices=CHOICES_REGPROCTYPE)

	class Meta:
		model = SelfRegisterRequest
		fields = '__all__'

class ProcessRegisterView(UpdateView):
	model = SelfRegisterRequest
	form_class = ProcessRegisterForm
	template_name = 'admin/process-regreq_form.html'

	def form_valid(self, form):
		subtype = form.cleaned_data['submit_type'] if 'submit_type' in form.cleaned_data else 'update'
		
		if subtype == 'register':
			login  = form.cleaned_data['email']
			passwd = User.objects.make_random_password()
			
			has_error = False
			
			try:
				user = User.objects.create_user(
					login,
					form.cleaned_data['email'],
					passwd)
			except Exception as e:		
				logger.error(e)
				has_error = True
		
			if has_error:
				form.add_error(None, 'could not create user account; '
				'make sure a user does not exist for the same email.')
			else:
				subject = 'Account Details'
				body = 'A user account has been created for you on '\
				'Epixel Keytrack. You can sign in with the following: \r\n\r\n'\
				'username: ' + login + '\r\n'\
				'password: ' + passwd + '\r\n\r\n'\
				'Thank you.'
				
				email_notif(form.cleaned_data['email'], subject, body)
			
			if not has_error:
				try:
					person = Person.objects.create(user=user,
						epsid=form.cleaned_data['epsid'],
						name=form.cleaned_data['name'],
						designation=form.cleaned_data['designation'])

					person.managers.set(form.cleaned_data['managers'])
					person.projects.set(form.cleaned_data['projects'])

				except Exception as e:
					logger.error(e)
					has_error = True

					form.add_error(None, 'created the user account, '
					'but creation of Person object failed (may be duplicate epsid?); '
					'you will have to do it manually.')

			if has_error:
				if form.is_valid():
					form.save() # save updates if any
				
				cntxt = super().get_context_data()
				cntxt['form'] = form
				return render(self.request, self.template_name, cntxt)
			else:
				self.get_object().delete()
		
			return redirect('dashboard.admin.regreqs')

		elif subtype == 'reject':
			self.get_object().delete()

			subject = 'Registration Request Rejected'
			body = 'Your request to open an account on Epixel Keytrack '\
			'has been rejected for some reason. Please contact the support team '\
			'for more information.'\
			'\r\n\r\nThank you.'

			email_notif(form.cleaned_data['email'], subject, body)

			return redirect('dashboard.admin.regreqs')

		else: # update
			form.save()
			return redirect(reverse('dashboard.admin.regreq',
				args=[self.get_object().pk]))

class RegisterRequestsView(View):
	def get(self, request, *args, **kwargs):
		cntxt = { 'regreqs': SelfRegisterRequest.objects.all() }
		
		return render(request, 'admin/regreqs.html', cntxt)
