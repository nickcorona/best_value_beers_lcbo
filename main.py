import subprocess

# Call the first script
subprocess.call(["python", "web_scrape.py"])

# Call the second script
subprocess.call(["python", "lcbo_ratings.py"])
