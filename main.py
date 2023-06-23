import subprocess
from email_sender import send_email
import dotenv
import os
from utils.env_handler import get_env_var
from constants import TO_EMAIL

# Load environment variables
dotenv.load_dotenv()

# Call the first script
subprocess.call(["python", "web_scrape.py"])

# Call the second script
subprocess.call(["python", "lcbo_ratings.py"])

send_email(
    get_env_var(TO_EMAIL),
    "Best value beers - 595 Bay LCBO",
    None,
    None,
    "LCBO_store_inventory.txt",
)
