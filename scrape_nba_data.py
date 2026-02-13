"""
NBA Data Collection Script
==========================
Uses the nba_api package to pull game logs, advanced stats, and injury/inactive
player data for the 2023-24 and 2024-25 NBA seasons.

This fills in the gap in the existing Game Data (which ends June 2023).

Output files (saved to Data/Game Data/):
  - game_2024_2025.csv          : Basic box score stats per team per game
  - game_advanced_2024_2025.csv : Advanced stats (pace, ORtg, DRtg) per team per game
  - inactive_2024_2025.csv      : Inactive/DNP players per game

Usage:
  python scrape_nba_data.py
"""

import pandas as pd
import numpy as np
from nba_api.stats.endpoints import (
    teamgamelogs,
    leaguegamefinder,
    boxscoretraditionalv3,
)
from nba_api.stats.static import teams
import time
import os
import sys

OUTPUT_DIR = "Data/Game Data"
SEASONS = ['2023-24', '2024-25']
RATE_LIMIT_SECONDS = 0.7  # NBA API rate limit: ~1 request/sec


def collect_basic_game_logs(seasons):
    """
    Collect basic box score stats for all teams across specified seasons.
    Uses TeamGameLogs endpoint (single call per season for all teams).
    """
    all_data = []

    for season in seasons:
        print(f"  Fetching basic game logs for {season}...")
        time.sleep(RATE_LIMIT_SECONDS)

        logs = teamgamelogs.TeamGameLogs(
            season_nullable=season,
            season_type_nullable='Regular Season',
        )
        df = logs.get_data_frames()[0]

        # Drop rank columns to keep it clean
        rank_cols = [c for c in df.columns if c.endswith('_RANK')]
        df = df.drop(columns=rank_cols + ['AVAILABLE_FLAG'], errors='ignore')

        all_data.append(df)
        print(f"    Got {len(df)} team-game rows ({df['GAME_ID'].nunique()} games)")

    combined = pd.concat(all_data, ignore_index=True)
    print(f"  Total basic: {len(combined)} rows, {combined['GAME_ID'].nunique()} unique games")
    return combined


def collect_advanced_game_logs(seasons):
    """
    Collect advanced stats (pace, ORtg, DRtg, etc.) for all teams.
    Uses TeamGameLogs with Advanced measure type.
    """
    all_data = []

    for season in seasons:
        print(f"  Fetching advanced game logs for {season}...")
        time.sleep(RATE_LIMIT_SECONDS)

        logs = teamgamelogs.TeamGameLogs(
            season_nullable=season,
            season_type_nullable='Regular Season',
            measure_type_player_game_logs_nullable='Advanced',
        )
        df = logs.get_data_frames()[0]

        # Drop rank columns
        rank_cols = [c for c in df.columns if c.endswith('_RANK')]
        df = df.drop(columns=rank_cols + ['AVAILABLE_FLAG'], errors='ignore')

        all_data.append(df)
        print(f"    Got {len(df)} team-game rows")

    combined = pd.concat(all_data, ignore_index=True)
    print(f"  Total advanced: {len(combined)} rows")
    return combined


