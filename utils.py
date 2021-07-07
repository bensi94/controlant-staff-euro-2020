from typing import Dict, Union, List

from api import get_group_standings


QUARTER_FINAL_QUALIFIERS = (
    "Belgium",
    "Italy",
    "Czech Republic",
    "Denmark",
    "Switzerland",
    "Spain",
    "England",
    "Ukraine",
)

SEMI_FINAL_QUALIFIERS = (
    "Spain",
    "Italy",
    "England",
    "Denmark"
)

FINAL_QUALIFIERS = (
    "Italy",
)


def format_table_data(
    data: Dict[str, Dict[str, Union[str, List]]]
) -> List[Dict[str, str]]:
    return sorted(
        [
            {
                **{"Name": key},
                **{
                    inner_key: (
                        ", ".join(inner_value)
                        if isinstance(inner_value, list)
                        else inner_value
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
    second_key = "Second place in group"
    quarter_key = "Quarter final qualifiers"
    semi_key = "Semi finals qualifiers"
    final_key = "Finals qualifiers"

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

    quarter_points = sum(
        10 for team in chosen_teams[quarter_key] if team in QUARTER_FINAL_QUALIFIERS
    )

    semi_points = sum(
        12 for team in chosen_teams[semi_key] if team in SEMI_FINAL_QUALIFIERS
    )

    final_points = sum(
        16 for team in chosen_teams[final_key] if team in FINAL_QUALIFIERS
    )

    return {
        "Group points": group_points,
        "Quarter final points": quarter_points,
        "Semi finals qualifiers": semi_points,
        "Finals qualifiers points": final_points,
        "Total points": sum((group_points, quarter_points, semi_points, final_points)),
    }


def get_points_table(data: Dict[str, Dict[str, Union[str, List]]]):
    group_standings = get_group_standings()

    table_list = sorted(
        [
            {**{"Position": 0, "Name": key}, **_get_points(group_standings, value)}
            for key, value in data.items()
        ],
        key=lambda k: k["Total points"],
        reverse=True,
    )

    current_position = 1
    current_score = 0

    for player_number, player in enumerate(table_list, start=1):
        if player["Total points"] != current_score:
            current_position = player_number
            current_score = player["Total points"]

        player["Position"] = current_position

    return table_list
