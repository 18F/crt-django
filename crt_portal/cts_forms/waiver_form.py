from django.forms import (BooleanField, CharField, CheckboxInput, ChoiceField, DateField,
                          EmailInput, HiddenInput, IntegerField,
                          ModelChoiceField, ModelForm, Form,
                          ModelMultipleChoiceField, MultipleChoiceField,
                          Select, SelectMultiple, Textarea, TextInput,
                          TypedChoiceField)
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from .models import AmericaReport
from .model_variables import STATES_AND_TERRITORIES
from .phone_regex import phone_validation_regex
from .model_variables import CONTACT_PHONE_INVALID_MESSAGE
from .widgets import UsaCheckboxSelectMultiple, CrtDateInput

User = get_user_model()


class WaiverForm(ModelForm):
    """This form is for CRT only for complaints that come from other sources than the public web form"""
    class Meta:
        model = AmericaReport
        fields = [
            'contact_first_name',
            'contact_last_name',
            'contact_email',
            'contact_phone',
            'contact_address_line_1',
            'contact_address_line_2',
            'contact_city',
            'contact_state',
            'contact_zip',
            'agency',
            'product_name',
            'product_company',
            'parent_company',
            'unique_entity_identifer',
            'duns_number',
            'country_of_origin',
            'purpose_of_product',
            'market_justification',
        ]

        widgets = {
            'contact_first_name': TextInput(attrs={
                'class': 'usa-input',
            }),
            'cotact_last_name': TextInput(attrs={
                'class': 'usa-input',
            }),
            'contact_email': EmailInput(attrs={
                'class': 'usa-input',
            }),
            'contact_phone': TextInput(attrs={
                'class': 'usa-input',
                'pattern': phone_validation_regex,
                'title': CONTACT_PHONE_INVALID_MESSAGE
            }),
            'contact_address_line_1': TextInput(attrs={
                'class': 'usa-input',
            }),
            'contact_address_line_2': TextInput(attrs={
                'class': 'usa-input',
            }),
            'contact_city': TextInput(attrs={
                'class': 'usa-input',
            }),
            'contact_zip': TextInput(attrs={
                'class': 'usa-input',
            }),
            'agency': TextInput(attrs={
                'class': 'usa-input',
            }),
            # product
            'product_name': TextInput(attrs={
                'class': 'usa-input',
            }),
            'product_company': TextInput(attrs={
                'class': 'usa-input',
            }),
            'parent_company': TextInput(attrs={
                'class': 'usa-input',
            }),
            'unique_entity_identifer': TextInput(attrs={
                'class': 'usa-input',
            }),
            'duns_number': TextInput(attrs={
                'class': 'usa-input',
            }),
            'country_of_origin': TextInput(attrs={
                'class': 'usa-input',
            }),
            'purpose_of_product': TextInput(attrs={
                'class': 'usa-textarea',
            }),
        }


    def __init__(self, *args, **kwargs):
        ModelForm.__init__(self, *args, **kwargs)
        self.fields['market_justification'].widget.attrs['class'] = 'usa-textarea word-count-500'
        self.fields['market_justification'].help_text =  'Detailed justification for the use of goods, products, or materials that have not been mined, produced, or manufactured in the United States.'


class Filters(ModelForm):
    status = MultipleChoiceField(
        initial=(('new', 'New'), ('open', 'Open')),
        required=False,
        label='status',
        choices=(
            ('new', 'New'),
            ('open', 'Open'),
            ('denied', 'Denied'),
            ('approved', 'Approved')
        ),
        widget=UsaCheckboxSelectMultiple(),
    )
    contact_state = MultipleChoiceField(
        required=False,
        choices=STATES_AND_TERRITORIES,
        widget=UsaCheckboxSelectMultiple(attrs={
            'name': 'contact_state',
        }),
    )
    market_justification = CharField(
        required=False,
        widget=TextInput(
            attrs={
                'class': 'usa-input',
                'name': 'justification',
                'placeholder': 'justification',
                'aria-label': 'justification'
            },
        ),
    )
    assigned_to = ModelChoiceField(
        required=False,
        queryset=User.objects.filter(is_active=True).order_by('username'),
        label=_("Assigned to"),
        to_field_name='username',
        widget=Select(attrs={
            'name': 'assigned_to',
            'class': 'usa-input'
        })
    )
    create_date_start = DateField(
        required=False,
        label="From:",
        input_formats=('%Y-%m-%d'),
        widget=CrtDateInput(attrs={
            'class': 'usa-input',
            'name': 'create_date_start',
            'min': '2019-01-01',
            'placeholder': 'yyyy-mm-dd',
        }),
    )
    create_date_end = DateField(
        required=False,
        label="To:",
        input_formats=('%Y-%m-%d'),
        widget=CrtDateInput(attrs={
            'class': 'usa-input',
            'name': 'create_date_end',
            'min': '2019-01-01',
            'placeholder': 'yyyy-mm-dd',
        }),
    )


    class Meta:
        model = AmericaReport
        fields = [
            'contact_first_name',
            'contact_last_name',
            'contact_city',
            'contact_state',
            'status',
            'assigned_to',
            'id',
            'market_justification',
            'contact_email',
        ]

        labels = {
            # These are CRT view only
            'contact_first_name': 'Contact first name',
            'contact_last_name': 'Contact last name',
            'contact_city': 'Contact city',
            'contact_state': 'Incident location state',
            'contact_email': 'Contact email',
            'assigned_to': 'Assignee',
            'id': 'Wavier application ID',
            'market_justification': 'Justification',
            'create_date_start': 'Created Date Start',
            'create_date_end': 'Created Date End',
        }

        widgets = {
            'contact_first_name': TextInput(attrs={
                'class': 'usa-input',
                'name': 'contact_first_name',
                'placeholder': 'Contact First Name',
                'id': 'id_contact_first_name',
                'aria-label': 'Contact First Name'
            }),
            'contact_last_name': TextInput(attrs={
                'class': 'usa-input',
                'name': 'contact_last_name',
                'placeholder': 'Contact Last Name',
                'aria-label': 'Contact Last Name'
            }),
            'contact_city': TextInput(attrs={
                'class': 'usa-input',
                'name': 'location_city'
            }),
            'id': TextInput(attrs={
                'class': 'usa-input',
                'name': 'public_id',
                'placeholder': 'ID',
                'aria-label': 'CRT Public ID'
            }),
            'market_justification': TextInput(attrs={
                'class': 'usa-input',
                'name': 'violation_summary',
                'placeholder': 'Personal Description',
                'aria-label': 'Personal Description'
            }),
            'contact_email': EmailInput(attrs={
                'class': 'usa-input',
                'name': 'contact_email',
                'placeholder': 'Contact Email',
                'aria-label': 'Email',
            }),
        }
        error_messages = {
            'create_date': {
                'in_future': _("Create date cannot be in the future."),
            },
        }
