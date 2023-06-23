import subprocess

import dotenv

from constants import TO_EMAIL
from email_sender import send_email
from utils.env_handler import get_env_var

# Load environment variables
dotenv.load_dotenv()

# Call the first script
subprocess.call(["python", "web_scrape.py"])

# Call the second script
subprocess.call(["python", "lcbo_ratings.py"])

send_email(
    get_env_var(TO_EMAIL),
    "Best value beers - 595 Bay LCBO",
    text_file="LCBO_store_inventory.txt",
)
