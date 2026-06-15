from pathlib import Path

from src.parser import parse_html_file

RAW_DIR = Path("../data/raw")
PARSED_DIR = Path("../data/parsed")


def get_parsed_path(raw_file: Path) -> Path:
    relative_path = raw_file.relative_to(RAW_DIR)
    return PARSED_DIR / relative_path.with_suffix(".csv")


def infer_metadata(raw_file: Path) -> dict:
    relative_path = raw_file.relative_to(RAW_DIR)

    return {
        "tournament_id": relative_path.parts[0],
        "category": raw_file.stem,
        "source_file": str(relative_path),
    }


def parse_if_needed(raw_file: Path) -> bool:
    parsed_file = get_parsed_path(raw_file)

    if parsed_file.exists():
        print(f"Skip: {parsed_file}")
        return False

    print(f"Parse: {raw_file}")

    df = parse_html_file(raw_file)

    metadata = infer_metadata(raw_file)
    for key, value in metadata.items():
        df[key] = value

    parsed_file.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(parsed_file, index=False)

    return True


def main():
    raw_files = sorted(RAW_DIR.glob("**/*.html"))

    parsed = 0
    skipped = 0

    for raw_file in raw_files:
        did_parse = parse_if_needed(raw_file)

        if did_parse:
            parsed += 1
        else:
            skipped += 1

    print(f"Parsed {parsed}, skipped {skipped}.")


if __name__ == '__main__':
    main()
