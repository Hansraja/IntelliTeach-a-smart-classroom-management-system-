from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core.mail import send_mail
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.db import models

from IgCMS import settings
from .backends import UserManager

class AuthUser(AbstractBaseUser, PermissionsMixin):
    username = None
    email = models.EmailField(
        _('email address'),
        unique=True,
        max_length=254,
        help_text=_('Required. a valid email address.'),
        error_messages={
            'unique': _("A user with that email already exists."),
        },)
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=150, blank=True)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_hod = models.BooleanField(default=False)
    is_faculty = models.BooleanField(default=False)
    is_student = models.BooleanField(default=False)
    picture = models.ImageField(upload_to='images/profile_pictures', null=True, blank=True)
    
    objects = UserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name']
    
    class Meta:
        db_table = 'auth_user'
        verbose_name = _('user')
        verbose_name_plural = _('users')
        
    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email) # type: ignore
        
    def get_full_name(self):
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()
    
    def get_short_name(self):
        return self.first_name
    
    def email_user(self, subject, message, from_email=None, **kwargs):
        send_mail(subject, message, from_email, [self.email], **kwargs)

    def update_password_email(self, password: str):
        subject = f'Password Reset from {settings.APP_NAME}'
        message = f'Hello {self.get_full_name()},\n\nYour password has been reset successfully.\n\nHere are your new login details:\n\nEmail: {self.email}\nPassword: {password}\n\nPlease note that your password should not be shared with anyone.\n\n\n\nThis is an auto-generated email by the system and does not support incoming mails. If you have any queries, please reach out to us through your dashboard.'
        from_email = 'igcms@igcms.com'
        send_mail(subject=subject, from_email=from_email, recipient_list=[self.email], message=message)

    def delete_account_email(self):
        subject = f'Account Deletion from {settings.APP_NAME}'
        message = f'Hello {self.get_full_name()},\n\nYour account has been deleted successfully.\n\nIf you have any queries, please reach out to us through your dashboard.'
        from_email = 'ig@igcms.com'
        send_mail(subject=subject, from_email=from_email, recipient_list=[self.email], message=message)


class HOD(models.Model):
    user = models.OneToOneField(AuthUser, on_delete=models.CASCADE)


class Faculty(models.Model):
    user = models.OneToOneField(AuthUser, on_delete=models.CASCADE)
    subject = models.CharField(max_length=100, null=True, blank=True)
    mobile = models.CharField(max_length=15, null=True, blank=True)

    def send_welcome_email(self, password: str):
        subject = f'Faculty Details from {settings.APP_NAME} - {self.subject}'
        message = f'Hello {self.user.get_full_name()},\n\nYou have been successfully added to the {settings.COLLEGE_NAME}\'s class room management System.\n\nHere are your login details:\n\nEmail: {self.user.email}\nPassword: {password}\n\nPlease note that your password should not be shared with anyone.\n\n\n\nThis is an auto-generated email by the system and does not support incoming mails. If you have any queries, please reach out to us through your dashboard.'
        from_email = 'ik@igcms.com'
        send_mail(subject=subject, from_email=from_email, recipient_list=[self.user.email], message=message)

    def __str__(self):
        return self.user.get_full_name()

class Student(models.Model):
    user = models.OneToOneField(AuthUser, on_delete=models.CASCADE)
    roll_number = models.CharField(max_length=20, unique=True)
    father_name = models.CharField(max_length=100, null=True, blank=True)
    mother_name = models.CharField(max_length=100, null=True, blank=True)
    dob = models.DateField( null=True, blank=True)
    mobile = models.CharField(max_length=15, null=True, blank=True)

    def send_welcome_email(self, password: str):
        subject = f'Student Details from {settings.APP_NAME} - Roll No. {self.roll_number}'
        message = f'Hello {self.user.get_full_name()},\n\nYou have been successfully added to the {settings.COLLEGE_NAME}\'s class room management System.\n\nHere are your login details:\n\nRoll No.: {self.roll_number}\nPassword: {password}\n\nPlease note that your password should not be shared with anyone.\n\n\n\nThis is an auto-generated email by the system and does not support incoming mails. If you have any queries, please reach out to us through your dashboard.'
        from_email = 'ikgcms@igcms.com'
        send_mail(subject=subject, from_email=from_email, recipient_list=[self.user.email], message=message)

    def __str__(self):
        return self.user.get_full_name()
