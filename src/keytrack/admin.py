from django.contrib import admin

from .models import Host
from .models import Repository
from .models import Project
from .models import Designation
from .models import Person
from .models import SSHKey

from django import forms

from django.contrib.admin.widgets import FilteredSelectMultiple

from django_better_admin_arrayfield.admin.mixins import DynamicArrayMixin
from django_better_admin_arrayfield.forms.widgets import DynamicArrayWidget

admin.site.register(Host)
admin.site.register(Repository)
admin.site.register(Project)
admin.site.register(Designation)
admin.site.register(SSHKey)

class PersonAdminForm(forms.ModelForm, DynamicArrayMixin):
	class Meta:
		model   = Person
		widgets = {
			# is_stacked=False => lists placed horizontally
			'projects': FilteredSelectMultiple('Projects', is_stacked=False),

			'projects_with_live_server_access':
				FilteredSelectMultiple('Projects', is_stacked=False),

			'projects_with_db_access':
				FilteredSelectMultiple('Projects', is_stacked=False),

			'repos_with_read_access':
				FilteredSelectMultiple('Repositories', is_stacked=False),

			'repos_with_write_access':
				FilteredSelectMultiple('Repositories', is_stacked=False),
			
			'jenkins_urls':
				DynamicArrayWidget(),
		}
		fields  = '__all__'

class PersonAdmin(admin.ModelAdmin):
	form = PersonAdminForm

admin.site.register(Person, PersonAdmin)
