from django.core.exceptions import PermissionDenied

class AdminOnlyMixin:
	def dispatch(self, request, *args, **kwargs):
		if not request.user.is_staff:
			raise PermissionDenied('Only admins can access this page.')
	
		return super().dispatch(request, *args, **kwargs)
