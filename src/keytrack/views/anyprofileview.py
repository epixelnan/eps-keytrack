from django.views.generic.detail import DetailView
from django.shortcuts import render

from keytrack.models import Host
from keytrack.models import Person
from keytrack.models import SSHKey

import logging

logger = logging.getLogger(__name__)

def get_person_for_user_id(uid):
	try:
		return Person.objects.get(user=uid)
	except Exception as e:
		logger.error('could not get Person object for user=' +
			str(uid) + ': ' + str(e))

	return None

class AnyProfileViewBase(DetailView):
	model = Person
	template_name = 'dashboard-profile.html'
	
	def get(self, request, *args, **kwargs):
		person = get_person_for_user_id(self.uid)
		if person == None:
			return render(request, 'dashboard_500.html', status=500)

		self.object = person

		# I referred the django source
		cntxt = self.get_context_data(object=self.object)
		cntxt['fields'] = self.model._meta.fields
		
		# Many-to-many fields are not present in self.model._meta.fields
		
		lists = [
			{
				'heading':          'Managers',
				'items':            self.object.managers.all(),
				'item_name_plural': 'managers',
			},
			{
				'heading':          'Projects',
				'items':            self.object.projects.all(),
				'item_name_plural': 'projects',
			},
			{
				'heading':          'Projects with Live Server Access',
				'items':            self.object.projects_with_live_server_access.all(),
				'item_name_plural': 'projects with live server access',
			},
			{
				'heading':          'Projects with Database Access',
				'items':            self.object.projects_with_db_access.all(),
				'item_name_plural': 'projects with database access',
			},
			{
				'heading':          'Repos with Read Access',
				'items':            self.object.repos_with_read_access.all(),
				'item_name_plural': 'repos with read access',
			},
			{
				'heading':          'Repos with Write Access',
				'items':            self.object.repos_with_write_access.all(),
				'item_name_plural': 'repos with write access',
			},
		]
		
		cntxt['lists'] = lists

		cntxt['hosts'] = Host.objects.filter(owner=self.object.id)
		cntxt['sshkeys'] = SSHKey.objects.filter(owner=self.object.id)

		return self.render_to_response(cntxt)