def collect_inactive_players(game_ids, batch_size=50):
    """
    Collect inactive/DNP player data from individual box scores.

    This is the slowest part because we need one API call per game.
    We extract players with empty minutes or DNP comments.
    """
    all_inactive = []
    total = len(game_ids)
    errors = []

    for i, game_id in enumerate(game_ids):
        if (i + 1) % 50 == 0 or i == 0:
            print(f"    Processing game {i+1}/{total} ({game_id})...")

        time.sleep(RATE_LIMIT_SECONDS)

        try:
            trad = boxscoretraditionalv3.BoxScoreTraditionalV3(game_id=game_id)
            players = trad.get_data_frames()[0]

            # Find inactive players: empty minutes string or DNP comment
            inactive_mask = (
                (players['minutes'] == '') |
                (players['minutes'].isna()) |
                (players['comment'].str.contains('DNP|DND|NWT|Inactive', case=False, na=False))
            )

            if inactive_mask.any():
                inactive = players[inactive_mask][
                    ['gameId', 'personId', 'firstName', 'familyName',
                     'teamTricode', 'teamId', 'comment']
                ].copy()
                inactive.columns = [
                    'GAME_ID', 'PLAYER_ID', 'FIRST_NAME', 'LAST_NAME',
                    'TEAM_ABBREVIATION', 'TEAM_ID', 'COMMENT'
                ]
                all_inactive.append(inactive)

        except Exception as e:
            errors.append((game_id, str(e)))
            if len(errors) <= 5:
                print(f"    Warning: Error for game {game_id}: {e}")

    if errors:
        print(f"    {len(errors)} errors out of {total} games")

    if all_inactive:
        combined = pd.concat(all_inactive, ignore_index=True)
        print(f"  Total inactive records: {len(combined)} across {combined['GAME_ID'].nunique()} games")
        return combined
    else:
        print("  No inactive players found (unlikely - check for errors)")
        return pd.DataFrame()


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    print("=" * 60)
    print("NBA DATA COLLECTION")
    print(f"Seasons: {SEASONS}")
    print("=" * 60)

    # Step 1: Basic game logs
    print("\n[1/3] Collecting basic game logs...")
    basic_df = collect_basic_game_logs(SEASONS)
    basic_path = os.path.join(OUTPUT_DIR, "game_2024_2025.csv")
    basic_df.to_csv(basic_path, index=False)
    print(f"  Saved to {basic_path}")

    # Step 2: Advanced game logs
    print("\n[2/3] Collecting advanced game logs...")
    advanced_df = collect_advanced_game_logs(SEASONS)
    advanced_path = os.path.join(OUTPUT_DIR, "game_advanced_2024_2025.csv")
    advanced_df.to_csv(advanced_path, index=False)
    print(f"  Saved to {advanced_path}")

    # Step 3: Inactive players (this takes a while - ~1 sec per game)
    print("\n[3/3] Collecting inactive/DNP players...")
    # Get unique game IDs from basic logs
    game_ids = sorted(basic_df['GAME_ID'].unique())
    print(f"  Need to query {len(game_ids)} individual box scores")

    # Check if we have a partial file from a previous run
    inactive_path = os.path.join(OUTPUT_DIR, "inactive_2024_2025.csv")
    if os.path.exists(inactive_path):
        existing = pd.read_csv(inactive_path, dtype={'GAME_ID': str})
        existing_ids = set(existing['GAME_ID'].unique())
        remaining_ids = [gid for gid in game_ids if gid not in existing_ids]
        print(f"  Found existing file with {len(existing_ids)} games, {len(remaining_ids)} remaining")

        if remaining_ids:
            new_inactive = collect_inactive_players(remaining_ids)
            if len(new_inactive) > 0:
                inactive_df = pd.concat([existing, new_inactive], ignore_index=True)
            else:
                inactive_df = existing
        else:
            print("  All games already collected!")
            inactive_df = existing
    else:
        inactive_df = collect_inactive_players(game_ids)

    inactive_df.to_csv(inactive_path, index=False)
    print(f"  Saved to {inactive_path}")

    # Summary
    print("\n" + "=" * 60)
    print("COLLECTION COMPLETE")
    print("=" * 60)
    print(f"  Basic game logs:    {len(basic_df):,} rows -> {basic_path}")
    print(f"  Advanced game logs: {len(advanced_df):,} rows -> {advanced_path}")
    print(f"  Inactive players:   {len(inactive_df):,} rows -> {inactive_path}")
    print(f"\n  Unique games: {basic_df['GAME_ID'].nunique():,}")
    print(f"  Seasons: {basic_df['SEASON_YEAR'].unique()}")


if __name__ == '__main__':
    main()
