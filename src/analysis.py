import pandas as pd


def summarize_kata_usage(df: pd.DataFrame, group_cols: list[str] | None = None) -> pd.DataFrame:
    """
    Summarize kata usage and win rate.

    Required columns:
    - kata_name
    - winner
    - player_id

    group_cols lets you separate by category/gender/tournament/etc.
    """
    if group_cols is None:
        group_cols = []

    required_cols = {"kata_name", "winner", "player_id"}
    missing_cols = required_cols - set(df.columns)

    if missing_cols:
        raise ValueError(f"Missing required columns: {missing_cols}")

    grouping = group_cols + ["kata_name"]

    summary = (
        df.groupby(grouping)
        .agg(
            performances=("kata_name", "size"),
            wins=("winner", "sum"),
            unique_athletes=("player_id", "nunique"),
        )
        .reset_index()
    )

    if group_cols:
        summary["total_performances"] = (
            summary.groupby(group_cols)["performances"].transform("sum")
        )
    else:
        summary["total_performances"] = summary["performances"].sum()

    summary["usage_pct"] = (
        summary["performances"] / summary["total_performances"] * 100
    )

    summary["win_rate"] = summary["wins"] / summary["performances"] * 100

    prior_games = 20

    global_win_rate = summary["wins"].sum() / summary["performances"].sum()
    prior_wins = global_win_rate * prior_games

    summary["adjusted_win_rate"] = (
            (summary["wins"] + prior_wins)
            / (summary["performances"] + prior_games)
            * 100
    )

    return summary.sort_values(
        group_cols + ["performances", "win_rate"],
        ascending=[True] * len(group_cols) + [False, False],
    )