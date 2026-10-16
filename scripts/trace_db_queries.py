"""A simple script to intercept and print DB queries behind a view GET.

Use the following command to run it the project root:

```sh
uv run ./manage.py shell < ./scripts/trace_db_queries.py
```

NOTE: The view URL is hard-coded to `index` currently.
"""

from django.db import connection
from django.urls import reverse
from django.test.utils import CaptureQueriesContext
from django.test import Client
from django.conf import settings


settings.ALLOWED_HOSTS.append('*')

client = Client()

# GET '/products/?q=&tags=7&tags=8&tags=2'
data = {
    'q': '',
    'tags': [7, 8, 2]
}

# Use the context manager to intercept queries in an active DB connection
with CaptureQueriesContext(connection) as db:
    response = client.get(reverse('index'), data=data)

queries_executed = len(db.captured_queries)
print(f'Total queries executed: {queries_executed}')

for query in db.captured_queries:
    raw_sql = query['sql']
    print(raw_sql)
