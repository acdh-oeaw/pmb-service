from rdflib import Graph, Namespace, URIRef, RDF, Literal
from apis_core.apis_metainfo.models import TempEntityClass
from django.conf import settings


class ArcheMd:
    """simple class to express basic info about an entity in ARCHE-MD schema"""

    def return_graph(self):
        g = Graph()
        subj = URIRef(self.detail_view_url)
        g.add((subj, RDF.type, self.ARCHE[self.arche_class]))
        g.add((subj, self.ARCHE["hasIdentifier"], subj))
        if self.entity_class_name == "person":
            g.add(
                (
                    subj,
                    self.ARCHE["hasTitle"],
                    Literal(
                        f"{self.entity.name}, {self.entity.first_name}", lang="und"
                    ),
                )
            )
        else:
            g.add(
                (
                    subj,
                    self.ARCHE["hasTitle"],
                    Literal(f"{self.entity.name}", lang="und"),
                )
            )
        for x in self.entity_uris:
            g.add((subj, self.ARCHE["hasIdentifier"], URIRef(x)))
        try:
            g.add((subj, self.ARCHE["hasLatitude"], Literal(f"{self.entity.lat}")))
            g.add((subj, self.ARCHE["hasLongitude"], Literal(f"{self.entity.lng}")))
        except AttributeError:
            pass
        return g

    def __init__(self, entity_id):
        self.ARCHE = Namespace("https://vocabs.acdh.oeaw.ac.at/schema#")
        self.entity_id = entity_id
        self.item = TempEntityClass.objects.get(id=entity_id)
        self.entity = self.item.get_child_entity()
        self.entity_class_name = self.entity.__class__.__name__.lower()
        self.detail_view_url = settings.PMB_DETAIL_VIEW_PATTERN.format(
            self.entity_class_name, self.entity_id
        )
        if self.entity_class_name == "institution":
            self.arche_class = "Organization"
        else:
            self.arche_class = self.entity_class_name.capitalize()
        self.entity_uris = [
            x.uri
            for x in self.entity.uri_set.all()
            if "gnd" in x.uri or "geonames" in x.uri or "wikidata" in x.uri
        ]
