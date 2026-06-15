from pathlib import Path
import pandas as pd

from src.analysis import summarize_kata_usage

PARSED_DIR = Path("../data/parsed")
ANALYSIS_DIR = Path("../data/analysis")


def get_analysis_path(parsed_file: Path) -> Path:
    """
    Maps:

    data/parsed/2026-06_k1-a-coruna/kata_male.csv

    to:

    data/analysis/tournaments/2026-06_k1-a-coruna/kata_male_summary.csv
    """
    relative_path = parsed_file.relative_to(PARSED_DIR)
    return ANALYSIS_DIR / "tournaments" / relative_path.with_name(
        f"{parsed_file.stem}_summary.csv"
    )


def analyze_file(parsed_file: Path) -> pd.DataFrame:
    df = pd.read_csv(parsed_file)

    relative_path = parsed_file.relative_to(PARSED_DIR)

    tournament_id = relative_path.parts[0]
    category = parsed_file.stem

    summary = summarize_kata_usage(df)

    summary.insert(0, "tournament_id", tournament_id)
    summary.insert(1, "category", category)
    summary.insert(2, "source_file", str(relative_path))

    return summary


def main():
    parsed_files = sorted(PARSED_DIR.glob("**/*.csv"))

    if not parsed_files:
        raise FileNotFoundError(f"No parsed CSV files found under {PARSED_DIR}")

    analyzed = 0

    for parsed_file in parsed_files:
        out_file = get_analysis_path(parsed_file)

        if out_file.exists():
            print(f"Skip existing: {out_file}")
            continue

        print(f"Analyze: {parsed_file} -> {out_file}")

        summary = analyze_file(parsed_file)

        out_file.parent.mkdir(parents=True, exist_ok=True)
        summary.to_csv(out_file, index=False)

        analyzed += 1

    print(f"Done. Analyzed {analyzed} files.")


if __name__ == "__main__":
    main()