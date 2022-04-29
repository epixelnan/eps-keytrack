from django.core.exceptions import PermissionDenied

MSG_ADMIN_ONLY = 'Only admins can access this page.'

class AdminOnlyMixin:
	def dispatch(self, request, *args, **kwargs):
		if not request.user.is_staff:
			raise PermissionDenied(MSG_ADMIN_ONLY)
	
		return super().dispatch(request, *args, **kwargs)
