# CO2-api-consumer

CO2 api consumer

## Installation

créer et entrer dans un env virtuel

`mkvirtualenv <env>`

`virtualenv <env>`

installer les dépendances

`pip install -r requirements.txt`

migrer la base

`cd co2_api_consumer`

`./manage.py migrate`

## Commandes

lancer la recupération de données de l'api

`./manage.py retrieve`

lancer la compilation des fréquences

`./manage.py fill_frequency`
