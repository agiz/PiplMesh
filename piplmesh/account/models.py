from mongoengine import *

from django.utils.encoding import smart_str
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth.hashers import check_password, make_password
from django.utils.translation import ugettext_lazy as _

import datetime

REDIRECT_FIELD_NAME = 'next'

class CustomUser(Document):
    """A User document that aims to mirror most of the API specified by Django
    at http://docs.djangoproject.com/en/dev/topics/auth/#users
    Ripped from mongoengine auth.py
    """
    username = StringField(max_length=30, required=True,
                           verbose_name=_('username'),
                           help_text=_("Required. 30 characters or fewer. Letters, numbers and @/./+/-/_ characters"))

    first_name = StringField(max_length=30,
                             verbose_name=_('first name'))

    last_name = StringField(max_length=30,
                            verbose_name=_('last name'))
    email = EmailField(verbose_name=_('e-mail address'))
    password = StringField(max_length=128,
                           verbose_name=_('password'),
                           help_text=_("Use '[algo]$[iterations]$[salt]$[hexdigest]' or use the <a href=\"password/\">change password form</a>."))
    is_staff = BooleanField(default=False,
                            verbose_name=_('staff status'),
                            help_text=_("Designates whether the user can log into this admin site."))
    is_active = BooleanField(default=True,
                             verbose_name=_('active'),
                             help_text=_("Designates whether this user should be treated as active. Unselect this instead of deleting accounts."))
    is_superuser = BooleanField(default=False,
                                verbose_name=_('superuser status'),
                                help_text=_("Designates that this user has all permissions without explicitly assigning them."))
    last_login = DateTimeField(default=datetime.datetime.now,
                               verbose_name=_('last login'))
    date_joined = DateTimeField(default=datetime.datetime.now,
                                verbose_name=_('date joined'))
    # Custom fields
    birthdate = DateTimeField()
    gender = StringField(max_length=6)
    facebook_id = IntField()
    token = StringField(max_length=150)


    meta = {
        'indexes': [
            {'fields': ['username'], 'unique': True}
        ]
    }

    def __unicode__(self):
        return self.username

    def get_full_name(self):
        """Returns the users first and last names, separated by a space.
        """
        full_name = u'%s %s' % (self.first_name or '', self.last_name or '')
        return full_name.strip()

    def is_anonymous(self):
        return False

    def is_authenticated(self):
        return True

    def set_password(self, raw_password):
        """Sets the user's password - always use this rather than directly
        assigning to :attr:`~mongoengine.django.auth.User.password` as the
        password is hashed before storage.
        """
        self.password = make_password(raw_password)
        self.save()
        return self

    def check_password(self, raw_password):
        """Checks the user's password against a provided password - always use
        this rather than directly comparing to
        :attr:`~mongoengine.django.auth.User.password` as the password is
        hashed before storage.
        """
        return check_password(raw_password, self.password)

    @classmethod
    def create_user(cls, username, password, email=None):
        """Create (and save) a new user with the given username, password and
        email address.
        """
        now = datetime.datetime.now()

        # Normalize the address by lowercasing the domain part of the email
        # address.
        if email is not None:
            try:
                email_name, domain_part = email.strip().split('@', 1)
            except ValueError:
                pass
            else:
                email = '@'.join([email_name, domain_part.lower()])

        user = cls(username=username, email=email, date_joined=now)
        user.set_password(password)
        user.save()
        return user

    def get_and_delete_messages(self):
        return []
