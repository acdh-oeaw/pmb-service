from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from browsing.browsing_utils import GenericListView, BaseCreateView, BaseUpdateView

from apis_core.apis_vocabularies.models import EventWorkRelation
from apis_core.apis_relations.models import EventWork
from apis_core.apis_relations.config import FIELDS_TO_EXCLUDE
from apis_core.apis_relations.utils import (
    generate_relation_form,
    generate_relation_filter_formhelper,
    generate_relation_filter,
    generate_relation_table,
)


class EventWorkCreate(BaseCreateView):

    model = EventWork
    form_class = generate_relation_form(EventWork)

    def get_success_url(self):
        return self.object.get_object_list_view()

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(EventWorkCreate, self).dispatch(*args, **kwargs)


class EventWorkUpdate(BaseUpdateView):

    model = EventWork
    form_class = generate_relation_form(EventWork)

    def get_success_url(self):
        return self.object.get_object_list_view()

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(EventWorkUpdate, self).dispatch(*args, **kwargs)


class EventWorkListView(GenericListView):
    model = EventWork
    filter_class = generate_relation_filter(EventWork, EventWorkRelation)
    formhelper_class = generate_relation_filter_formhelper()
    table_class = generate_relation_table(EventWork)
    init_columns = [
        "start_date_written",
        "end_date_written",
        "source",
        "relation_type",
        "target",
        "crud",
    ]
    verbose_name = "Ereignisse und Werke"
    exclude_columns = FIELDS_TO_EXCLUDE
    enable_merge = False
    template_name = "apis_relations/list_view.html"
