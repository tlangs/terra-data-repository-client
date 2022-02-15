ENVIRONMENTS = {
    'localhost': 'http://localhost:8080',
    'dev': 'https://jade.datarepo-dev.broadinstitute.org',
    'prod': 'https://data.terra.bio'
}


SORT_FIELDS = ["name", "description", "created_date"]
SORT_DIRECTIONS = ["asc", "desc"]

RETRIEVE_DATASETS_INCLUDES = ["NONE", "SCHEMA", "ACCESS_INFORMATION", "PROFILE", "DATA_PROJECT", "STORAGE"]
