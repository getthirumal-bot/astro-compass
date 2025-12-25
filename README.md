cd C:\Users\itadmin\astro-app

# Initialize git
git init

# Add remote
git remote add origin https://github.com/getthirumal-bot/astro-compass.git

# Pull the README that GitHub created
git pull origin main --allow-unrelated-histories

# Add all your files
git add .

# Commit
git commit -m "Add Astro Consensus Compass app"

# Push
git push -u origin main
