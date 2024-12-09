# Generated by Django 5.1.3 on 2024-12-09 12:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("network", "0002_alter_edge_options_alter_edge_source_kind_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="edge",
            name="source_lat",
            field=models.FloatField(blank=True, null=True, verbose_name="Breitengrad"),
        ),
        migrations.AddField(
            model_name="edge",
            name="source_lng",
            field=models.FloatField(blank=True, null=True, verbose_name="Längengrad"),
        ),
        migrations.AddField(
            model_name="edge",
            name="target_lat",
            field=models.FloatField(blank=True, null=True, verbose_name="Breitengrad"),
        ),
        migrations.AddField(
            model_name="edge",
            name="target_lng",
            field=models.FloatField(blank=True, null=True, verbose_name="Längengrad"),
        ),
    ]