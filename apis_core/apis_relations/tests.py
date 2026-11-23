from django.core.exceptions import ValidationError
from django.test import TestCase

from apis_core.apis_entities.models import Person
from apis_core.apis_relations.forms2 import (
    GenericRelationForm,
    normalize_target_autocomplete_value,
)
from apis_core.apis_relations.models import PersonPerson
from apis_core.apis_vocabularies.models import PersonPersonRelation


class GenericRelationFormTestCase(TestCase):
    # fixtures = [
    #     "db.json",
    # ]

    def test_autocomplete_off_on_all_fields(self):
        """All form fields disable browser autofill (see #451)."""
        form = GenericRelationForm(
            entity_type="person",
            relation_form="PersonPlace",
        )
        self.assertTrue(form.fields)
        for name, field in form.fields.items():
            self.assertEqual(
                field.widget.attrs.get("autocomplete"),
                "off",
                msg=f"field '{name}' is missing autocomplete='off'",
            )

    def test_normalize_target_autocomplete_value_accepts_numeric_id(self):
        self.assertEqual(normalize_target_autocomplete_value("44909"), "44909")

    def test_normalize_target_autocomplete_value_extracts_db_id_from_html_label(self):
        value = (
            "<span ><small>db</small> <b>Altaussee 43</b> "
            "<small>db-ID: 44909</small> </span>"
        )
        self.assertEqual(normalize_target_autocomplete_value(value), "44909")

    def test_normalize_target_autocomplete_value_accepts_urls(self):
        value = "https://example.org/entity/123"
        self.assertEqual(normalize_target_autocomplete_value(value), value)

    def test_normalize_target_autocomplete_value_rejects_plain_text(self):
        with self.assertRaises(ValidationError) as exc_info:
            normalize_target_autocomplete_value("Altaussee 43")

        self.assertEqual(exc_info.exception.code, "invalid")

    def test_form_is_valid_and_normalizes_html_target_value(self):
        form_combinations = [
            ("person", "PersonPlace"),
            ("person", "PersonPerson"),
            ("person", "PersonInstitution"),
            ("institution", "PersonInstitution"),
            ("person", "PersonEvent"),
            ("person", "PersonWork"),
            ("institution", "InstitutionPlace"),
            ("institution", "InstitutionInstitution"),
            ("institution", "InstitutionEvent"),
            ("institution", "InstitutionWork"),
            ("place", "PlaceEvent"),
            ("place", "PlaceWork"),
            ("place", "PlacePlace"),
            ("event", "EventWork"),
            ("event", "EventEvent"),
            ("work", "WorkWork"),
        ]

        for entity_type, relation_form in form_combinations:
            with self.subTest(entity_type=entity_type, relation_form=relation_form):
                form = GenericRelationForm(
                    entity_type=entity_type,
                    relation_form=relation_form,
                    data={
                        "relation_type": "1",
                        "target": (
                            "<span ><small>db</small> <b>Altaussee 43</b> "
                            "<small>db-ID: 44909</small> </span>"
                        ),
                        "start_date_written": "",
                        "end_date_written": "",
                        "references": "",
                        "notes": "",
                    },
                )

                self.assertTrue(form.is_valid(), msg=form.errors.as_json())
                self.assertEqual(form.cleaned_data["target"], "44909")


class SameEntityRelationDirectionTestCase(TestCase):
    """Editing a relation between two entities of the same type must not swap
    its sides (and thereby reverse its meaning), no matter from which entity's
    page it is edited."""

    @classmethod
    def setUpTestData(cls):
        cls.father = Person.objects.create(name="Vater")
        cls.son = Person.objects.create(name="Sohn")
        cls.is_father_of = PersonPersonRelation.objects.create(
            name="ist Vater von", name_reverse="ist Sohn von"
        )
        cls.knows = PersonPersonRelation.objects.create(
            name="kennt", name_reverse="kennt"
        )

    def _save(self, site, target, relation, relation_type, notes="edited"):
        # mirrors save_ajax_form: the form is built without the instance
        form = GenericRelationForm(
            entity_type=Person,
            relation_form="PersonPerson",
            data={
                "relation_type": f"{relation_type.id}",
                "target": f"{target.id}",
                "start_date_written": "",
                "end_date_written": "",
                "references": "",
                "notes": notes,
            },
        )
        self.assertTrue(form.is_valid(), msg=form.errors.as_json())
        form.save(site_instance=site, instance=relation.pk)
        relation.refresh_from_db()

    def _relation(self):
        return PersonPerson.objects.create(
            related_persona=self.father,
            related_personb=self.son,
            relation_type=self.is_father_of,
        )

    def test_edit_from_a_side_keeps_direction(self):
        rel = self._relation()
        self._save(self.father, self.son, rel, self.is_father_of)
        self.assertEqual(rel.related_persona, self.father)
        self.assertEqual(rel.related_personb, self.son)
        self.assertEqual(rel.notes, "edited")

    def test_edit_from_b_side_keeps_direction(self):
        rel = self._relation()
        self._save(self.son, self.father, rel, self.is_father_of)
        self.assertEqual(rel.related_persona, self.father)
        self.assertEqual(rel.related_personb, self.son)
        self.assertEqual(rel.relation_type, self.is_father_of)
        self.assertEqual(rel.notes, "edited")

    def test_new_type_from_b_side_puts_current_entity_on_a(self):
        # a newly chosen type is picked from the forward labels
        rel = self._relation()
        self._save(self.son, self.father, rel, self.knows)
        self.assertEqual(rel.related_persona, self.son)
        self.assertEqual(rel.related_personb, self.father)
        self.assertEqual(rel.relation_type, self.knows)

    def test_new_relation_puts_current_entity_on_a(self):
        form = GenericRelationForm(
            entity_type=Person,
            relation_form="PersonPerson",
            data={
                "relation_type": f"{self.is_father_of.id}",
                "target": f"{self.son.id}",
                "start_date_written": "",
                "end_date_written": "",
                "references": "",
                "notes": "",
            },
        )
        self.assertTrue(form.is_valid(), msg=form.errors.as_json())
        rel = form.save(site_instance=self.father)
        self.assertEqual(rel.related_persona, self.father)
        self.assertEqual(rel.related_personb, self.son)
