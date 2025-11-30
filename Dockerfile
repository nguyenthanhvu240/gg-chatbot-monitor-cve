FROM python:3.11-alpine

# Set working directory
WORKDIR /app

# Install cron & curl
RUN apk add --no-cache curl bash

# Copy script
COPY cve_monitor.py .

# Install Python dependencies
RUN pip install --no-cache-dir requests

# Add cron job (runs every day at 10:00)
RUN echo "0 10 * * * python3 /app/cve_monitor.py >> /var/log/cve_monitor.log 2>&1" \
    > /etc/crontabs/root

# Run cron in foreground
CMD ["crond", "-f"]
