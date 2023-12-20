#!/bin/bash
fixtures="apis_core/apis_entities/fixtures/db.json"
echo "dumping fixtures into ${fixtures}"
python manage.py dumpdata --natural-primary > ${fixtures}

echo "modify urls"
sed -i 's/acdh.oeaw.ac.at/hansi4ever/g' ${fixtures}

echo "done"