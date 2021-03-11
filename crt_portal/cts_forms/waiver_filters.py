# Class to handle filtering Reports by supplied query params,
# provided they are valid filterable model properties.
import logging
import urllib.parse
from datetime import datetime

from django.contrib.postgres.search import SearchQuery, SearchVector

from .models import AmericaReport

logger = logging.getLogger(__name__)

# To add a new filter option for Reports, add the field name and expected filter behavior
filter_options = {
    'contact_first_name': '__icontains',
    'contact_last_name': '__icontains',
    'contact_email': '__icontains',
    'contact_address_line_1': '__icontains',
    'contact_address_line_2': '__icontains',
    'contact_city': '__icontains',
    'contact_state': '__in',
    'status': '__in',
    'contact_zip': '__in',
    'agency': '__search',
    'product_name': '__search',
    'product_company': '__search',
    'parent_company': '__search',
    'unique_entity_identifer':'__icontains',
    'duns_number': '__icontains',
    'country_of_origin': '__search',
    'purpose_of_product': '__search',
    'market_justification': 'serch_vecotr',
    'create_date_start': '__gte',
    'create_date_end': '__lte',
    'closed_date_start': '__gte',
    'closed_date_end': '__lte',
    'modified_date_start': '__gte',
    'modified_date_end': '__lte',
    'public_id': '__icontains',
    'assigned_to': 'foreign_key',
}


# Populate query with valid filterable fields

def _get_date_field_from_param(field):
    """
    Return model field by truncating the filter preposition
    which follows the last occurrence of `_`
    """
    return field[:field.rfind('_')]


def _change_datetime_to_end_of_day(dateObj, field):
    """
    Takes a datetime and field param to ensure an end_date
    field has time moved to end of day (23:59:59)
    """
    if 'end' in field:
        return dateObj.replace(hour=23, minute=59, second=59)
    else:
        return dateObj


def report_filter(querydict):
    kwargs = {}
    filters = {}
    qs = AmericaReport.objects.filter()
    for field in filter_options.keys():
        filter_list = querydict.getlist(field)

        if len(filter_list) > 0:
            filters[field] = querydict.getlist(field)
            if filter_options[field] == '__in':
                # works for one or more options with exact matches
                kwargs[f'{field}__in'] = querydict.getlist(field)
            elif filter_options[field] == '__search':
                # takes one phrase
                kwargs[f'{field}__search'] = querydict.getlist(field)[0]
            elif filter_options[field] == '__icontains':
                kwargs[f'{field}__icontains'] = querydict.getlist(field)[0]
            elif 'date' in field:
                # filters by a start date or an end date expects yyyy-mm-dd
                field_name = _get_date_field_from_param(field)
                encodedDate = querydict.getlist(field)[0]
                decodedDate = urllib.parse.unquote(encodedDate)
                try:
                    dateObj = datetime.strptime(decodedDate, "%Y-%m-%d")
                    dateObj = _change_datetime_to_end_of_day(dateObj, field)
                    kwargs[f'{field_name}{filter_options[field]}'] = dateObj
                except ValueError:
                    # if the date is invalid, we ignore it.
                    continue
            elif filter_options[field] == 'summary':
                # assumes summaries are edited so there is only one per report - that is current behavior
                kwargs['internal_comments__note__search'] = querydict.getlist(field)[0]
                kwargs['internal_comments__is_summary'] = True
            elif filter_options[field] == 'reported_reason':
                reasons = querydict.getlist(field)
                kwargs['protected_class__value__in'] = reasons
            elif filter_options[field] == 'foreign_key':
                # assumes assigned_to but could add logic for other foreign keys in the future
                kwargs['assigned_to__username__in'] = querydict.getlist(field)
            elif filter_options[field] == 'eq':
                kwargs[field] = querydict.getlist(field)[0]
            elif filter_options[field] == '__gte':
                kwargs[field] = querydict.getlist(field)
            elif filter_options[field] == 'serch_vecotr':
                combined_or_search = _combine_term_searches_with_or(filter_list)
                qs = qs.annotate(search=SearchVector(field)).filter(search=combined_or_search)
    qs = qs.filter(**kwargs)
    return qs, filters


def _combine_term_searches_with_or(terms):
    """Create a CombinedSearchQuery of all received search terms"""
    combined_search = SearchQuery(terms.pop())
    for term in terms:
        combined_search = combined_search | SearchQuery(term)
    return combined_search
