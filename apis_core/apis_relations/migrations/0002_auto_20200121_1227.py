# Generated by Django 2.1.12 on 2020-01-21 12:27

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("apis_vocabularies", "0001_initial"),
        ("apis_relations", "0001_initial"),
        ("apis_entities", "0002_auto_20200121_1227"),
    ]

    operations = [
        migrations.AddField(
            model_name="workwork",
            name="relation_type",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="workwork_set",
                to="apis_vocabularies.WorkWorkRelation",
            ),
        ),
        migrations.AddField(
            model_name="placework",
            name="related_place",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="placework_set",
                to="apis_entities.Place",
            ),
        ),
        migrations.AddField(
            model_name="placework",
            name="related_work",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="placework_set",
                to="apis_entities.Work",
            ),
        ),
        migrations.AddField(
            model_name="placework",
            name="relation_type",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="placework_set",
                to="apis_vocabularies.PlaceWorkRelation",
            ),
        ),
        migrations.AddField(
            model_name="placeplace",
            name="related_placea",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="related_placeb",
                to="apis_entities.Place",
            ),
        ),
        migrations.AddField(
            model_name="placeplace",
            name="related_placeb",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="related_placea",
                to="apis_entities.Place",
            ),
        ),
        migrations.AddField(
            model_name="placeplace",
            name="relation_type",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="placeplace_set",
                to="apis_vocabularies.PlacePlaceRelation",
            ),
        ),
        migrations.AddField(
            model_name="placeevent",
            name="related_event",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="placeevent_set",
                to="apis_entities.Event",
            ),
        ),
        migrations.AddField(
            model_name="placeevent",
            name="related_place",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="placeevent_set",
                to="apis_entities.Place",
            ),
        ),
        migrations.AddField(
            model_name="placeevent",
            name="relation_type",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="placeevent_set",
                to="apis_vocabularies.PlaceEventRelation",
            ),
        ),
        migrations.AddField(
            model_name="personwork",
            name="related_person",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="personwork_set",
                to="apis_entities.Person",
            ),
        ),
        migrations.AddField(
            model_name="personwork",
            name="related_work",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="personwork_set",
                to="apis_entities.Work",
            ),
        ),
        migrations.AddField(
            model_name="personwork",
            name="relation_type",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="personwork_set",
                to="apis_vocabularies.PersonWorkRelation",
            ),
        ),
        migrations.AddField(
            model_name="personplace",
            name="related_person",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="personplace_set",
                to="apis_entities.Person",
            ),
        ),
        migrations.AddField(
            model_name="personplace",
            name="related_place",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="personplace_set",
                to="apis_entities.Place",
            ),
        ),
        migrations.AddField(
            model_name="personplace",
            name="relation_type",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="personplace_set",
                to="apis_vocabularies.PersonPlaceRelation",
            ),
        ),
        migrations.AddField(
            model_name="personperson",
            name="related_persona",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="related_personb",
                to="apis_entities.Person",
            ),
        ),
        migrations.AddField(
            model_name="personperson",
            name="related_personb",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="related_persona",
                to="apis_entities.Person",
            ),
        ),
        migrations.AddField(
            model_name="personperson",
            name="relation_type",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="personperson_set",
                to="apis_vocabularies.PersonPersonRelation",
            ),
        ),
        migrations.AddField(
            model_name="personinstitution",
            name="related_institution",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="personinstitution_set",
                to="apis_entities.Institution",
            ),
        ),
        migrations.AddField(
            model_name="personinstitution",
            name="related_person",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="personinstitution_set",
                to="apis_entities.Person",
            ),
        ),
        migrations.AddField(
            model_name="personinstitution",
            name="relation_type",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="personinstitution_set",
                to="apis_vocabularies.PersonInstitutionRelation",
            ),
        ),
        migrations.AddField(
            model_name="personevent",
            name="related_event",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="personevent_set",
                to="apis_entities.Event",
            ),
        ),
        migrations.AddField(
            model_name="personevent",
            name="related_person",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="personevent_set",
                to="apis_entities.Person",
            ),
        ),
        migrations.AddField(
            model_name="personevent",
            name="relation_type",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="personevent_set",
                to="apis_vocabularies.PersonEventRelation",
            ),
        ),
        migrations.AddField(
            model_name="institutionwork",
            name="related_institution",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="institutionwork_set",
                to="apis_entities.Institution",
            ),
        ),
        migrations.AddField(
            model_name="institutionwork",
            name="related_work",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="institutionwork_set",
                to="apis_entities.Work",
            ),
        ),
        migrations.AddField(
            model_name="institutionwork",
            name="relation_type",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="institutionwork_set",
                to="apis_vocabularies.InstitutionWorkRelation",
            ),
        ),
        migrations.AddField(
            model_name="institutionplace",
            name="related_institution",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="institutionplace_set",
                to="apis_entities.Institution",
            ),
        ),
        migrations.AddField(
            model_name="institutionplace",
            name="related_place",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="institutionplace_set",
                to="apis_entities.Place",
            ),
        ),
        migrations.AddField(
            model_name="institutionplace",
            name="relation_type",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="institutionplace_set",
                to="apis_vocabularies.InstitutionPlaceRelation",
            ),
        ),
        migrations.AddField(
            model_name="institutioninstitution",
            name="related_institutionA",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="related_institutionB",
                to="apis_entities.Institution",
            ),
        ),
        migrations.AddField(
            model_name="institutioninstitution",
            name="related_institutionB",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="related_institutionA",
                to="apis_entities.Institution",
            ),
        ),
        migrations.AddField(
            model_name="institutioninstitution",
            name="relation_type",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="institutioninstitution_set",
                to="apis_vocabularies.InstitutionInstitutionRelation",
            ),
        ),
        migrations.AddField(
            model_name="institutionevent",
            name="related_event",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="institutionevent_set",
                to="apis_entities.Event",
            ),
        ),
        migrations.AddField(
            model_name="institutionevent",
            name="related_institution",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="institutionevent_set",
                to="apis_entities.Institution",
            ),
        ),
        migrations.AddField(
            model_name="institutionevent",
            name="relation_type",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="institutionevent_set",
                to="apis_vocabularies.InstitutionEventRelation",
            ),
        ),
        migrations.AddField(
            model_name="eventwork",
            name="related_event",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="eventwork_set",
                to="apis_entities.Event",
            ),
        ),
        migrations.AddField(
            model_name="eventwork",
            name="related_work",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="eventwork_set",
                to="apis_entities.Work",
            ),
        ),
        migrations.AddField(
            model_name="eventwork",
            name="relation_type",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="eventwork_set",
                to="apis_vocabularies.EventWorkRelation",
            ),
        ),
        migrations.AddField(
            model_name="eventevent",
            name="related_eventa",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="related_eventb",
                to="apis_entities.Event",
            ),
        ),
        migrations.AddField(
            model_name="eventevent",
            name="related_eventb",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="related_eventa",
                to="apis_entities.Event",
            ),
        ),
        migrations.AddField(
            model_name="eventevent",
            name="relation_type",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="eventevent_set",
                to="apis_vocabularies.EventEventRelation",
            ),
        ),
    ]
