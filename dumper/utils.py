from io import BytesIO

import pandas as pd
import requests
from AcdhArcheAssets.uri_norm_rules import get_normalized_uri
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from tqdm import tqdm

from apis_core.apis_metainfo.models import Uri

PMB_ENTITIES = "pmb_entities"


def chunks(iterable, size):
    for i in range(0, len(iterable), size):
        yield iterable[i : i + size]


def get_wikipedia_urls(wikidata_ids):
    values = " ".join(f"wd:{qid}" for qid in wikidata_ids)
    WIKIDATA_ENDPOINT = "https://query.wikidata.org/sparql"

    query = f"""
    PREFIX wd: <http://www.wikidata.org/entity/>
    PREFIX schema: <http://schema.org/>

    SELECT ?item ?article ?language WHERE {{
        VALUES ?item {{ {values} }}

        ?article schema:about ?item ;
                 schema:inLanguage ?language ;
                 schema:isPartOf <https://en.wikipedia.org/> .
    }}
    """

    response = requests.post(
        WIKIDATA_ENDPOINT,
        data={
            "query": query,
            "format": "json",
        },
        headers={
            "Accept": "application/sparql-results+json",
            "User-Agent": "my-wikidata-script/1.0 (your-email@example.com)",
        },
        timeout=120,
    )

    response.raise_for_status()

    results = response.json()["results"]["bindings"]

    # Collect all Wikipedia articles per Wikidata ID
    articles = {}

    for result in results:
        qid = result["item"]["value"].rsplit("/", 1)[-1]
        url = result["article"]["value"]
        language = result["language"]["value"]

        articles.setdefault(qid, {})[language] = url

    # Select de > en > any
    output = {}

    for qid in wikidata_ids:
        available = articles.get(qid, {})

        if "de" in available:
            output[qid] = available["de"]
        elif "en" in available:
            output[qid] = available["en"]
        elif available:
            output[qid] = next(iter(available.values()))
        else:
            output[qid] = None

    return output


def write_report(report, report_file=settings.PMB_LOG_FILE):  # pragma: no cover
    with open(report_file, "a") as f:
        f.write(f"{','.join(report)}\n")
        return "done"


def process_beacon(beacon_url, domain):
    """takes an URL to a beacon.txt file and a string to populate an APIS-URL domain field"""
    r = requests.get(beacon_url)
    lines = r.content.decode("utf-8").split("\n")
    created = 0
    for x in tqdm(lines, total=len(lines)):
        if "|" in x and not x.startswith("#"):
            gnd, beacon_uri = get_normalized_uri(x.split("|")[0]), x.split("|")[-1]
            try:
                item = Uri.objects.get(uri=gnd)
            except ObjectDoesNotExist:
                continue
            entity = item.entity
            try:
                Uri.objects.get(uri=beacon_uri)
                continue
            except ObjectDoesNotExist:
                new_uri = Uri.objects.create(uri=beacon_uri, entity=entity)
                new_uri.domain = domain
                new_uri.save()
                created += 1
    return created


def gsheet_to_df(sheet_id):
    GDRIVE_BASE_URL = "https://docs.google.com/spreadsheet/ccc?key="
    url = f"{GDRIVE_BASE_URL}{sheet_id}&output=csv"
    r = requests.get(url)
    print(r.status_code)
    data = r.content
    df = pd.read_csv(BytesIO(data))
    return df
