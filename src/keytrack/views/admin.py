from django.views.generic.list import ListView
from keytrack.models import Person

from keytrack.models import Person

class PeopleView(ListView):
	model = Person
	template_name = 'admin/generic-list.html'
	
	def get_context_data(self, **kwargs):
		cntxt = super().get_context_data(**kwargs)
		cntxt['heading'] = 'People'
		cntxt['obj_type_name'] = 'people'
		
		return cntxt
