
chmod +x /python/main.py

mv /python/run-scraper /etc/cron.d/run-scraper
chmod 0644 /etc/cron.d/run-scraper
crontab /etc/cron.d/run-scraper

printenv >> /etc/environment

# Start cron service and follow the log for debugging
cron && tail -f /var/log/cron.log