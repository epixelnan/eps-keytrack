from django.views.generic.list import ListView

from keytrack.models import Person
from keytrack.models import Project

from .admin_mixins import AdminOnlyMixin

class PeopleView(AdminOnlyMixin, ListView):
	model = Person
	template_name = 'admin/generic-list.html'
	
	def get_context_data(self, **kwargs):
		cntxt = super().get_context_data(**kwargs)
		cntxt['heading'] = 'People'
		cntxt['class_plural'] = 'people'
		
		return cntxt

class ProjectsView(ListView):
	model = Project
	template_name = 'admin/generic-list.html'
	
	def get_context_data(self, **kwargs):
		cntxt = super().get_context_data(**kwargs)
		cntxt['heading'] = 'Projects'
		cntxt['class_plural'] = 'projects'
		
		return cntxt
