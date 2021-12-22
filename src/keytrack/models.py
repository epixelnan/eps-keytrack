from django.db import models
from django.conf import settings

class Project(models.Model):
	name  = models.CharField(max_length=256)

	def __str__(self):
		return self.name

class Designation(models.Model):
	name = models.CharField(max_length=128)

	def __str__(self):
		return self.name

class Person(models.Model):
	user  = models.OneToOneField(settings.AUTH_USER_MODEL, 
	                             on_delete=models.CASCADE)
	epsid = models.CharField(max_length=30,unique=True)
	name  = models.CharField(max_length=256)
	designation = models.ForeignKey(Designation, on_delete=models.PROTECT,
	              blank=True,null=True)
	
	host_ip   = models.CharField(max_length=128, null=True)
	host_name = models.CharField(max_length=128, null=True)
	
	host_types = (
		('desktop', 'Desktop'),
		('laptop', 'Laptop'),
		('other', 'Other'),
	)
	
	host_type = models.CharField(max_length=32,
	                             choices=host_types, default='other')

	os_types = (
		('mswin', 'Windows'),
		('mac', 'Mac OS'),
		('linux', 'Linux-based'),
		('other', 'Other'),
	)

	host_os = models.CharField(max_length=32,
	                             choices=os_types, default='other')
	
	has_vpn_access = models.BooleanField(default=False)
	
	projects = models.ManyToManyField(Project)
	
	def __str__(self):
		return self.epsid + '(' + self.name + ')'
