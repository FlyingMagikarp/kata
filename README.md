File naming pattern
- YYYY-MM_event_cat_location/category.html
- 2026-06_k1_premier_rabat/kata_male.html

## Scripts
- parse_all.py 

parses all files in `data/raw/` that don't have a parsed equivalent in `data/parsed/`

- analyze_tournaments.py
parses all files in `data/parsed/` and generates a summary in `data/analysis/tournaments`

- analyze_combined_by_gender.py
generates a summary in `data/analysis/combined` of all tournaments combined by gender

