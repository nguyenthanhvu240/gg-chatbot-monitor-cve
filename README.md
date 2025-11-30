# 🛡️ CVE Monitor - Daily Security Alerts to Google Chat

[![Python](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/)
[![Docker](https://img.shields.io/badge/docker-ready-blue.svg)](https://www.docker.com/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Shodan](https://img.shields.io/badge/data-Shodan_CVEDB-red.svg)](https://cvedb.shodan.io/)

An automated CVE (Common Vulnerabilities and Exposures) monitoring tool that fetches daily vulnerabilities from [Shodan's CVEDB](https://cvedb.shodan.io/) and posts beautifully formatted alerts to your Google Chat workspace.

Perfect for security teams, DevOps engineers, and anyone who needs to stay updated on the latest security vulnerabilities!

---

## 📋 Table of Contents

- [Features](#-features)
- [What This Tool Does](#-what-this-tool-does)
- [Prerequisites](#-prerequisites)
- [Getting Google Chat Webhook](#-getting-google-chat-webhook)
- [Installation Method 1: Local Script](#-installation-method-1-local-script-simple--quick)
- [Installation Method 2: Docker](#-installation-method-2-docker-recommended-for-production)
- [Configuration & Customization](#%EF%B8%8F-configuration--customization)
- [Usage Examples](#-usage-examples)
- [Troubleshooting](#-troubleshooting)
- [Contributing](#-contributing)

---

## ✨ Features

- 🔄 **Automated Daily Monitoring** - Runs at 10:00 AM UTC every day automatically
- 📅 **Yesterday's CVEs** - Fetches all CVEs published the previous day
- 🎨 **Beautiful Google Chat Cards** - Rich formatted messages with severity indicators
- 🎯 **Severity-Based Color Coding**:
  - 🔴 **CRITICAL** (CVSS 9.0+)
  - 🟠 **HIGH** (CVSS 7.0-8.9)
  - 🟡 **MEDIUM** (CVSS 4.0-6.9)
  - 🟢 **LOW** (CVSS 0-3.9)
  - ⚪ **Not Yet Scored**
- 🔗 **Direct Links** - Quick access to Shodan and NVD for detailed info
- 📊 **Daily Summary Report** - Total CVEs found and posted
- 🔍 **Advanced Filtering** - Filter by CVSS score or keywords (optional)
- 🐳 **Docker Ready** - Easy deployment with Docker or Docker Compose
- ⚡ **Lightweight** - Minimal dependencies, runs on any Python 3.11+ system

---

## 🎯 What This Tool Does

### The Problem
Security teams need to stay informed about new CVEs, but manually checking CVE databases every day is time-consuming and inefficient.

### The Solution
This tool automatically:
1. **Checks** Shodan's CVEDB every day at 10:00 AM UTC
2. **Fetches** all CVEs published yesterday
3. **Formats** them into beautiful, easy-to-read cards
4. **Posts** them to your Google Chat space
5. **Sends** a summary report

### Example Workflow
```
┌─────────────────┐
│  Nov 22, 2025   │  CVEs are published
│  CVEs Published │
└────────┬────────┘
         │
         ▼
┌─────────────────────┐
│  Nov 23, 10:00 AM   │  Script runs automatically
│  Script Executes    │
└────────┬────────────┘
         │
         ▼
┌─────────────────────┐
│  Fetch from Shodan  │  Gets yesterday's CVEs
│  CVEDB API          │
└────────┬────────────┘
         │
         ▼
┌─────────────────────┐
│  Format Cards       │  Creates beautiful cards
│  with CVSS & Links  │
└────────┬────────────┘
         │
         ▼
┌─────────────────────┐
│  Post to Google     │  You get notified!
│  Chat Webhook       │
└─────────────────────┘
```

---

## 📋 Prerequisites

Before you begin, ensure you have one of the following:

### For Method 1 (Local Script):
- **Python 3.11 or higher** installed
- **pip** (Python package manager)
- **cron** (for scheduling on Linux/Mac) or **Task Scheduler** (Windows)
- Internet connection

### For Method 2 (Docker):
- **Docker** installed ([Get Docker](https://docs.docker.com/get-docker/))
- **Docker Compose** (usually comes with Docker Desktop)
- Internet connection

### For Both Methods:
- **Google Chat Workspace** with permissions to create webhooks
- **Webhook URL** from Google Chat (see below)

---

## 🔑 Getting Google Chat Webhook

Before installing, you need a Google Chat webhook URL. Follow these steps:

### Step 1: Open Google Chat
Go to [chat.google.com](https://chat.google.com)

### Step 2: Create or Select a Space
- Create a new space, or
- Use an existing space where you want to receive CVE alerts

### Step 3: Access Webhooks
1. Click on the **space name** at the top
2. Select **Apps & integrations**
3. Click on **Webhooks**

### Step 4: Create Webhook
1. Click **Create webhook**
2. Give it a name: `CVE Monitor` (or any name you prefer)
3. Optionally, add an avatar image
4. Click **Create**

### Step 5: Copy the URL
You'll get a URL that looks like this:
```
https://chat.googleapis.com/v1/spaces/XXXXX/messages?key=YYYYY&token=ZZZZZ
```

**⚠️ Keep this URL private!** Anyone with this URL can post messages to your space.

---

## 🚀 Installation Method 1: Local Script (Simple & Quick)

Perfect for: Quick testing, personal use, single-server deployments

### Step 1: Clone the Repository

```bash
# Clone the repository
git clone https://github.com/nguyenthanhvu240/gg-chatbot-monitor-cve.git

# Navigate to the directory
cd gg-chatbot-monitor-cve
```

### Step 2: Install Python Dependencies

```bash
# Install required packages
pip install requests

# Or if you use pip3
pip3 install requests
```

That's it! Only one dependency needed: `requests`

### Step 3: Configure Your Webhook

You have two options:

#### Option A: Using Environment Variable (Recommended)

```bash
# Set environment variable (Linux/Mac)
export GOOGLE_CHAT_WEBHOOK="YOUR_WEBHOOK_URL_HERE"

# For permanent setup, add to ~/.bashrc or ~/.zshrc
echo 'export GOOGLE_CHAT_WEBHOOK="YOUR_WEBHOOK_URL_HERE"' >> ~/.bashrc
source ~/.bashrc
```

For Windows PowerShell:
```powershell
$env:GOOGLE_CHAT_WEBHOOK="YOUR_WEBHOOK_URL_HERE"

# For permanent setup
[System.Environment]::SetEnvironmentVariable('GOOGLE_CHAT_WEBHOOK','YOUR_WEBHOOK_URL_HERE','User')
```

#### Option B: Edit the Script Directly

Open `cve_monitor.py` and find this line (around line 12):

```python
GOOGLE_CHAT_WEBHOOK = os.environ.get('GOOGLE_CHAT_WEBHOOK', 'YOUR_WEBHOOK_URL_HERE')
```

Replace `YOUR_WEBHOOK_URL_HERE` with your actual webhook URL:

```python
GOOGLE_CHAT_WEBHOOK = os.environ.get('GOOGLE_CHAT_WEBHOOK', 'https://chat.googleapis.com/v1/spaces/...')
```

### Step 4: Test Run

Test the script manually before scheduling:

```bash
python3 cve_monitor.py
```

You should see output like:
```
============================================================
CVE Monitor - Shodan CVEDB
Started at: 2025-11-30 16:00:00
============================================================
Fetching CVEs for date: 2025-11-29
Found 15 CVE(s) for 2025-11-29
Posting CVE-2025-13526 to Google Chat...
✓ Successfully posted CVE-2025-13526
...
============================================================
Completed at: 2025-11-30 16:01:23
Total: 15 CVEs | Posted: 15 CVEs
============================================================
```

Check your Google Chat space - you should see CVE cards appear! 🎉

### Step 5: Schedule Daily Execution

Now schedule it to run automatically every day at 10:00 AM.

#### For Linux/Mac (Using Cron):

```bash
# Open crontab editor
crontab -e
```

Add this line (adjust paths to match your system):
```bash
0 10 * * * cd /home/ubuntu/CVE-Google-Chat-Alert && /usr/bin/python3 cve_monitor.py >> /var/log/cve_monitor.log 2>&1
```

**Finding the correct paths:**
```bash
# Find Python path
which python3
# Output: /usr/bin/python3

# Find your script path
pwd
# Output: /home/ubuntu/CVE-Google-Chat-Alert
```

**Understanding the cron syntax:**
```
 ┌───────────── minute (0 - 59)
 │ ┌───────────── hour (0 - 23)
 │ │ ┌───────────── day of month (1 - 31)
 │ │ │ ┌───────────── month (1 - 12)
 │ │ │ │ ┌───────────── day of week (0 - 6) (Sunday to Saturday)
 │ │ │ │ │
 │ │ │ │ │
 0 10 * * *  = Every day at 10:00 AM
```

**Verify cron job:**
```bash
# List your cron jobs
crontab -l

# Check if cron service is running
sudo systemctl status cron
```

#### For Windows (Using Task Scheduler):

1. Open **Task Scheduler** (search in Start menu)
2. Click **Create Basic Task** in the right panel
3. **Name**: `CVE Monitor`
4. **Description**: `Daily CVE monitoring from Shodan`
5. Click **Next**

6. **Trigger**: Select **Daily**
7. **Start date**: Today
8. **Start time**: `10:00 AM`
9. **Recur every**: `1 days`
10. Click **Next**

11. **Action**: Select **Start a program**
12. **Program/script**: Browse to your Python executable
   - Usually: `C:\Python311\python.exe`
   - Or: `C:\Users\YourName\AppData\Local\Programs\Python\Python311\python.exe`
13. **Add arguments**: Full path to script
   - Example: `C:\Users\YourName\CVE-Google-Chat-Alert\cve_monitor.py`
14. **Start in**: Script directory
   - Example: `C:\Users\YourName\CVE-Google-Chat-Alert`
15. Click **Next**, then **Finish**

**Test immediately:**
Right-click the task → **Run**

### Step 6: Monitor Logs

View logs to ensure everything is working:

```bash
# View logs in real-time
tail -f /var/log/cve_monitor.log

# Or view last 50 lines
tail -n 50 /var/log/cve_monitor.log
```

---

## 🐳 Installation Method 2: Docker (Recommended for Production)

Perfect for: Production environments, servers, containers, easy deployment

### Step 1: Clone the Repository

```bash
# Clone the repository
git clone https://github.com/NoDataFound/CVE-Google-Chat-Alert.git

# Navigate to the directory
cd gg-chatbot-monitor-cve
```

### Step 2: Create Environment File

```bash
# Copy the example file
cp .env.example .env
```

**Note:** If you're on Windows and `cp` doesn't work, use:
```cmd
copy .env.example .env
```

### Step 3: Configure Environment Variables

Edit the `.env` file:

```bash
# Linux/Mac
nano .env

# Or use any text editor
vim .env
code .env
```

Add your Google Chat webhook URL:

```env
# CVE Monitor Configuration
GOOGLE_CHAT_WEBHOOK=https://chat.googleapis.com/v1/spaces/XXXXX/messages?key=YYYYY&token=ZZZZZ
```

**Save and close the file.**

### Step 4: Build and Run with Docker Compose (Easiest)

#### Build the Docker Image:

```bash
docker-compose build
```

You'll see output like:
```
[+] Building 45.2s (12/12) FINISHED
 => [internal] load build definition from Dockerfile
 => => transferring dockerfile: 425B
 => [internal] load .dockerignore
 ...
 => => naming to docker.io/library/cve-monitor
```

#### Start the Container:

```bash
docker-compose up -d
```

The `-d` flag runs it in detached mode (background).

Output:
```
[+] Running 1/1
 ✔ Container cve-monitor  Started
```

#### Verify Container is Running:

```bash
docker ps
```

You should see:
```
CONTAINER ID   IMAGE         COMMAND                  CREATED          STATUS          PORTS     NAMES
abc123def456   cve-monitor   "/bin/sh -c 'cron &&…"   10 seconds ago   Up 9 seconds              cve-monitor
```

### Step 5: Test the Container Immediately

Don't wait until 10:00 AM - test it now:

```bash
docker exec -it cve-monitor python /app/cve_monitor.py
```

You should see the same output as the local installation, and CVE cards should appear in your Google Chat!

### Step 6: Monitor Container Logs

#### View All Logs:

```bash
# Follow logs in real-time
docker-compose logs -f

# View last 50 lines
docker-compose logs --tail=50

# View logs for specific container
docker logs cve-monitor
```

#### View Script Logs:

```bash
# Access the log file inside container
docker exec -it cve-monitor tail -f /var/log/cve_monitor.log

# Or if you mounted the logs volume, view from host
tail -f logs/cve_monitor.log
```

### Alternative: Build and Run Without Docker Compose

If you prefer using Docker directly:

#### Build the Image:

```bash
docker build -t cve-monitor .
```

#### Run the Container:

```bash
docker run -d \
  --name cve-monitor \
  --restart unless-stopped \
  -e TZ=UTC \
  -e GOOGLE_CHAT_WEBHOOK="YOUR_WEBHOOK_URL_HERE" \
  -v $(pwd)/logs:/var/log \
  cve-monitor
```

**For Windows PowerShell:**
```powershell
docker run -d `
  --name cve-monitor `
  --restart unless-stopped `
  -e TZ=UTC `
  -e GOOGLE_CHAT_WEBHOOK="YOUR_WEBHOOK_URL_HERE" `
  -v ${PWD}/logs:/var/log `
  cve-monitor
```

### Managing the Docker Container

```bash
# Stop the container
docker-compose stop
# or
docker stop cve-monitor

# Start the container
docker-compose start
# or
docker start cve-monitor

# Restart the container
docker-compose restart
# or
docker restart cve-monitor

# Stop and remove the container
docker-compose down
# or
docker stop cve-monitor && docker rm cve-monitor

# View container status
docker ps -a

# Access container shell
docker exec -it cve-monitor /bin/bash
```

---

## ⚙️ Configuration & Customization

### Changing the Schedule

The default schedule is **10:00 AM UTC daily**. To change it:

#### For Local Installation:

Edit your crontab:
```bash
crontab -e
```

**Examples:**
```bash
# Every 6 hours
0 */6 * * * cd /path/to/script && python3 cve_monitor.py >> /var/log/cve_monitor.log 2>&1

# Twice daily (9 AM and 9 PM)
0 9,21 * * * cd /path/to/script && python3 cve_monitor.py >> /var/log/cve_monitor.log 2>&1

# Every hour
0 * * * * cd /path/to/script && python3 cve_monitor.py >> /var/log/cve_monitor.log 2>&1

# Monday through Friday at 8 AM
0 8 * * 1-5 cd /path/to/script && python3 cve_monitor.py >> /var/log/cve_monitor.log 2>&1
```

#### For Docker Installation:

Edit the `Dockerfile` (line 17):

```dockerfile
# Change this line:
RUN echo "0 10 * * * cd /app && /usr/local/bin/python /app/cve_monitor.py >> /var/log/cve_monitor.log 2>&1" > /etc/cron.d/cve-monitor

# Examples:
# Every 6 hours:
RUN echo "0 */6 * * * cd /app && /usr/local/bin/python /app/cve_monitor.py >> /var/log/cve_monitor.log 2>&1" > /etc/cron.d/cve-monitor

# Twice daily:
RUN echo "0 9,21 * * * cd /app && /usr/local/bin/python /app/cve_monitor.py >> /var/log/cve_monitor.log 2>&1" > /etc/cron.d/cve-monitor
```

Then rebuild:
```bash
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

### Filtering by CVSS Score

Only show HIGH and CRITICAL vulnerabilities (CVSS ≥ 7.0):

Edit `cve_monitor.py` around line 17:

```python
# Show only HIGH/CRITICAL CVEs
MIN_CVSS_SCORE = 7.0

# Or show all CVEs (default)
MIN_CVSS_SCORE = None
```

### Filtering by Keywords

Only show CVEs matching specific products/vendors:

Edit `cve_monitor.py` around line 18:

```python
# Filter by keywords
FILTER_KEYWORDS = ['linux', 'apache', 'nginx', 'kubernetes', 'docker', 'mysql']

# Or show all CVEs (default)
FILTER_KEYWORDS = None
```

**After editing**, restart:

**Local:**
```bash
# No restart needed, just wait for next scheduled run
# Or test immediately
python3 cve_monitor.py
```

**Docker:**
```bash
docker-compose restart
# Or rebuild for code changes
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

### Changing Timezone

#### For Docker:

Edit `docker-compose.yml`:

```yaml
environment:
  - TZ=America/New_York  # Change to your timezone
  - GOOGLE_CHAT_WEBHOOK=${GOOGLE_CHAT_WEBHOOK}
```

**Common timezones:**
- `UTC` (default)
- `America/New_York` (EST/EDT)
- `America/Los_Angeles` (PST/PDT)
- `Europe/London` (GMT/BST)
- `Europe/Paris` (CET/CEST)
- `Asia/Tokyo` (JST)
- `Asia/Shanghai` (CST)
- `Asia/Ho_Chi_Minh` (ICT)
- `Australia/Sydney` (AEST/AEDT)

[Full timezone list](https://en.wikipedia.org/wiki/List_of_tz_database_time_zones)

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- [Shodan](https://www.shodan.io/) for providing the excellent CVEDB API
- [NIST NVD](https://nvd.nist.gov/) for comprehensive CVE information
- Google Chat for webhook integration
- The open-source community

---

## ⭐ Star This Repository

If you find this tool useful, please consider giving it a star on GitHub! It helps others discover the project and motivates continued development.

[![GitHub stars](https://img.shields.io/github/stars/nguyenthanhvu240/gg-chatbot-monitor-cve?style=social)](https://github.com/nguyenthanhvu240/gg-chatbot-monitor-cve)
