import math
import os
from datetime import datetime
from time import sleep
from zoneinfo import ZoneInfo

from django.conf import settings
from django.core.management.base import BaseCommand
from tqdm import tqdm

from apis_core.apis_metainfo.models import TempEntityClass, Uri
from dumper.utils import chunks, get_wikipedia_urls, write_report


class Command(BaseCommand):
    help = "mint Wikipedia links IDs for GND-URIs"

    def handle(self, *args, **kwargs):
        tz = ZoneInfo("Europe/Vienna")
        start_time = datetime.now(tz=tz).strftime(settings.PMB_TIME_PATTERN)

        ents = (
            TempEntityClass.objects.filter(uri__domain="wikidata").exclude(
                uri__uri__icontains="wikipedia"
            )
            # .exclude(collection=col)
        )
        uris_to_process = Uri.objects.filter(entity__in=ents).filter(domain="wikidata")

        print(
            f"All in all {uris_to_process.count()} WIKIDATA-Entities without Wikipedia"
        )
        ents = TempEntityClass.objects.filter(uri__domain="wikidata").exclude(
            uri__uri__icontains="wikipedia"
        )
        uris_to_process = Uri.objects.filter(entity__in=ents).filter(domain="wikidata")
        wikidata_ids = [x.uri.split("/")[-1] for x in uris_to_process]
        all_results = {}
        total = math.ceil(len(wikidata_ids) / 500)
        for batch in tqdm(chunks(wikidata_ids, 500), total=total):
            all_results.update(get_wikipedia_urls(batch))
            sleep(5)

        entities = [x.entity for x in uris_to_process]
        ent_uri_list = list(zip(entities, all_results.items()))
        filtered_ent_uri_list = [x for x in ent_uri_list if x[1][1]]
        print(
            f"found {len(filtered_ent_uri_list)} wikipedia URLs for {len(ent_uri_list)} entities with wikidata IDS"
        )
        for x in tqdm(filtered_ent_uri_list, total=len(filtered_ent_uri_list)):
            Uri.objects.get_or_create(uri=x[1][1], domain="wikipedia", entity=x[0])

        end_time = datetime.now(tz=tz).strftime(settings.PMB_TIME_PATTERN)
        report = [os.path.basename(__file__), start_time, end_time]
        write_report(report)
