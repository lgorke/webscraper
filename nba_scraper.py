#!/usr/bin/env python3

import requests
import time
from concurrent.futures import ThreadPoolExecutor


# ESPN NBA standings API
URL = "https://site.api.espn.com/apis/v2/sports/basketball/nba/standings"

def fetch_season(season):
    """Retrieve NBA standings data for one season."""

    response = requests.get(URL,params={"season": season},timeout=15)
    response.raise_for_status()
    return season, response.json()

# Seasons are identified by the year they end (ex. 2027 represents the 2026-27 season)
def get_seasons():
    """Ask the user which NBA seasons to retrieve."""

    print("NBA Standings Scraper")
    print("Enter season-ending years (e.g., 2027 for 2026-27).")
    print("Separate multiple seasons with commas.")

    user_input = input("Enter seasons: ")
    seasons = list(map(int, user_input.split(",")))

    return seasons

def extract_standings(result):
    """Extract team standings from an ESPN API response."""

    season, data = result
    standings = []

    for conference in data.get("children", []):
        entries = conference.get("standings", {}).get("entries", [])

        for rank, entry in enumerate(entries, start=1):
            team = entry.get("team", {})

            stats = {stat["name"]: stat.get("displayValue", stat.get("value", "")) for stat in entry.get("stats", [])}

            standings.append({
                "season": season,
                "conference": conference.get("name", "Unknown"),
                "rank": rank,
                "team": team.get("displayName", "Unknown"),
                "abbreviation": team.get("abbreviation", ""),
                "wins": stats.get("wins", "N/A"),
                "losses": stats.get("losses", "N/A"),
                "win_percentage": stats.get("winPercent", "N/A"),
                "games_behind": stats.get("gamesBehind", "N/A"),
            })

    return standings


def scrape_sequential():
    """Fetch standings one season at a time."""

    results = list(map(fetch_season, SEASONS))
    return list(map(extract_standings, results))

def scrape_concurrent():
    """Fetch standings for multiple seasons simultaneously."""

    with ThreadPoolExecutor(max_workers=4) as executor:
        results = list(executor.map(fetch_season, SEASONS))
    return list(map(extract_standings, results))


def print_standings(all_standings):
    """Print NBA standings in the terminal."""

    for season_standings in all_standings:
        if not season_standings:
            continue

        season = season_standings[0]["season"]

        print("\n" + "=" * 23)
        print(f"NBA STANDINGS - {season - 1}-{str(season)[-2:]}")
        print("=" * 23)

        conferences = {conference for conference in map(lambda team: team["conference"], season_standings)}

        for conference in sorted(conferences):
            print(f"\n{conference.upper()}")
            print("-" * 18)

            print(
                f"{'Rank':<6}{'Team':<25}{'W':<8}"
                f"{'L':<8}{'Win %':<12}{'GB':<8}"
            )

            teams = list(filter(lambda team: team["conference"] == conference, season_standings))

            for team in teams:
                print(
                    f"{team['rank']:<6}"
                    f"{team['team']:<25}"
                    f"{team['wins']:<8}"
                    f"{team['losses']:<8}"
                    f"{team['win_percentage']:<12}"
                    f"{team['games_behind']:<8}"
                )

def main():
    """Compare sequential and concurrent scraping performance."""

    seasons = get_seasons()

    print("\nStarting sequential scraping...")

    start = time.perf_counter()
    sequential_results = list(map(fetch_season, seasons))
    sequential_results = list(map(extract_standings, sequential_results))
    sequential_time = time.perf_counter() - start

    print(f"Sequential time: {sequential_time:.2f} seconds")

    print("\nStarting concurrent scraping...")

    start = time.perf_counter()

    with ThreadPoolExecutor(max_workers=min(4, len(seasons))) as executor:
        concurrent_results = list(
            map(extract_standings, executor.map(fetch_season, seasons))
        )

    concurrent_time = time.perf_counter() - start

    print(f"Concurrent time: {concurrent_time:.2f} seconds")

    if concurrent_time > 0:
        speedup = sequential_time / concurrent_time
        print(f"Speedup: {speedup:.2f}x")

    print("\nDisplaying NBA standings:")
    print_standings(concurrent_results)

if __name__ == "__main__":
    main()
