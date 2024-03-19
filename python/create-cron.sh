python main.py

mv /python/main-cron /etc/cron.d/main-cron
chmod 0644 /etc/cron.d/main-cron
crontab /etc/cron.d/main-cron
touch /var/log/cron.log

printenv >> /etc/environment

# Start cron service and follow the log for debugging
cron && tail -f /var/log/cron.log