from django.contrib.auth.mixins import UserPassesTestMixin, PermissionRequiredMixin, LoginRequiredMixin
from projects.models import Project
from django.urls import reverse_lazy


class AccessMixin(UserPassesTestMixin):

    login_required = True
    conditions = []

    login_url = reverse_lazy('users:login')

    def test_func(self):
        if self.conditions:
            return all(self.conditions)
        return True

    def dispatch(self, request, *args, **kwargs):
        if self.login_required and not request.user.is_authenticated:
            return self.handle_no_permission()
        user_test_result = self.get_test_func()()
        if not user_test_result:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)
