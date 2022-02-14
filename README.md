# pokedex
A Pokemon management app

## How to use

### Get schema.yaml
    schema/

### Swagger like page
    schema/swagger-ui/

### Documentation page
    schema/redoc/


## Commands

### Import Pokemon csv
    docker-compose run  app sh -c "python manage.py import_csv <path/to/file>"
### Run Docker container
    docker-compose up
### Run test
    docker-compose run --rm  app sh -c "pytest -n auto --cov"

### Rebuild docker image
    docker build . --tag pokedex-docker
### Rebuild docker services
    docker-compose build

### Generate DRF spectacular schema
    docker-compose run --rm app sh -c "python manage.py spectacular --file schema.yml"
    docker run -p 80:8080 -e SWAGGER_JSON=/schema.yml -v ${PWD}/schema.yml:/schema.yml swaggerapi/swagger-ui
