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
