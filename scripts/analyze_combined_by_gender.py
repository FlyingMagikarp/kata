from pathlib import Path
import pandas as pd

from src.analysis import summarize_kata_usage

PARSED_DIR = Path("../data/parsed")
ANALYSIS_DIR = Path("../data/analysis")


def infer_gender_from_file(file: Path) -> str:
    """
    Adjust this if your filenames differ.

    Expected examples:
    - kata_male.csv
    - kata_female.csv
    - male_individual_kata.csv
    - female_individual_kata.csv
    """
    stem = file.stem.lower()

    if "female" in stem or "women" in stem:
        return "female"

    if "male" in stem or "men" in stem:
        return "male"

    raise ValueError(f"Could not infer gender from filename: {file}")


def load_all_parsed() -> pd.DataFrame:
    files = sorted(PARSED_DIR.glob("**/*.csv"))

    if not files:
        raise FileNotFoundError(f"No parsed CSV files found under {PARSED_DIR}")

    dfs = []

    for file in files:
        df = pd.read_csv(file)

        relative_path = file.relative_to(PARSED_DIR)

        df["tournament_id"] = relative_path.parts[0]
        df["category"] = file.stem
        df["gender"] = infer_gender_from_file(file)
        df["source_file"] = str(relative_path)

        dfs.append(df)

    return pd.concat(dfs, ignore_index=True)


def main():
    df = load_all_parsed()

    out_dir = ANALYSIS_DIR / "combined"
    out_dir.mkdir(parents=True, exist_ok=True)

    for gender, gender_df in df.groupby("gender"):
        print(f"Analyze combined gender: {gender}")

        summary = summarize_kata_usage(gender_df)

        summary.insert(0, "gender", gender)
        summary.insert(1, "tournaments", gender_df["tournament_id"].nunique())
        summary.insert(2, "total_rows", len(gender_df))

        out_file = out_dir / f"all_kata_{gender}.csv"
        summary.to_csv(out_file, index=False)

        print(f"Saved: {out_file}")

    print("Done.")


if __name__ == "__main__":
    main()