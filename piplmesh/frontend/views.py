from django.views import generic as generic_views
from django.utils import decorators as utils_decorators
from lazysignup import decorators as lazysignup_decorators

class LazyUserMixin(object):
    @utils_decorators.method_decorator(lazysignup_decorators.allow_lazy_user)
    def dispatch(self, *args, **kwargs):
        return super(LazyUserMixin, self).dispatch(*args, **kwargs)

class HomeView(LazyUserMixin, generic_views.TemplateView):
    template_name = 'home.html'