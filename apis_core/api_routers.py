from functools import reduce

from django.conf import settings
from django.urls import reverse
from django_filters import rest_framework as filters
from rest_framework import pagination, renderers, serializers, viewsets
from rest_framework.filters import OrderingFilter
from rest_framework.response import Response

from apis_core.helper_functions.ContentType import GetContentTypes

from .api_renderers import NetJsonRenderer
from .apis_metainfo.models import TempEntityClass

try:
    MAX_AGE = settings.MAX_AGE
except AttributeError:
    MAX_AGE = 0


def deep_get(dictionary, keys, default=None):
    return reduce(
        lambda d, key: d.get(key, default) if isinstance(d, dict) else default,
        keys.split("."),
        dictionary,
    )


class CustomPagination(pagination.LimitOffsetPagination):
    def get_paginated_response(self, data):
        return Response(
            {
                "next": self.get_next_link(),
                "previous": self.get_previous_link(),
                "count": self.count,
                "limit": self.limit,
                "offset": self.offset,
                "results": data,
            }
        )


class ApisBaseSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    label = serializers.SerializerMethodField(method_name="add_label")
    url = serializers.SerializerMethodField(method_name="add_uri")

    def add_id(self, obj):
        return obj.pk

    def add_label(self, obj):
        return str(obj)

    def add_uri(self, obj):
        return self.context["view"].request.build_absolute_uri(
            reverse(
                "apis:apis_api:{}-detail".format(obj.__class__.__name__.lower()),
                kwargs={"pk": obj.pk},
            )
        )

    def add_type(self, obj):
        lst_type = ["kind", "type", "collection_type", "relation_type"]
        lst_kind = [
            x
            for x in obj._meta.fields
            if x.name in lst_type and "apis_vocabularies" in str(x.related_model)
        ]
        if len(lst_kind):
            pk_obj = getattr(obj, f"{lst_kind[0].name}_id")
            if pk_obj is not None:
                obj_type = getattr(obj, str(lst_kind[0].name))
                res = {
                    "id": pk_obj,
                    "url": self.context["view"].request.build_absolute_uri(
                        reverse(
                            f"apis:apis_api:{lst_kind[0].related_model.__name__.lower()}-detail",
                            kwargs={"pk": pk_obj},
                        )
                    ),
                    "type": obj_type.__class__.__name__,
                    "label": str(obj_type),
                    "parent_class": getattr(obj, "parent_class_id", None),
                }
                return res

    class Meta:
        model = TempEntityClass
        fields = ["id", "label", "url"]


class EntitySerializer(ApisBaseSerializer):
    type = serializers.SerializerMethodField(method_name="add_type")
    sameAs = serializers.SerializerMethodField(method_name="add_sameas")

    def add_type(self, instance):
        return instance.__class__.__name__

    def add_sameas(self, instance):
        res = []
        for uri in instance.uri_set.all():
            res.append(uri.uri)
        return res

    class Meta(ApisBaseSerializer.Meta):
        fields = ApisBaseSerializer.Meta.fields + ["type", "sameAs"]


class LabelSerializer(ApisBaseSerializer):
    parent_id = serializers.PrimaryKeyRelatedField(
        many=False, source="parent_class_id", read_only=True
    )

    def add_parent_id(self, obj):
        return obj.parent_class_id

    class Meta(ApisBaseSerializer.Meta):
        fields = ApisBaseSerializer.Meta.fields + [
            "parent_id",
        ]


class VocabsBaseSerializer(LabelSerializer, EntitySerializer):
    pass


class RelationObjectSerializer2(ApisBaseSerializer):
    relation_type = VocabsBaseSerializer(read_only=True)
    related_entity = serializers.SerializerMethodField(method_name="add_related_entity")

    def add_related_entity(self, instance):
        for at in dir(instance):
            if (
                at.startswith("related_")
                and at.endswith("_id")
                and getattr(instance, at) != self._pk_instance
            ):
                return EntitySerializer(
                    getattr(instance, at[:-3]), context=self.context
                ).data

    class Meta(ApisBaseSerializer.Meta):
        fields = ApisBaseSerializer.Meta.fields + ["relation_type", "related_entity"]

    def __init__(self, *args, **kwargs):
        self._pk_instance = kwargs.pop("pk_instance")
        super(RelationObjectSerializer2, self).__init__(*args, **kwargs)


