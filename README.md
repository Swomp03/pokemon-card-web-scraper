# Pokemon-Card-Web-Scraper-Python

This is the Python Web Scraper for the Pokémon Card Web Scraper Project.

## Technology Used
- Python
- bs4
- SQL
- Postgres
- Google Translate

## Notes
- Make sure to add a .env for your Postgres DB connection string

## Postgres DB | Create a DB called PKMNCards & add 9 tables:
- all_sets
  - set_code (text)
  - image_location (text) [for the front-end button image]
  - set_release_date (date)

- cardrush_cards
  - card_name (text)
  - price (numeric with length/precision = 10 & scale = 2)
  - stock (integer)
  - link (text)
  - card_number (text)
  - card_set (text)
  - last_updated (timestamp with time zone)
 
- cardrush_sites
  - link (text)
  - set (text)
  - set_amount (integer)
  - set_release_date (date)
 
- hareruya_cards & toreca_camp_cards
  - Same as cardrush_cards
 
- hareruya_sites & toreca_camp_sites
  - Same as cardrush_sites

- price_charting_cards
  - card_name (text)
  - price (numeric with length/precision = 10 & scale = 2)
  - link (text)
  - image_link (text)
  - card_number (text)
  - card_set (text)
  - set_amount (text)
  - last_updated (timestamp with time zone)

- price_charting_sites
  - link (text)
  - card_set (text)
  - set_amount (integer)
  - set_release_date (date)
