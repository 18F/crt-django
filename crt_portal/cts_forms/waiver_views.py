import urllib.parse

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.utils.translation import gettext_lazy as _
from django.shortcuts import get_object_or_404, redirect, reverse, render
from django.db.models import F
from django.core.paginator import Paginator
from django.views.generic import View

from formtools.wizard.views import SessionWizardView

from .models import AmericaReport
from .waiver_filters import report_filter
from .waiver_sorts import report_sort
from .page_through import pagination
from .waiver_form import Filters, ResponseActions, ReportEditForm
from .forms import BulkActionsForm, CommentActions, ContactEditForm, ComplaintActions, Review, PrintActions
from .views import reconstruct_query



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

        return redirect(reverse('crt_forms:individual-waiver', kwargs={'id': americareport.pk}))


@login_required
def waiver_index_view(request):
    # profile_form = ProfileForm()
    # # Check for Profile object, then add filter to request
    # if hasattr(request.user, 'profile') and request.user.profile.intake_filters:
    #     request.GET = request.GET.copy()
    #     global_section_filter = request.user.profile.intake_filters.split(',')

    #     # If assigned_section is NOT specified in request, use filter from profile
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

    return render(request, 'forms/complaint_view/index/waiver-index.html', final_data)


def serialize_data(report, request, report_id):
    output = {
        'actions': ComplaintActions(instance=report),
        'responses': ResponseActions(instance=report),
        'comments': CommentActions(),
        'print_options': PrintActions(),
        # test
        'activity_stream': {},
        'data': report,
        'return_url_args': request.GET.get('next', ''),
        'index': request.GET.get('index', ''),
        # 'summary': report.get_summary,
        # for print media consumption
        'print_actions': {},
        'questions': Review.question_text,
    }

    return output

def setup_filter_parameters(report, querydict):
    """
    If we have the `next` and `index` query parameters, then update
    the filter count, previous query, and next query so that filter
    navigation can continue apace.
    """
    output = {}
    return_url_args = querydict.get('next', '')
    index = querydict.get('index', None)

    if index == '':
        index = None

    if return_url_args and index is not None:
        requested_query = reconstruct_query(return_url_args)
        requested_ids = list(requested_query.values_list('id', flat=True))

        index = int(index)
        if report.id in requested_ids:
            # override in case user input an invalid index
            index = requested_ids.index(report.id)
            output.update({
                'filter_current': index + 1,
            })
        else:
            # this report is no longer in the filter, but we want
            # to move backwards so that the previously next report
            # becomes the actual next report.
            index -= 1

        try:
            previous_id = requested_ids[index - 1] if index > 0 else None
            next_id = requested_ids[index + 1] if index < len(requested_ids) - 1 else None
            next_query = urllib.parse.quote(return_url_args)
        except IndexError:
            # When we cannot determine the next report page we are
            # removing the next button.
            return {}

        output.update({
            'filter_count': requested_query.count(),
            'filter_previous': previous_id,
            'filter_next': next_id,
            'filter_previous_query': f'?next={next_query}&index={index - 1}',
            'filter_next_query': f'?next={next_query}&index={index + 1}',
        })

    return output


class ShowWaiverView(LoginRequiredMixin, View):
    forms = {
        form.CONTEXT_KEY: form
        for form in [ContactEditForm, ComplaintActions, ReportEditForm]
    }

    def get(self, request, id):
        report = get_object_or_404(AmericaReport, pk=id)
        output = serialize_data(report, request, report.id)
        contact_form = ContactEditForm(instance=report)
        details_form = ReportEditForm(instance=report)
        filter_output = setup_filter_parameters(report, request.GET)
        output.update({
            'contact_form': contact_form,
            'details_form': details_form,
            # test
            'email_enabled': False,
            **filter_output,
        })
        return render(request, 'forms/complaint_view/show/waiver_index.html', output)

    def get_form(self, request, report):
        form_type = request.POST.get('type')
        if not form_type:
            raise SuspiciousOperation("Invalid form data")
        return self.forms[form_type](request.POST, instance=report), form_type

    def post(self, request, id):
        """
        Multiple forms are provided on the page
        Accept only the submitted form and discard any other inbound changes
        """
        report = get_object_or_404(Report, pk=id)

        form, inbound_form_type = self.get_form(request, report)
        if form.is_valid() and form.has_changed():
            report = form.save(commit=False)

            # # Reset Assignee and Status if assigned_section is changed
            # if 'assigned_section' in form.changed_data:
            #     report.status_assignee_reset()

            # # district and location are on different forms so handled here.
            # # If the incident location changes, update the district.
            # # District can be overwritten in the drop down.
            # # If there was a location change but no new match for district, don't override.
            # if 'district' not in form.changed_data:
            #     current_district = report.district
            #     assigned_district = report.assign_district()
            #     if assigned_district and current_district != assigned_district:
            #         report.district = assigned_district
            #         description = f'Updated from "{current_district}" to "{report.district}"'
            #         add_activity(request.user, "District:", description, report)

            report.save()
            form.update_activity_stream(request.user)
            messages.add_message(request, messages.SUCCESS, form.success_message())

            url = preserve_filter_parameters(report, request.POST)
            return redirect(url)
        else:
            output = serialize_data(report, request, id)
            filter_output = setup_filter_parameters(report, request.POST)
            output.update({inbound_form_type: form, **filter_output})

            try:
                fail_message = form.FAIL_MESSAGE
            except AttributeError:
                fail_message = 'No updates applied'
            messages.add_message(request, messages.ERROR, fail_message)

            # provide new forms for those not submitted
            for form_type, form in self.forms.items():
                if form_type != inbound_form_type:
                    output.update({form_type: form(instance=report)})

            return render(request, 'forms/complaint_view/show/waiver_index.html', output)

