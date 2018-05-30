Python 3.6 is not yet supported, but we will support it by the next
release. Make sure you are using Python 3.4 or 3.5.

Install requirements:

```bash
pip install -r requirements.txt
```

Start PostgreSQL, Redis, and Elasticsearch Docker containers:

```bash
docker-compose up
```

Setup project database:

```bash
python manage.py migrate
python manage.py createsuperuser --username admin --email admin@example.com
python manage.py register
python manage.py elastic_index
python manage.py elastic_mapping
```

Run servers (each in a separate terminal window):

```bash
python manage.py runserver # Django development server
python manage.py runlistener # Executor listener server
celery -A resolwe_project worker --queues=ordinary,hipri --loglevel=info # Celery workload manager
```

Optionally if you require reactive feedback over web sockets:

```bash
python manage.py runobservers  # Query observers for reactive UI``
```

To include the Resolwe Bioinformatics extension, add the following:

```python
resolwe_project/settings.py

INSTALLED_APPS = [
    ...
    'resolwe.toolkit',

    'resolwe_bio',
    'resolwe_bio.kb',

    'resolwe_project.base',
    ...
]
```

```python
resolwe_project/urls.py

...
from resolwe.elastic import routers as search_routers
...
api_router.register(r'kb/feature/admin', FeatureViewSet)
api_router.register(r'kb/mapping/admin', MappingViewSet)

search_router = search_routers.SearchRouter(trailing_slash=False)  # pylint: disable=invalid-name
search_router.register(r'kb/feature/search', FeatureSearchViewSet, 'kb_feature_search')
search_router.register(r'kb/feature/autocomplete', FeatureAutocompleteViewSet, 'kb_feature_autocomplete')
search_router.register(r'kb/mapping/search', MappingSearchViewSet, 'kb_mapping_search')

urlpatterns = [
...
url(r'^api/', include(api_router.urls + search_router.urls, namespace='resolwe-api')),
...

```
