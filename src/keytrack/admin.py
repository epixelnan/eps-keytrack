from django.contrib import admin

from .models import Designation
from .models import Person
from .models import Project

from django import forms

from django.contrib.admin.widgets import FilteredSelectMultiple

admin.site.register(Designation)
admin.site.register(Project)

class PersonAdminForm(forms.ModelForm):
	class Meta:
		model   = Person
		widgets = {
			# is_stacked=False => lists placed horizontally
			'projects': FilteredSelectMultiple('Projects', is_stacked=False),

			'projects_with_live_server_access':
				FilteredSelectMultiple('Projects', is_stacked=False),

			'projects_with_db_access':
				FilteredSelectMultiple('Projects', is_stacked=False),
		}
		fields  = '__all__'

class PersonAdmin(admin.ModelAdmin):
	form = PersonAdminForm

admin.site.register(Person, PersonAdmin)
