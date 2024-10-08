import re
from collections import OrderedDict

from rest_framework import renderers


class NetJsonRenderer(renderers.JSONRenderer):
    media_type = "application/json"
    format = "json+net"

    def render(self, data, media_type=None, renderer_context=None):
        try:
            test = re.search(r"/relations/([^/]+)/", data["results"][0]["url"])
        except IndexError:
            return super().render(
                data, accepted_media_type=media_type, renderer_context=renderer_context
            )
        if test:
            rel = test.group(1)
            for r in data["results"][0].keys():
                if r.startswith("related_"):
                    r2 = r.split("_")[1]
                    rel2 = re.match("^{}[a-z]*".format(r2), rel)
                    if rel2:
                        source = r
                    elif r.endswith("a"):
                        source = r
                    elif r.endswith("b"):
                        target = r
                    rel2 = re.match("^[a-z]*?{}$".format(r2), rel)
                    if rel2:
                        target = r
            results2 = []
            for d in data["results"]:
                d2 = OrderedDict(
                    [
                        (
                            ("target", v)
                            if k == target
                            else ("source", v) if k == source else (k, v)
                        )
                        for k, v in d.items()
                    ]
                )
                if (
                    d2["source"] is None or d2["target"] is None
                ):  # fix needed to not get 500s if relations without source or target exist in the data
                    continue
                target_type = d2["target"]["url"].split("/")[-3].title()
                source_type = d2["source"]["url"].split("/")[-3].title()
                d2["target"]["type"] = target_type
                d2["source"]["type"] = source_type
                results2.append(d2)
            data["results"] = results2
            res3 = super().render(
                data, accepted_media_type=media_type, renderer_context=renderer_context
            )
            return res3
