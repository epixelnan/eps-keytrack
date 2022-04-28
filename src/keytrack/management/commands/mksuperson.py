from django.core.management.base import BaseCommand, CommandError

from django.contrib.auth.models import User
from keytrack.models import Person


class Command(BaseCommand):
	help = 'Creates Person object for the superuser'

	def handle(self, *args, **options):
		su = User.objects.filter(is_superuser=True)
		if len(su) <= 0:
			raise CommandError('No superuser found')
		
		su_person = Person.objects.filter(user=su[0])
		if len(su_person) <= 0:
			Person.objects.create(user=su[0], name='admin')
			self.stdout.write(self.style.SUCCESS('Created Person for the superuser.'))
		else:
			self.stdout.write(
				self.style.NOTICE('Person already exists for the superuser.'))
