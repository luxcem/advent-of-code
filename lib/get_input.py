import requests


def get_input(year: int, day: int, puzzle: int) -> str:
    url = f"https://adventofcode.com/{year}/day/{day}/input"
    with open("session.txt") as f:
        session = f.read().strip()
    cookies = {"session": session}
    response = requests.get(url, cookies=cookies)
    return response.text.strip()
