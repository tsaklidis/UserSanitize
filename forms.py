#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
from django import forms
from django.forms.widgets import PasswordInput, TextInput

from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth.models import User

from ..utilities.unique.functions import get_random_string


class Allow():

    def alphanumeric(self, data):
        # Allow letters, numbers and underspace
        if not re.match(r'(^[\w._]+$)', data, re.UNICODE):
            raise forms.ValidationError(
                u'Only letters and numbers are allowed.')
        return data

    def letters(self, data):
        # Allow only letters
        if not re.match(r'(^[\D.]+$)', data, re.UNICODE):
            raise forms.ValidationError(
                u'Only letters, no spaces allowed.')
        return data

    def numbers(self, data):
        pass

    def password_check(self, data):
        # Verify the strength of 'password'
        # Returns a dict indicating the wrong criteria
        # A password is considered strong if:
        #     8 characters length or more
        #     1 digit or more
        #     1 symbol or more
        #     1 uppercase letter or more
        #     1 lowercase letter or more

        # check the length
        length_error = len(data) < 8

        # check digits
        digit_error = re.search(r"\d", data) is None

        # check uppercase
        uppercase_error = re.search(r"[A-Z]", data) is None

        # check lowercase
        lowercase_error = re.search(r"[a-z]", data) is None

        # check symbols
        symbol_error = re.search(
            r"[ !#$%&'()*+,-./[\\\]^_`{|}~" + r'"]', data) is None

        # result
        password_ok = not (
            length_error or digit_error or uppercase_error or
            lowercase_error or symbol_error
        )

        return {
            'ok': password_ok,
            'Length': length_error,
            'Digit': digit_error,
            'Uppercase': uppercase_error,
            'Lowercase': lowercase_error,
            'Symbol': symbol_error,
        }


class LoginAuthenticationForm(AuthenticationForm):
    # Form for authenticating a requested user.
    # Authenticates a user against the provided username
    # and password.
    # User can use as username his email or his actual username.

    username = forms.CharField(required=True, max_length=50,
                               widget=TextInput(attrs={
                                   'placeholder': 'Username',
                                   'class': 'form-control',
                                   'required': 'true'}))

    password = forms.CharField(required=True,
                               widget=PasswordInput(attrs={
                                   'placeholder': 'Passord',
                                   'class': 'form-control',
                                   'required': 'true'}))

    remember_me = forms.BooleanField(required=False,
                                     widget=forms.CheckboxInput())

    def clean_remember_me(self):
        # checked or not keep loged in
        if not self.cleaned_data.get('remember_me'):
            self.request.session.set_expiry(0)


class ManagerPasswordChangeForm(PasswordChangeForm):
    # Form for changing password.

    new_password1 = forms.CharField(required=True,
                                    widget=PasswordInput(attrs={
                                        'placeholder': 'New password',
                                        'class': 'form-control',
                                        'required': 'true'}))

    new_password2 = forms.CharField(required=True,
                                    widget=PasswordInput(attrs={
                                        'placeholder': 'Repeat new password',
                                        'class': 'form-control',
                                        'required': 'true'}))

    old_password = forms.CharField(required=True,
                                   widget=PasswordInput(attrs={
                                       'placeholder': 'Old password',
                                       'class': 'form-control',
                                       'required': 'true'}))


class UserForm(forms.ModelForm):

    username = forms.CharField(required=True,
                               max_length=100,
                               error_messages={
                                   'unique': 'Username is in use'},
                               widget=TextInput(
                                   attrs={
                                       'class': 'form-control input-sm',
                                       'placeholder': "username",
                                       'required': 'True',
                                       'data-trigger': 'focus',
                                       'title': 'Field: Username',
                                       'data-content': 'Enter your username'})
                               )

    password = forms.CharField(required=True,
                               widget=PasswordInput(
                                   attrs={
                                       'placeholder': 'Passord',
                                       'required': 'true',
                                       'class': 'form-control input-sm',
                                       'data-trigger': 'focus',
                                       'title': 'Field: Passord',
                                       'data-content': 'Enter a secret password'})  # noqa
                               )

    password2 = forms.CharField(required=True,
                                widget=PasswordInput(
                                    attrs={
                                        'placeholder': 'Repeat password',
                                        'required': 'true',
                                        'class': 'form-control input-sm',
                                        'data-trigger': 'focus',
                                        'title': 'Field: Repeat password',
                                        'data-content': 'Repeat password.'})
                                )

    first_name = forms.CharField(required=True,
                                 max_length=100,
                                 widget=TextInput(
                                     attrs={
                                         'class': 'form-control input-sm',
                                         'placeholder': "First Name",
                                         'required': 'True',
                                         'data-trigger': 'focus',
                                         'title': 'Field: First Name',
                                         'data-content': 'Enter your\
                                         first name'

                                     }))

    last_name = forms.CharField(required=True,
                                max_length=100,
                                widget=TextInput(
                                    attrs={
                                        'class': 'form-control input-sm',
                                        'placeholder': "Last Name",
                                        'required': 'True',
                                        'data-trigger': 'focus',
                                        'title': 'Field: Last Name',
                                        'data-content': 'Enter your last name.'

                                    }))

    email = forms.EmailField(required=True,
                             widget=TextInput(
                                 attrs={
                                     'class': 'form-control input-sm',
                                     'placeholder': "Email",
                                     'required': 'True',
                                     'data-trigger': 'focus',
                                     'title': 'Field: Email',
                                     'data-content': 'enter a valid email.'
                                 }),
                             error_messages={
                                 'invalid': 'Use a valid email.'},
                             )

    def clean_username(self):
        # Check for valid username
        username = self.cleaned_data['username']
        sanizite = Allow()
        return sanizite.alphanumeric(username)

    def clean_first_name(self):
        first_name = self.cleaned_data['first_name']
        sanizite = Allow()
        return sanizite.letters(first_name)

    def clean_last_name(self):
        last_name = self.cleaned_data['last_name']
        sanizite = Allow()
        return sanizite.letters(last_name)

    def clean_email(self):
        # To avoid hardcoding domains, create a model eg: BanedEmails
        # This way you can add domains from Django panel
        baned = ['something.com', 'domain.com']
        email = self.cleaned_data.get('email')
        domain = email.split('@')[1]

        if domain in baned:
            # A good technique is not informing why a baned mail is not allowd
            raise forms.ValidationError(u'Not Allowed Domain')

        if User.objects.filter(email=email)\
                .exclude(email=self.instance.email).exists():
            raise forms.ValidationError(u'Email in use!')
        return email

    def clean_password2(self):
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')
        if password2 != password:
            raise forms.ValidationError(u"Passwords don't match")
        return password

    def clean_password(self):
        password = self.cleaned_data.get('password')
        sanizite = Allow()
        results = sanizite.password_check(password)

        if results['ok']:
            return password
        else:
            msg_str = ''
            for msg in results:
                if results[msg]:
                    msg_str += msg + ', '
            raise forms.ValidationError(
                u"Password must include: {0}".format(msg_str))

    class Meta:
        model = User
        fields = ('username', 'password', 'first_name',
                  'last_name', 'email', 'password2')