def generic_serializer_creation_factory():
    lst_cont = GetContentTypes().get_model_classes()
    not_allowed_filter_fields = [
        "useradded",
        "vocab_name",
        "parent_class",
        "vocab",
        "entity",
        "autofield",
    ]
    for cont in lst_cont:
        prefetch_rel = []
        select_related = []
        test_search = getattr(settings, cont.__module__.split(".")[1].upper(), False)
        entity_str = str(cont.__name__).replace(" ", "")
        entity = cont
        app_label = cont.__module__.split(".")[1].lower()
        exclude_lst = []
        if app_label == "apis_entities":
            exclude_lst = deep_get(test_search, "{}.api_exclude".format(entity_str), [])
            for f in entity._meta.get_fields():
                if "_set" in str(f):
                    to_exclude = str(f).split(".")[-1]
                    exclude_lst.append(to_exclude)
        else:
            set_prem = getattr(settings, cont.__module__.split(".")[1].upper(), {})
            exclude_lst = deep_get(set_prem, "exclude", [])
            exclude_lst.extend(deep_get(set_prem, "{}.exclude".format(entity_str), []))
        entity_field_name_list = []
        for x in entity._meta.get_fields():
            entity_field_name_list.append(x.name)
        exclude_lst_fin = []
        for x in exclude_lst:
            if x in entity_field_name_list:
                exclude_lst_fin.append(x)
        if entity_str.lower() == "text":
            exclude_lst_fin.extend(["kind", "source"])
        if app_label == "apis_relations":
            exclude_lst_fin.extend(["text", "collection"])
        for f in entity._meta.get_fields():
            if f.__class__.__name__ == "ManyToManyField":
                prefetch_rel.append(f.name)
            elif f.__class__.__name__ == "ForeignKey":
                select_related.append(f.name)

        class TemplateSerializer(serializers.HyperlinkedModelSerializer):
            id = serializers.ReadOnlyField()
            url = serializers.HyperlinkedIdentityField(
                view_name=f"apis:apis_api:{entity_str.lower()}-detail"
            )
            _entity = entity
            _exclude_lst = exclude_lst_fin
            _app_label = app_label

            class Meta:
                model = entity
                exclude = exclude_lst_fin

            def add_labels(self, obj):
                return {"id": obj.pk, "label": str(obj)}

            def add_sameas(self, instance):
                res = []
                for uri in instance.uri_set.all():
                    res.append(uri.uri)
                return res

            if entity_str.lower() == "text":

                def __init__(self, *args, **kwargs):
                    super().__init__(*args, **kwargs)
                    self._highlight = False
                    self.fields["kind"] = LabelSerializer(many=False, read_only=True)

            else:

                def __init__(self, *args, **kwargs):
                    super().__init__(*args, **kwargs)
                    app_label = self._app_label
                    if app_label == "apis_entities":
                        self.fields["sameAs"] = serializers.SerializerMethodField(
                            "add_sameas"
                        )
                    for f in self._entity._meta.get_fields():
                        ck_many = f.__class__.__name__ == "ManyToManyField"
                        if f.name in self._exclude_lst:
                            continue
                        elif f.__class__.__name__ in [
                            "ManyToManyField",
                            "ForeignKey",
                        ] and "apis_vocabularies" not in str(f.related_model):
                            self.fields[f.name] = ApisBaseSerializer(
                                many=ck_many, read_only=True
                            )
                        elif f.__class__.__name__ in ["ManyToManyField", "ForeignKey"]:
                            self.fields[f.name] = LabelSerializer(
                                many=ck_many, read_only=True
                            )

        TemplateSerializer.__name__ = TemplateSerializer.__qualname__ = (
            f"{entity_str.title().replace(' ', '')}Serializer"
        )

        class TemplateSerializerRetrieve(TemplateSerializer):
            if entity_str.lower() == "text":
                text = serializers.SerializerMethodField(
                    method_name="txt_serializer_add_text"
                )

                def __init__(self, *args, **kwargs):
                    super().__init__(*args, **kwargs)
                    self._inline_annotations = False
                    self._highlight = False
                    self.fields["kind"] = LabelSerializer(many=False, read_only=True)

                def txt_serializer_add_text(self, instance):
                    if self._inline_annotations:
                        return self._txt_html
                    else:
                        return instance.text

            else:

                def __init__(self, *args, **kwargs):
                    super().__init__(*args, **kwargs)
                    for f in self._entity._meta.get_fields():
                        ck_many = f.__class__.__name__ == "ManyToManyField"
                        if f.name in self._exclude_lst:
                            continue
                        elif f.__class__.__name__ in [
                            "ManyToManyField",
                            "ForeignKey",
                        ] and "apis_vocabularies" not in str(f.related_model):
                            self.fields[f.name] = ApisBaseSerializer(
                                many=ck_many, read_only=True
                            )
                        elif f.__class__.__name__ in ["ManyToManyField", "ForeignKey"]:
                            self.fields[f.name] = LabelSerializer(
                                many=ck_many, read_only=True
                            )

        TemplateSerializerRetrieve.__name__ = (
            TemplateSerializerRetrieve.__qualname__
        ) = f"{entity_str.title().replace(' ', '')}DetailSerializer"

        allowed_fields_filter = {
            "IntegerField": ["in", "range", "exact"],
            "CharField": ["exact", "icontains", "iregex", "isnull"],
            "DateField": ["year", "lt", "gt", "year__lt", "year__gt", "exact"],
            "PositiveIntegerField": ["in", "range", "exact"],
            "AutoField": ["in", "exact"],
        }
        filterset_dict = {}
        filter_fields = {}

        for field in entity._meta.fields + entity._meta.many_to_many:
            if getattr(settings, "APIS_API_EXCLUDE_SETS", False) and "_set" in str(
                field.name.lower()
            ):
                continue
            if (
                field.name.lower() in not_allowed_filter_fields
                or field.name == "tempentityclass_ptr"
            ):
                continue
            elif field.__class__.__name__ in ["ForeignKey", "ManyToManyField"]:
                filter_fields[field.name] = ["exact"]
                if field.__class__.__name__ == "ForeignKey":
                    filter_fields[field.name].append("in")
                for f2 in field.related_model._meta.fields:
                    if f2.__class__.__name__ in [
                        "CharField",
                        "DateField",
                        "IntegerField",
                        "AutoField",
                    ]:
                        filter_fields[f"{field.name}__{f2.name}"] = (
                            allowed_fields_filter[f2.__class__.__name__]
                        )
                continue
            if field.__class__.__name__ in allowed_fields_filter.keys():
                filter_fields[field.name] = allowed_fields_filter[
                    field.__class__.__name__
                ]
            else:
                filter_fields[field.name] = ["exact"]
        additional_filters = getattr(settings, "APIS_API_ADDITIONAL_FILTERS", False)
        if additional_filters:
            if entity_str in additional_filters.keys():
                for f1 in additional_filters[entity_str]:
                    if f1[0] not in filter_fields.keys():
                        filter_fields[f1[0]] = f1[1]

        class MetaFilter(object):
            model = entity
            fields = filter_fields

        filterset_dict["Meta"] = MetaFilter

        class TemplateViewSet(viewsets.ReadOnlyModelViewSet):
            _select_related = select_related
            _prefetch_rel = prefetch_rel
            pagination_class = CustomPagination
            model = entity
            filter_backends = (filters.DjangoFilterBackend, OrderingFilter)
            filterset_fields = filter_fields
            depth = 2
            renderer_classes = [
                renderers.JSONRenderer,
                renderers.BrowsableAPIRenderer,
            ]
            if app_label == "apis_relations":
                renderer_classes.append(NetJsonRenderer)

            _serializer_class = TemplateSerializer
            _serializer_class_retrieve = TemplateSerializerRetrieve

            def get_serializer_class(self, *arg, **kwargs):
                if self.action == "list":
                    return self._serializer_class
                else:
                    return self._serializer_class_retrieve

            def get_serializer_context(self):
                context = super(self.__class__, self).get_serializer_context()
                return context

            def get_queryset(self):
                return self.model.objects.all()

            def list_viewset(self, request):
                res = super(self.__class__, self).list(request)
                return res

            def dispatch(self, request, *args, **kwargs):
                return super(self.__class__, self).dispatch(request, *args, **kwargs)

            def retrieve(self, request, pk=None):
                res = super(self.__class__, self).retrieve(request, pk=pk)
                return res

        TemplateViewSet.__name__ = TemplateViewSet.__qualname__ = (
            f"Generic{entity_str.title().replace(' ', '')}ViewSet"
        )

        serializers_dict[TemplateSerializer.__name__] = TemplateSerializer
        views[f"{entity_str.lower().replace(' ', '')}"] = TemplateViewSet


serializers_dict = dict()
views = dict()
generic_serializer_creation_factory()
