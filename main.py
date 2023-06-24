import dotenv

from constants import TO_EMAIL
from email_sender import send_email
from lcbo_ratings import lcbo_ratings
from utils.env_handler import get_env_var
from web_scrape import web_scrape_lcbo_store_inventory


def run_all_processes():
    # Load environment variables
    dotenv.load_dotenv()

    # Run web scraping
    web_scrape_lcbo_store_inventory()

    # Process and rate the beers
    lcbo_ratings()


if __name__ == "__main__":
    run_all_processes()
