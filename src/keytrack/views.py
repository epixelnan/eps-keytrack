from django import forms
from django.contrib.auth.models import User
from django.conf import settings
from django.core.mail import send_mail
from django.forms import ModelForm
from django.shortcuts import redirect
from django.shortcuts import render
from django.views import View
from django.views.generic.edit import CreateView, UpdateView
from django.urls import reverse

from .models import Person, SelfRegisterRequest, SSHKey

class DashboardView(View):
	def get(self, request, *args, **kwargs):
		if not request.user.is_authenticated:
			return redirect('login/')

		person = Person.objects.get(user=request.user.id)
		
		cntxt = {}

		cntxt['person']  = person
		cntxt['sshkeys'] = SSHKey.objects.filter(owner=person.id)
		
		if request.user.is_staff:
			cntxt['regReqCount'] = SelfRegisterRequest.objects.count()

		return render(request, 'dashboard.html', cntxt)

def email_notif(to, subject, body):
	if not to.split('@')[1] in settings.EPS_EMAIL_OK_DOMAINS:
		# TODO proper logging
		print('info: not sending email to disallowed domain: ' + to)
		
		return False

	sentCount = send_mail(
		subject,
		body,
		settings.EPS_EMAIL_FROM,
		[to],
		fail_silently=True,
	)

	# TODO proper logging
	if sentCount != 1:
		print('error: could not send email to: ' + to)
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
		print(form.cleaned_data) # TODO REM
		print(form.cleaned_data['submit_type'])
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
			except:		
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
						name=form.cleaned_data['name'],
						designation=form.cleaned_data['designation'])

					person.managers.set(form.cleaned_data['managers'])
					person.managers.projects.set(form.cleaned_data['projects'])

					self.get_object().delete()
				
				except:
					form.save() # save updates if any

					form.add_error(None, 'created the user account, '
					'but creation of Person object failed; you will have to do it '
					'manually.')

			if has_error:
				cntxt = super().get_context_data()
				cntxt['form'] = form
				return render(self.request, self.template_name, cntxt)
		
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
			return redirect(reverse('dashboard.admin.regreq',
				args=[self.get_object().pk]))

class RegisterRequestsView(View):
	def get(self, request, *args, **kwargs):
		cntxt = { 'regreqs': SelfRegisterRequest.objects.all() }
		
		return render(request, 'admin/regreqs.html', cntxt)
