from django.contrib import admin

from .models import Designation
from .models import Person
from .models import Project

admin.site.register(Designation)
admin.site.register(Person)
admin.site.register(Project)
