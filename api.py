import os


def get_headers():
    return {
        "x-rapidapi-host": "v3.football.api-sports.io",
        "x-rapidapi-key": os.environ.get("API_KEY"),
    }
