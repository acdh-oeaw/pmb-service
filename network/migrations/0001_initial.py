# Generated by Django 5.1.1 on 2024-11-23 07:42

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Edge",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "edge_id",
                    models.IntegerField(
                        help_text="ID der Kante", verbose_name="ID der Kante"
                    ),
                ),
                (
                    "edge_kind",
                    models.CharField(
                        choices=[
                            ("personperson", "Personen und Personen"),
                            ("personplace", "Personen und Orte"),
                            ("personwork", "Personen und Werke"),
                            ("personevent", "Personen und Ereignisse"),
                            ("personinstitution", "Personen und Institutionen"),
                            (
                                "institutioninstitution",
                                "Institutionen und Institutionen",
                            ),
                            ("institutionplace", "Institutionen und Orte"),
                            ("institutionwork", "Institutionen und Werke"),
                            ("institutionevent", "Institutionen und Ereignisse"),
                            ("placeplace", "Orte und Orte"),
                            ("placework", "Orte und Werke"),
                            ("placeevent", "Orte und Ereignisse"),
                            ("eventevent", "Ereignisse und Ereignisse"),
                            ("eventwork", "Ereignisse und Werke"),
                            ("workwork", "Werke und Werke"),
                        ],
                        help_text="Art der Beziehung (Personen und Orte, Werke und Werke, ...)",
                        max_length=100,
                        verbose_name="Kantentyp",
                    ),
                ),
                (
                    "source_label",
                    models.CharField(
                        help_text="Name der Quelle",
                        max_length=250,
                        verbose_name="Name der Quelle",
                    ),
                ),
                (
                    "source_kind",
                    models.CharField(
                        help_text="Art der Quelle (Person, Ort, Werk, Institution, Ereignis)",
                        max_length=250,
                        verbose_name="Art der Quelle",
                    ),
                ),
                (
                    "source_id",
                    models.IntegerField(
                        help_text="ID der Quelle", verbose_name="ID der Quelle"
                    ),
                ),
                (
                    "edge_label",
                    models.CharField(
                        help_text="Art der Beziehung von Quell- und Zielknoten",
                        max_length=250,
                        verbose_name="Art der Beziehung",
                    ),
                ),
                (
                    "target_label",
                    models.CharField(
                        help_text="Name des Ziels",
                        max_length=250,
                        verbose_name="Name des Ziels",
                    ),
                ),
                (
                    "target_kind",
                    models.CharField(
                        help_text="Art des Ziels (Person, Ort, Werk, Institution, Ereignis)",
                        max_length=250,
                        verbose_name="Art des Ziels",
                    ),
                ),
                (
                    "target_id",
                    models.IntegerField(
                        help_text="ID des Ziels", verbose_name="ID des Ziels"
                    ),
                ),
                (
                    "start_date",
                    models.DateField(
                        blank=True,
                        help_text="Beginn der Beziehung (YYYY-MM-DD)",
                        null=True,
                        verbose_name="Beginn der Beziehung",
                    ),
                ),
                (
                    "end_date",
                    models.DateField(
                        blank=True,
                        help_text="Ende der Beziehung (YYYY-MM-DD)",
                        null=True,
                        verbose_name="Ende der Beziehung",
                    ),
                ),
            ],
            options={
                "verbose_name": ("Kante",),
                "verbose_name_plural": "Kanten",
                "ordering": ["-id"],
            },
        ),
    ]
