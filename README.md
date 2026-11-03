# api-lab
6787084_W10-API_Lab_Exercise

## How to install and run

1. Create and activate a virtual environment:
   - Windows PowerShell: `python -m venv .venv` then `.venv\Scripts\activate`
   - macOS and Linux: `python3 -m venv .venv` then `source .venv/bin/activate`
2. Install the packages: `pip install -r requirements.txt`
3. Run all tests: `pytest -v`
4. Save an HTML report of a full run: `pytest -v --html=report.html --self-contained-html`

## Input domain model: POST /api/ratings

| Characteristic | Block | Value in the test | Test |
| -------------- | ----- | ----------------- | ---- |
| C1 Value of stars | 1 to 5 (base) | 3 | test_base_choice_is_saved |
| C1 Value of stars | below 1 | 0 | test_stars_out_of_range[0] |
| C1 Value of stars | above 5 | 6 | test_stars_out_of_range[6] |
| C2 Type of stars | whole number (base) | 3 | test_base_choice_is_saved |
| C2 Type of stars | decimal | 3.5 | test_stars_decimal |
| C2 Type of stars | text | "3" | test_stars_text |
| C2 Type of stars | missing | no field | test_stars_missing |
| C3 Pizza | exists (base) | a new pizza | test_base_choice_is_saved |
| C3 Pizza | does not exist | 999999999 | test_pizza_does_not_exist |
| C4 Token | the user's own (base) | from auth | test_base_choice_is_saved |
| C4 Token | none | no header | test_no_token |
| C4 Token | wrong length | token short | test_short_token |