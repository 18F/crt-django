import urllib.parse

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.utils.translation import gettext_lazy as _
from django.shortcuts import redirect, reverse, render
from django.db.models import F
from django.core.paginator import Paginator

from formtools.wizard.views import SessionWizardView

from .models import AmericaReport
from .waiver_filters import report_filter
from .waiver_sorts import report_sort
from .page_through import pagination
from .waiver_form import Filters



class WaiverFormView(LoginRequiredMixin, SessionWizardView):
    def get_template_names(self):
        return 'forms/waiver_template.html'

    def get_context_data(self, form, **kwargs):
        context = super().get_context_data(form=form, **kwargs)

        field_errors = list(map(lambda field: field.errors, context['form']))
        page_errors = [error for field in field_errors for error in field]

        ordered_step_names = [
            'Agency',
            'Contact',
            'Product Information',
            'Justification',
        ]

        context.update({
            'field_errors': field_errors,
            'page_errors': page_errors,
            'num_page_errors': len(list(page_errors)),
            'word_count_text': {
                'wordRemainingText': _('word remaining'),
                'wordsRemainingText': _(' words remaining'),
                'wordLimitReachedText': _(' word limit reached'),
            },
            'ordered_step_names': ordered_step_names,
            'stage_link': True,
            'submit_button': True,
        })

        return context

    def done(self, form_list, form_dict, **kwargs):
        # data, report = save_form(self.get_all_cleaned_data())
        report = self.get_all_cleaned_data()
        americareport = AmericaReport.objects.create(**report)

        return redirect(reverse('crt_forms:crt-forms-show', kwargs={'id': americareport.pk}))

@login_required
def waiver_index_view(request):
    # profile_form = ProfileForm()
    # # Check for Profile object, then add filter to request
    # if hasattr(request.user, 'profile') and request.user.profile.intake_filters:
    #     request.GET = request.GET.copy()
    #     global_section_filter = request.user.profile.intake_filters.split(',')

    #     # If assigned_section is NOT specificied in request, use filter from profile
    #     if 'assigned_section' not in request.GET:
    #         request.GET.setlist('assigned_section', global_section_filter)

    #     data = {'intake_filters': request.GET.getlist('assigned_section')}
    #     profile_form = ProfileForm(data)

    report_query, query_filters = report_filter(request.GET)

    # Sort data based on request from params, default to `created_date` of complaint
    per_page = request.GET.get('per_page', 15)
    page = request.GET.get('page', 1)

    # requested_reports = report_query.annotate(email_count=F('waiver_email_report_count__email_count'))

    sort_expr, sorts = report_sort(request.GET)
    # requested_reports = requested_reports.order_by(*sort_expr)
    requested_reports = report_query.order_by(*sort_expr)

    paginator = Paginator(requested_reports, per_page)
    requested_reports, page_format = pagination(paginator, page, per_page)

    sort_state = {}
    # make sure the links for this page have the same paging, sorting, filtering etc.
    page_args = f'?per_page={per_page}'

    # process filter query params
    filter_args = ''
    for query_item in query_filters.keys():
        arg = query_item
        for item in query_filters[query_item]:
            filter_args = filter_args + f'&{arg}={item}'
    page_args += filter_args

    # process sort query params
    sort_args = ''
    for sort_item in sorts:
        if sort_item[0] == SORT_DESC_CHAR:
            sort_state.update({sort_item[1::]: True})
        else:
            sort_state.update({sort_item: False})

        sort_args += f'&sort={sort_item}'
    page_args += sort_args

    all_args_encoded = urllib.parse.quote(f'{page_args}&page={page}')

    data = []

    paginated_offset = page_format['page_range_start'] - 1

    for index, report in enumerate(requested_reports):
        data.append({
            "report": report,
            "url": f'{report.id}?next={all_args_encoded}&index={paginated_offset + index}',
        })

    final_data = {
        'form': Filters(request.GET),
        'profile_form': {},
        'data_dict': data,
        'page_format': page_format,
        'page_args': page_args,
        'sort_state': sort_state,
        'filter_state': filter_args,
        'filters': query_filters,
        'return_url_args': all_args_encoded,
    }

    return render(request, 'forms/complaint_view/index/index.html', final_data)
