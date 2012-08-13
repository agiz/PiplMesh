from django import http, template
from django.conf import settings
from django.contrib import messages
from django.core import mail
from django.core import urlresolvers
from django.core.files import storage
from django.utils.translation import ugettext_lazy as _
from django.views import generic as generic_views

from tastypie import http as tastypie_http

from mongogeneric import detail

from piplmesh.account import models as account_models
from piplmesh.api import models as api_models, resources
from piplmesh.frontend import forms

import smtplib

HOME_CHANNEL_ID = 'home'

class HomeView(generic_views.TemplateView):
    template_name = 'home.html'

# TODO: Get HTML5 geolocation data and store it into request session
class OutsideView(generic_views.TemplateView):
    template_name = 'outside.html'

class SearchView(generic_views.TemplateView):
    template_name = 'search.html'

class AboutView(generic_views.TemplateView):
    template_name = 'about.html'
      
class ContactView(generic_views.FormView):
    """
    This view checks if all contact data are valid and then send mail.
    
    User is redirected back to contact page.
    """
    
    template_name = 'contact.html'
    success_url = urlresolvers.reverse_lazy('contact')
    form_class = forms.ContactForm

    def form_valid(self, form):
        subject = form.cleaned_data['subject'],
        email = form.cleaned_data['email'],
        message = form.cleaned_data['message'],
        try:
            mail.mail_managers(subject, message, email, (settings.DEFAULT_FROM_EMAIL,))
            messages.success(self.request, _("Thank you. Your message has been successfuly sent."))
        except smtplib.SMTPException, e:
            messages.error(self.request, _("Sorry, something went wrong here.")) 
        return super(ContactView, self).form_valid(form)

class UserView(detail.DetailView):
    """
    This view checks if user exist in database and returns his user page (profile).
    """

    template_name = 'user/user.html'
    document = account_models.User
    slug_field = 'username'
    slug_url_kwarg = 'username'

def upload_view(request):
    if request.method != 'POST':
        return http.HttpResponseBadRequest()

    resource = resources.UploadedFileResource()

    # TODO: Provide some user feedback while uploading

    uploaded_files = []
    for field, files in request.FILES.iterlists():
        for file in files:
            # We let storage decide a name
            filename = storage.default_storage.save('', file)

            uploaded_file = api_models.UploadedFile()
            uploaded_file.author = request.user
            uploaded_file.filename = filename
            uploaded_file.content_type = file.content_type
            uploaded_file.save()

            uploaded_files.append({
                'filename': filename,
                'resource_uri': resource.get_resource_uri(uploaded_file)
            })

    # TODO: Create background task to process uploaded file (check content type (both in GridFS file and UploadedFile document), resize images)

    return resource.create_response(request, uploaded_files, response_class=tastypie_http.HttpAccepted)

def forbidden_view(request, reason=''):
    """
    Displays 403 fobidden page. For example, when request fails CSRF protection.
    """

    from django.middleware import csrf
    t = template.loader.get_template('403.html')
    return http.HttpResponseForbidden(t.render(template.RequestContext(request, {
        'DEBUG': settings.DEBUG,
        'reason': reason,
        'no_referer': reason == csrf.REASON_NO_REFERER,
    })))
