from django.views.generic.list import ListView

from keytrack.models import Person
from keytrack.models import Project

from .admin_mixins import AdminOnlyMixin
from .anyprofileview import AnyProfileViewBase

class PeopleView(AdminOnlyMixin, ListView):
	model = Person
	template_name = 'admin/generic-list.html'
	
	def get_context_data(self, **kwargs):
		cntxt = super().get_context_data(**kwargs)
		cntxt['heading'] = 'People'
		cntxt['class_plural'] = 'people'
		cntxt['urlpattern'] = 'dashboard.admin.anyprofile'
		
		return cntxt

class ProjectsView(AdminOnlyMixin, ListView):
	model = Project
	template_name = 'admin/generic-list.html'
	
	def get_context_data(self, **kwargs):
		cntxt = super().get_context_data(**kwargs)
		cntxt['heading'] = 'Projects'
		cntxt['class_plural'] = 'projects'
		
		return cntxt

class AnyProfileView(AdminOnlyMixin, AnyProfileViewBase):
	def get(self, request, *args, **kwargs):
		self.uid = self.kwargs['pk']
		return super().get(request, *args, **kwargs)
