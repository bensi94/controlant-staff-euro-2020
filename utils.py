from typing import Dict, Union, List

from api import get_group_standings


def format_table_data(data: Dict[str, Dict[str, Union[str, List]]]) -> List[Dict[str, str]]:
    return sorted(
        [
            {
                **{"Name": key},
                **{
                    inner_key: (
                        ", ".join(inner_value) if isinstance(inner_value, list) else inner_value
                    )
                    for inner_key, inner_value in value.items()
                },
            }
            for key, value in data.items()
        ],
        key=lambda k: k["Name"],
    )


def _get_points(standings, chosen_teams) -> Dict[str, int]:
    first_key = "First place in group"
    second_key = "First place in group"

    group_points = 0

    for team in chosen_teams[first_key]:
        if team in standings[first_key]:
            group_points += 8
        elif team in standings[second_key]:
            group_points += 5

    for team in chosen_teams[second_key]:
        if team in standings[second_key]:
            group_points += 8
        elif team in standings[first_key]:
            group_points += 5

    return {"Group points": group_points, "Total points": sum([group_points])}


def get_points_table(data: Dict[str, Dict[str, Union[str, List]]]):
    group_standings = get_group_standings()

    return sorted(
        [{**{"Name": key}, **_get_points(group_standings, value)} for key, value in data.items()],
        key=lambda k: k["Total points"],
        reverse=True,
    )
