from django.contrib.auth.models import AnonymousUser, User
from django.core.exceptions import PermissionDenied
from django.test import TestCase
from django.test import RequestFactory

from .views.admin_process_regreqs import RegisterRequestsView
from .views.admin_mixins import MSG_ADMIN_ONLY

class RegisterRequestsViewTestCase(TestCase):
	def setUp(self):
		self.factory = RequestFactory()
		
		User.objects.create(username='NormalUser1', is_staff=False)
		User.objects.create(username='StaffUser1',  is_staff=True)

	def test_admin_only_for_anonymous(self):
		req  = self.factory.get('/admin/regreqs/')
		req.user = AnonymousUser()
		with self.assertRaisesMessage(PermissionDenied, MSG_ADMIN_ONLY):
			RegisterRequestsView.as_view()(req)

	def test_admin_only_for_non_staff(self):
		req  = self.factory.get('/admin/regreqs/')
		req.user = User.objects.get(username='NormalUser1')
		with self.assertRaisesMessage(PermissionDenied, MSG_ADMIN_ONLY):
			RegisterRequestsView.as_view()(req)

	def test_admin_only_for_staff(self):
		req  = self.factory.get('/admin/regreqs/')
		req.user = User.objects.get(username='StaffUser1')
		resp = RegisterRequestsView.as_view()(req)
		self.assertEqual(resp.status_code, 200)
