# pokedex
A Pokemon management app

## How to use
### View a list of Pokedex Creatures

    GET /pokedex/
### Retrieve a specific Pokedex creature
    GET /pokedex/{id}/

### View a list of Pokemons (login required)
    GET /pokemon/

### Create a Pokemon (login required)
    POST /pokemon/

### Update a Pokemon (login required)
    PATCH /pokemon/{id}/
    PUT /pokemon/{id}/

### Delete a Pokemon (login required)
    DELETE /pokemon/{id}/
### Give XP to a pokemon (login required)
    POST /pokemon/{id}/give-xp/


## Commands

### Import Pokemon csv
    docker-compose run  app sh -c "python manage.py import_csv <path/to/file>"
### Run Docker container

    docker-compose up
### Run test

    docker-compose run --rm  app sh -c "pytest"

### Rebuild docker image
    docker build .
### Rebuild docker services

    docker-compose build
