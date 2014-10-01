opps-tse
==============

Tribunal Superior Eleitoral API parser for Opps CMS 

[http://www.tse.jus.br/](http://www.tse.jus.br/)

[http://www.tse.jus.br/eleicoes/eleicoes-2014/parceria-divulgacao-resultados-2014](http://www.tse.jus.br/eleicoes/eleicoes-2014/parceria-divulgacao-resultados-2014)


### Install
```
pip install -e git+git@github.com:opps/opps-tse#egg=opps-tse
```

```
INSTALLED_APPS = [
	...
	'opps-tse',
	...
]

```

And run migrations.


### Populate database

In your django shell, do it:

```python
from opps.tse.tasks import populate

# execute
populate()
```

### Settings

```

OPPS_TSE_WEBSERVICE_PATH = '/path/to/2014/divulgacao/simulado/4464/distribuicao/'

OPPS_TSE_CANDIDATES_PHOTOS_DIRECTORY = '/path/to/foto_cand2014_div/'

```
