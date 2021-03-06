from django.db import models
from django.conf import settings
from django_better_admin_arrayfield.models.fields import ArrayField

class Repository(models.Model):
	url = models.CharField(max_length=4096)

	def __str__(self):
		return self.url

class Project(models.Model):
	name  = models.CharField(max_length=256)

	frameworks = (
		('drupal', 'Drupal'),
		('django', 'Django'),
		('other', 'Other'),
	)
	
	framework  = models.CharField(max_length=32,
	                             choices=frameworks, default='other')

	deployment_types = (
		('manual', 'Manual'),
		('docker', 'Docker'),
		('k8s', 'Kubernetes'),
		('other', 'Other'),
	)
	
	deployment_type  = models.CharField(max_length=32,
	                             choices=deployment_types, default='other')

	managers = models.ManyToManyField('Person')

	def __str__(self):
		return self.name

class Designation(models.Model):
	name = models.CharField(max_length=128)

	def __str__(self):
		return self.name

class Person(models.Model):
	user  = models.OneToOneField(settings.AUTH_USER_MODEL, 
	                             on_delete=models.CASCADE)
	
	# Keep in sync with the same field from SelfRegisterRequest
	epsid = models.CharField(max_length=30, unique=True)

	# TODO rem since the User model has first and last names?
	# TODO update __str__() then.
	# Keep in sync with the same field from SelfRegisterRequest
	name  = models.CharField(max_length=256)

	# Keep in sync with the same field from SelfRegisterRequest
	designation = models.ForeignKey(Designation, on_delete=models.PROTECT,
	              blank=True, null=True)

	# Keep in sync with the same field from SelfRegisterRequest
	managers = models.ManyToManyField('self', blank=True)
	
	has_vpn_access = models.BooleanField(default=False)
	
	iam_user = models.CharField(max_length=64, null=True, blank=True)
	
	# Keep in sync with the same field from SelfRegisterRequest
	projects = models.ManyToManyField(Project, blank=True)

	projects_with_live_server_access = models.ManyToManyField(
		Project, related_name='live_server_accessor', blank=True)

	projects_with_db_access = models.ManyToManyField(
		Project, related_name='db_accessor', blank=True)

	repos_with_read_access  = models.ManyToManyField(
		Repository, related_name='repo_reader', blank=True)

	repos_with_write_access = models.ManyToManyField(
		Repository, related_name='repo_writer', blank=True)

	jenkins_urls = ArrayField(models.CharField(max_length=4096), default=list)

	notes = models.TextField(blank=True)

	def __str__(self):
		return self.epsid + '(' + self.name + ')'

class Host(models.Model):
	owner  = models.ForeignKey(Person, on_delete=models.PROTECT,
	              blank=False, null=False)

	name = models.CharField(max_length=128, null=True, blank=True)
	ip   = models.CharField(max_length=128, null=True, blank=True)
	
	host_types = (
		('desktop', 'Desktop'),
		('laptop', 'Laptop'),
		('other', 'Other'),
	)
	
	type = models.CharField(max_length=32,
	                             choices=host_types, default='other')

	os_types = (
		('mswin', 'Windows'),
		('mac', 'Mac OS'),
		('linux', 'Linux-based'),
		('other', 'Other'),
	)

	os = models.CharField(max_length=32,
	                             choices=os_types, default='other')

class SSHKey(models.Model):
	pubkey = models.CharField(max_length=4096)
	owner  = models.ForeignKey(Person, on_delete=models.PROTECT,
	              blank=False, null=False)

	def __str__(self):
		return self.pubkey

class SelfRegisterRequest(models.Model):
	# Keep in sync with the same field from Person
	epsid = models.CharField(max_length=30, unique=True)
	
	email = models.EmailField(blank=False, null=False)
	
	# Keep in sync with the same field from Person
	name  = models.CharField(max_length=256)
	
	# Keep in sync with the same field from Person
	designation = models.ForeignKey(Designation, on_delete=models.PROTECT,
	              blank=True, null=True)

	# Keep in sync with the same field from Person
	managers = models.ManyToManyField(Person, blank=True)

	# Keep in sync with the same field from Person
	projects = models.ManyToManyField(Project, blank=True)
