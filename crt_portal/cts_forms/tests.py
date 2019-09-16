import random
import string

from django.test import TestCase
from django.test.client import Client
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.urls import reverse

from .models import ProtectedClass, Report
from .forms import WhatHappened, Where, Who, Details, Contact


class Valid_Form_Tests(TestCase):
    """Confirms each form is valid when given valid test data."""
    def test_WhatHappened_valid(self):
        form = WhatHappened(data={
            'primary_complaint': 'vote',
            'protected_class_set': ProtectedClass.objects.all(),
        })
        self.assertTrue(form.is_valid())

    def test_Where_valid(self):
        form = Where(data={
            'place': 'place_of_worship',
            'public_or_private_employer': 'public_employer',
            'employer_size': '14_or_less',
            'public_or_private_school': 'public',
            'public_or_private_facility': 'state_local_facility',
            'public_or_private_healthcare': 'state_local_facility',
        })
        self.assertTrue(form.is_valid())

    def test_Who_valid(self):
        form = Who(data={
            'respondent_contact_ask': False,
            'respondent_type': 'employer',
            'respondent_name': 'Max',
            'respondent_city': 'Hometown',
            'respondent_state': 'AK',
        })
        self.assertTrue(form.is_valid())

    def test_Details_valid(self):
        form = Details(data={
            'violation_summary': 'Hello! I have a problem.',
            'when': 'last_6_months',
            'how_many': 'no',
        })
        self.assertTrue(form.is_valid())

    def test_Contact_valid(self):
        form = Contact(data={
            'contact_first_name': 'first_name',
            'contact_last_name': 'last_name',
        })
        self.assertTrue(form.is_valid())


class Validation_Form_Tests(TestCase):
    """Confirming validation on the server level"""
    def test_required_primary_complaint(self):
        form = WhatHappened(data={
            'primary_complaint': '',
            'protected_class_set': ProtectedClass.objects.all(),
        })

        self.assertTrue('primary_complaint<ul class="errorlist"><li>This field is required.' in str(form.errors))

    def test_required_when(self):
        form = Details(data={
            'violation_summary': 'Hello! I have a problem.',
            'when': '',
            'how_many': 'no',
        })
        self.assertTrue('when<ul class="errorlist"><li>This field is required.' in str(form.errors))

    def test_required_violation_summary(self):
        form = Details(data={
            'violation_summary': '',
            'when': 'last_6_months',
            'how_many': 'no',
        })
        self.assertTrue('violation_summary<ul class="errorlist"><li>This field is required.' in str(form.errors))

    def test_required_where(self):
        form = Where(data={
            'place': '',
            'public_or_private_employer': 'public_employer',
            'employer_size': '14_or_less',
            'public_or_private_school': 'public',
            'public_or_private_facility': 'state_local_facility',
            'public_or_private_healthcare': 'state_local_facility',
        })
        self.assertTrue('place<ul class="errorlist"><li>This field is required.' in str(form.errors))


class ContactValidationTests(TestCase):
    def test_non_ascii_name(self):
        form = Contact(data={
            'contact_first_name': '李王',
            'contact_last_name': '王-Núñez',
            'contact_email': '',
            'contact_phone': ''
        })
        self.assertTrue(form.is_valid())

    def test_non_ascii_email(self):
        form = Contact(data={
            'contact_first_name': '',
            'contact_last_name': '',
            'contact_email': 'foo@bär.com',
            'contact_phone': ''
        })
        self.assertTrue(form.is_valid())

    def test_phone_too_short(self):
        """Model validation tests need to be structured differently"""
        phone = Report(
            contact_phone='202',
        )

        try:
            phone.full_clean()
        except ValidationError as err:
            self.assertTrue(err.message_dict['contact_phone'] == ['"202" doesn\'t have enough numbers to be a phone number. Please double check your phone number and make sure you have an area code.'])

    def test_international_phone(self):
        phone = Report(
            contact_phone='+02071838750',
        )
        try:
            phone.full_clean()
        except ValidationError as err:
            self.assertTrue('contact_phone' not in err.message_dict)

    def test_international_phone_longer(self):
        phone = Report(
            contact_phone='+442071838750',
        )
        try:
            phone.full_clean()
        except ValidationError as err:
            self.assertTrue('contact_phone' not in err.message_dict)


class LoginRequiredTests(TestCase):
    """Please add a test for each url that is tied to a view that requires login."""
    def setUp(self):
        self.client = Client()
        self.test_pass = ''.join(random.choice(string.ascii_lowercase) for i in range(32))
        self.user = User.objects.create_user('john', 'lennon@thebeatles.com', self.test_pass)

    def test_view_all_login_success(self):
        """ We probably only need one successful login test"""
        self.client.login(username='john', password=self.test_pass)
        response = self.client.get(reverse('crt_forms:crt-forms-index'))
        self.assertEqual(response.status_code, 200)

    def test_view_all_login(self):
        response = self.client.get(reverse('crt_forms:crt-forms-index'))
        self.assertRedirects(response, '/accounts/login/?next=/form/view')
