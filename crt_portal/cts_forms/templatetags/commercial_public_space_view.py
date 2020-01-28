from django import template
from ..model_variables import COMMERCIAL_PUBLIC_FRIENDLY_TEXT


register = template.Library()


@register.inclusion_tag('forms/snippets/commercial_public_space_view.html')
def render_commercial_public_space_view(location, type):
    other_text = None

    if location != 'other':
        location_type = COMMERCIAL_PUBLIC_FRIENDLY_TEXT.get(location, '—')
    else:
        location_type = type
        other_text = 'Other'

    return {
        'location_type': location_type,
        'other_text': other_text
    }
