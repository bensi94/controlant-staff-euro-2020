from typing import Dict, Tuple, Any

import requests
import requests_cache


requests_cache.install_cache(expire_after=360)


def get_group_standings() -> dict[str, tuple[Any, ...]]:
    response = requests.get("https://api.urslit.net/leagues/s15733/standings").json()
    standings = list(zip(*[[team["name"] for team in group["standings"]] for group in response]))

    return {"First place in group": standings[0], "Second place in group": standings[1]}
