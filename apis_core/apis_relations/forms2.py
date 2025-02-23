import copy
import re

from crispy_forms.bootstrap import Accordion, AccordionGroup
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout
from dal import autocomplete
from django import forms
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db.models import Q
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from apis_core.apis_entities.fields import ListSelect2
from apis_core.apis_entities.models import AbstractEntity

from apis_core.apis_metainfo.models import TempEntityClass, Uri
from apis_core.apis_relations.models import AbstractRelation
from apis_core.helper_functions import DateParser

from .tables import get_generic_relations_table


def validate_target_autocomplete(value):
    try:
        value = int(value)
    except ValueError:
        if value.startswith("http"):
            pass
        else:
            raise ValidationError(
                _("Invalid value: %(value)s, use either URLs or select a value"),
                code="invalid",
                params={"value": value},
            )


class GenericRelationForm(forms.ModelForm):
    class Meta:
        model = TempEntityClass
        fields = ["start_date_written", "end_date_written", "references", "notes"]
        labels = {
            "start_date_written": _("Start"),
            "end_date_written": _("End"),
        }

    def save(self, site_instance, instance=None, commit=True):
        """
        Save function of the GenericRelationForm.
        :param site_instance: Instance where the form is used on
        :param instance: PK of the relation that is saved
        :param commit: Whether to already commit the save.
        :type site_instance: object
        :type instance: int
        :type commit: bool
        :rtype: object
        :return: instance of relation
        """
        cd = self.cleaned_data
        if instance:
            x = self.relation_form.objects.get(pk=instance)
        else:
            x = self.relation_form()
        if f"{site_instance.id}" == f'{cd["target"]}':
            return x
        x.relation_type_id = cd["relation_type"]
        x.start_date_written = cd["start_date_written"]
        x.end_date_written = cd["end_date_written"]
        x.notes = cd["notes"]
        x.references = cd["references"]
        setattr(x, self.rel_accessor[3], site_instance)
        target = AbstractEntity.get_entity_class_of_name(self.rel_accessor[0])
        t1 = target.get_or_create_uri(cd["target"])
        setattr(x, self.rel_accessor[2], t1)
        params = {
            self.rel_accessor[3]: site_instance,
            self.rel_accessor[2]: t1,
            "start_date_written": cd["start_date_written"],
            "end_date_written": cd["end_date_written"],
            "relation_type_id": cd["relation_type"],
        }
        if commit:
            qs = x.__class__.objects.filter(**params)
            if qs.count() > 0:
                pass
            else:
                x.save()
        return x

    def get_text_id(self):
        """
        Function to retrieve the highlighted text.
        :return: ID of text that was highlighted
        """
        return self.cleaned_data["HL_text_id"][5:]

    def get_html_table(self, entity_type, request, site_instance, form_match):
        table = get_generic_relations_table(
            relation_class=self.relation_form,
            entity_instance=site_instance,
            detail=False,
        )
        prefix = re.match(
            r"([A-Z][a-z])[^A-Z]*([A-Z][a-z])", self.relation_form.__name__
        )
        prefix = prefix.group(1) + prefix.group(2) + "-"
        if form_match.group(1) == form_match.group(2):
            dic_a = {"related_" + entity_type.lower() + "a": site_instance}
            dic_b = {"related_" + entity_type.lower() + "b": site_instance}
            objects = self.relation_form.objects.filter(
                Q(**dic_a) | Q(**dic_b)
            ).order_by("-updated")[:10]
            table_html = table(data=objects, prefix=prefix)
        else:
            tab_query = {"related_" + entity_type.lower(): site_instance}
            ttab = self.relation_form.objects.filter(**tab_query).order_by("-updated")[
                :10
            ]
            table_html = table(data=ttab, prefix=prefix)
        return table_html

    def __init__(self, siteID=None, highlighter=False, *args, **kwargs):
        """
        Generic Form for relations.
        :param siteID: ID of the entity the form is used on
        :param entity_type: Entity type of the entity the form is used on
        :param relation_form: Type of relation form.
        :param instance: instance of relation.
        :param highlighter: whether the form is used in the highlighter
        :type siteID: int
        :type entity_type: object or int
        :type relation_form: object or int
        :type instance: object
        :type highlighter: bool
        """
        attrs = {
            "data-placeholder": "Type to get suggestions",
            "data-minimum-input-length": 0,
            "data-html": True,
            "style": "width: 100%",
        }
        help_text_target = "Search and select or use an URL from a reference resource"
        attrs_target = copy.deepcopy(attrs)
        attrs_target["data-tags"] = "1"
        css_notes = "LS"
        self.highlighter = highlighter
        entity_type = kwargs.pop("entity_type")
        if type(entity_type) != str:
            entity_type = entity_type.__name__
        self.relation_form = kwargs.pop("relation_form")
        if type(self.relation_form) == str:
            self.relation_form = AbstractRelation.get_relation_class_of_name(
                self.relation_form
            )
        self.request = kwargs.pop("request", False)
        super(GenericRelationForm, self).__init__(*args, **kwargs)
        instance = getattr(self, "instance", None)
        self.fields["relation_type"] = forms.CharField(
            label="Relation type", required=True
        )
        self.helper = FormHelper()
        self.helper.form_class = "{}Form".format(str(self.relation_form))
        self.helper.form_tag = False
        lst_src_target = re.findall("[A-Z][^A-Z]*", self.relation_form.__name__)
        if lst_src_target[0] == lst_src_target[1]:
            if instance and instance.id:
                if getattr(
                    instance, "related_{}a_id".format(lst_src_target[0].lower())
                ) == int(siteID):
                    self.rel_accessor = (
                        lst_src_target[1],
                        True,
                        "related_{}b".format(lst_src_target[1].lower()),
                        "related_{}a".format(lst_src_target[0].lower()),
                    )
                else:
                    self.rel_accessor = (
                        lst_src_target[1],
                        False,
                        "related_{}a".format(lst_src_target[1].lower()),
                        "related_{}b".format(lst_src_target[0].lower()),
                    )
            else:
                self.rel_accessor = (
                    lst_src_target[1],
                    True,
                    "related_{}b".format(lst_src_target[1].lower()),
                    "related_{}a".format(lst_src_target[0].lower()),
                )
            self.fields["relation_type"] = autocomplete.Select2ListCreateChoiceField(
                label="Relation type",
                widget=ListSelect2(
                    url=reverse(
                        "apis:apis_vocabularies:generic_vocabularies_autocomplete",
                        args=[
                            "".join(
                                [
                                    lst_src_target[0].lower(),
                                    lst_src_target[1].lower(),
                                    "relation",
                                ]
                            ),
                            "normal",
                        ],
                    ),
                    attrs=attrs,
                ),
            )
            self.fields["target"] = autocomplete.Select2ListCreateChoiceField(
                label=lst_src_target[1],
                widget=ListSelect2(
                    url=reverse(
                        "apis:apis_entities:generic_entities_autocomplete",
                        args=[lst_src_target[1].lower()],
                    ),
                    attrs=attrs_target,
                ),
                validators=[validate_target_autocomplete],
                help_text=help_text_target,
            )
        elif entity_type.lower() == lst_src_target[0].lower():
            self.rel_accessor = (
                lst_src_target[1],
                True,
                "related_{}".format(lst_src_target[1].lower()),
                "related_{}".format(lst_src_target[0].lower()),
            )
            self.fields["relation_type"] = autocomplete.Select2ListCreateChoiceField(
                label="Relation type",
                widget=ListSelect2(
                    url=reverse(
                        "apis:apis_vocabularies:generic_vocabularies_autocomplete",
                        args=[
                            "".join(
                                [
                                    lst_src_target[0].lower(),
                                    lst_src_target[1].lower(),
                                    "relation",
                                ]
                            ),
                            "normal",
                        ],
                    ),
                    attrs=attrs,
                ),
            )
            self.fields["target"] = autocomplete.Select2ListCreateChoiceField(
                label=lst_src_target[1],
                widget=ListSelect2(
                    # url='/entities/autocomplete/{}'.format(lst_src_target[1].lower()),
                    url=reverse(
                        "apis:apis_entities:generic_entities_autocomplete",
                        args=[lst_src_target[1].lower()],
                    ),
                    attrs=attrs_target,
                ),
                validators=[validate_target_autocomplete],
                help_text=help_text_target,
            )
        elif entity_type.lower() == lst_src_target[1].lower():
            self.rel_accessor = (
                lst_src_target[0],
                False,
                "related_{}".format(lst_src_target[0].lower()),
                "related_{}".format(lst_src_target[1].lower()),
            )
            self.fields["relation_type"] = autocomplete.Select2ListCreateChoiceField(
                label="Relation type",
                widget=ListSelect2(
                    url=reverse(
                        "apis:apis_vocabularies:generic_vocabularies_autocomplete",
                        args=[
                            "".join(
                                [
                                    lst_src_target[0].lower(),
                                    lst_src_target[1].lower(),
                                    "relation",
                                ]
                            ),
                            "reverse",
                        ],
                    ),
                    attrs=attrs,
                ),
            )
            self.fields["target"] = autocomplete.Select2ListCreateChoiceField(
                label=lst_src_target[0],
                widget=ListSelect2(
                    url=reverse(
                        "apis:apis_entities:generic_entities_autocomplete",
                        args=[lst_src_target[0].lower()],
                    ),
                    attrs=attrs_target,
                ),
                validators=[validate_target_autocomplete],
                help_text=help_text_target,
            )
        else:
            pass
        if instance and instance.id:
            self.fields["target"].choices = [
                (
                    str(
                        Uri.objects.filter(
                            entity=getattr(instance, self.rel_accessor[2])
                        )[0]
                    ),
                    str(getattr(instance, self.rel_accessor[2])),
                )
            ]
            self.fields["target"].initial = (
                str(
                    Uri.objects.filter(entity=getattr(instance, self.rel_accessor[2]))[
                        0
                    ]
                ),
                str(getattr(instance, self.rel_accessor[2])),
            )
            if self.rel_accessor[1]:
                self.fields["relation_type"].choices = [
                    (instance.relation_type.id, instance.relation_type.label)
                ]
                self.fields["relation_type"].initial = (
                    instance.relation_type.id,
                    instance.relation_type.label,
                )
            else:
                self.fields["relation_type"].choices = [
                    (instance.relation_type.id, instance.relation_type.label_reverse)
                ]
                self.fields["relation_type"].initial = (
                    instance.relation_type.id,
                    instance.relation_type.label_reverse,
                )

        self.helper.include_media = False
        self.helper.layout = Layout(
            "relation_type",
            "target",
            "start_date_written",
            "end_date_written",
            Accordion(
                AccordionGroup(
                    "Notes and References",
                    "notes",
                    "references",
                    active=False,
                    css_id="{}_{}_notes_refs".format(
                        self.relation_form.__name__, css_notes
                    ),
                )
            ),
        )

        if instance != None:
            if instance.start_date_written:
                self.fields["start_date_written"].help_text = (
                    DateParser.get_date_help_text_from_dates(
                        single_date=instance.start_date,
                        single_start_date=instance.start_start_date,
                        single_end_date=instance.start_end_date,
                        single_date_written=instance.start_date_written,
                    )
                )
            else:
                self.fields["start_date_written"].help_text = (
                    DateParser.get_date_help_text_default()
                )

            if instance.end_date_written:
                self.fields["end_date_written"].help_text = (
                    DateParser.get_date_help_text_from_dates(
                        single_date=instance.end_date,
                        single_start_date=instance.end_start_date,
                        single_end_date=instance.end_end_date,
                        single_date_written=instance.end_date_written,
                    )
                )
            else:
                self.fields["end_date_written"].help_text = (
                    DateParser.get_date_help_text_default()
                )
