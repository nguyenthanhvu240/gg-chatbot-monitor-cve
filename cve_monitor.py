#!/usr/bin/env python3
"""
Daily CVE Monitor using Shodan CVEDB
Fetches CVEs for YESTERDAY (previous day) and posts to Google Chat
Designed to run at 10:00 AM daily
Example: Runs on Sunday 10:00 AM → Fetches Saturday's CVEs
"""

import requests
import json
from datetime import datetime, timezone
import time

# Configuration
# Avatar Bot: https://lh3.googleusercontent.com/proxy/wMlu7uhILc0G4gQKmOcAOO4k5WLhShGe_eK5PVmHWKgaFat3GVI9Ox6lJUIaeqTiVs8OKbPmxUomkyIEdnM8UUk10j4h5ki2Z-kN9wuGG-noFBB6FsMMGRWOSqZaPVM82bsoh3abqrKKJSGHiqdHT9PULwjXyitVeXJ6IkmFNlQ
# Setup Crontab: At 10:00 AM everyday: 0 10 * * * cd /home/kali && /usr/bin/python3 cve_monitor.py >> /var/log/cve_monitor.log 2>&1


# Replace this with new Google Chat
GOOGLE_CHAT_WEBHOOK = "https://chat.googleapis.com/v1/spaces/YOUR_SPACE/messages?key=YOUR_KEY&token=YOUR_TOKEN" # edit this to your google chat webhook
CVEDB_API_URL = "https://cvedb.shodan.io/cves"

# Optional: Filter settings (set to None to get all CVEs)
MIN_CVSS_SCORE = None  # e.g., 7.0 for HIGH/CRITICAL only
FILTER_KEYWORDS = None  # e.g., ['linux', 'apache', 'nginx'] or None for all


def get_yesterday_date():
    """Get yesterday's date from machine host in YYYY-MM-DD format"""
    from datetime import timedelta
    yesterday = datetime.now() - timedelta(days=1)
    return yesterday.strftime('%Y-%m-%d')


def fetch_cves_by_date(date_str):
    """Fetch CVEs from Shodan CVEDB for a specific date"""
    params = {
        'start_date': date_str,
        'end_date': date_str
    }

    print(f"Fetching CVEs for date: {date_str}")

    try:
        response = requests.get(CVEDB_API_URL, params=params, timeout=30)
        response.raise_for_status()
        data = response.json()

        cves = data.get('cves', [])
        print(f"Found {len(cves)} CVE(s) for {date_str}")
        return cves

    except requests.RequestException as e:
        print(f"Error fetching CVEs: {e}")
        return []


def get_cvss_score(cve):
    """Extract CVSS score from CVE data"""
    # Try CVSS v3 first
    if 'cvss_v3' in cve and cve['cvss_v3']:
        return cve['cvss_v3']
    # Fall back to CVSS v2
    if 'cvss_v2' in cve and cve['cvss_v2']:
        return cve['cvss_v2']
    return None


def get_severity_from_score(score):
    """Determine severity level from CVSS score"""
    if score is None:
        return "Unknown"
    elif score >= 9.0:
        return "CRITICAL"
    elif score >= 7.0:
        return "HIGH"
    elif score >= 4.0:
        return "MEDIUM"
    else:
        return "LOW"


def get_severity_emoji(severity):
    """Get emoji for severity level"""
    emoji_map = {
        "CRITICAL": "🔴",
        "HIGH": "🟠",
        "MEDIUM": "🟡",
        "LOW": "🟢",
        "Unknown": "⚪"
    }
    return emoji_map.get(severity, "⚪")


def should_alert(cve):
    """Check if CVE meets alert criteria"""
    # Check CVSS score filter
    if MIN_CVSS_SCORE is not None:
        score = get_cvss_score(cve)
        if score is None or score < MIN_CVSS_SCORE:
            return False

    # Check keyword filter
    if FILTER_KEYWORDS is not None:
        summary = cve.get('summary', '').lower()
        if not any(keyword.lower() in summary for keyword in FILTER_KEYWORDS):
            return False

    return True


def format_cve_message(cve):
    """Format CVE data as a Google Chat card with better formatting"""
    cve_id = cve.get('cve_id', 'Unknown')
    summary = cve.get('summary', 'No description available')

    # Truncate long summaries
    if len(summary) > 500:
        summary = summary[:497] + '...'

    # Get CVSS scores and severity
    cvss_score = get_cvss_score(cve)
    severity = get_severity_from_score(cvss_score)
    emoji = get_severity_emoji(severity)

    # Format score display
    if cvss_score:
        score_display = f"{cvss_score}"
        severity_display = f"{emoji} {severity}"
    else:
        score_display = "N/A"
        severity_display = f"{emoji} Not Scored"

    # Get published date
    published = cve.get('published_time', 'Unknown')
    if published != 'Unknown':
        try:
            pub_date = datetime.fromisoformat(published.replace('Z', '+00:00'))
            published = pub_date.strftime('%b %d, %Y %H:%M UTC')
        except:
            pass

    # Get references
    references = cve.get('references', [])

    # Build widgets list
    widgets = []

    # Severity and Score section
    widgets.append({
        "decoratedText": {
            "startIcon": {
                "knownIcon": "STAR"
            },
            "topLabel": "Severity",
            "text": f"<b>{severity_display}</b>",
            "bottomLabel": f"CVSS Score: {score_display}"
        }
    })

    # Published date
    widgets.append({
        "decoratedText": {
            "startIcon": {
                "knownIcon": "CLOCK"
            },
            "topLabel": "Published",
            "text": published
        }
    })

    # Divider
    widgets.append({"divider": {}})

    # Description
    widgets.append({
        "textParagraph": {
            "text": f"<b>Description:</b><br>{summary}"
        }
    })

    # References section (if available)
    if references:
        ref_count = len(references)
        if ref_count <= 3:
            ref_text = "<br>".join([f"• <a href='{ref}'>{ref[:60]}...</a>" if len(ref) > 60 else f"• <a href='{ref}'>{ref}</a>" for ref in references])
        else:
            ref_text = "<br>".join([f"• <a href='{ref}'>{ref[:60]}...</a>" if len(ref) > 60 else f"• <a href='{ref}'>{ref}</a>" for ref in references[:2]])
            ref_text += f"<br><i>...and {ref_count - 2} more references</i>"

        widgets.append({"divider": {}})
        widgets.append({
            "textParagraph": {
                "text": f"<b>References:</b><br>{ref_text}"
            }
        })

    # Action buttons
    widgets.append({"divider": {}})
    widgets.append({
        "buttonList": {
            "buttons": [
                {
                    "text": "View on Shodan",
                    "onClick": {
                        "openLink": {
                            "url": f"https://cvedb.shodan.io/cve/{cve_id}"
                        }
                    }
                },
                {
                    "text": "View on NVD",
                    "onClick": {
                        "openLink": {
                            "url": f"https://nvd.nist.gov/vuln/detail/{cve_id}"
                        }
                    }
                }
            ]
        }
    })

    # Create Google Chat card
    card = {
        "cardsV2": [{
            "cardId": cve_id,
            "card": {
                "header": {
                    "title": f"{emoji} {cve_id}",
                    "subtitle": f"{severity} Severity",
                    "imageUrl": "https://www.shodan.io/static/img/shodan-icon.png",
                    "imageType": "CIRCLE"
                },
                "sections": [{
                    "widgets": widgets
                }]
            }
        }]
    }

    return card


def post_to_google_chat(message):
    """Send message to Google Chat webhook"""
    headers = {'Content-Type': 'application/json; charset=UTF-8'}

    try:
        response = requests.post(
            GOOGLE_CHAT_WEBHOOK,
            headers=headers,
            data=json.dumps(message),
            timeout=10
        )
        response.raise_for_status()
        return True
    except requests.RequestException as e:
        print(f"Error posting to Google Chat: {e}")
        return False


def send_summary_message(date_str, total_cves, posted_cves):
    """Send a summary message to Google Chat"""

    # Determine summary emoji
    if posted_cves == 0:
        summary_emoji = "✅"
        summary_text = "No new CVEs to report"
    elif posted_cves < 10:
        summary_emoji = "📊"
        summary_text = f"Found {posted_cves} new CVE(s)"
    else:
        summary_emoji = "⚠️"
        summary_text = f"High activity: {posted_cves} new CVE(s)"

    # Get current local time
    local_time = datetime.now().strftime('%b %d, %Y %H:%M')

    summary_card = {
        "cardsV2": [{
            "cardId": f"summary-{date_str}",
            "card": {
                "header": {
                    "title": f"{summary_emoji} Daily CVE Report",
                    "subtitle": date_str
                },
                "sections": [{
                    "widgets": [
                        {
                            "decoratedText": {
                                "startIcon": {
                                    "knownIcon": "DESCRIPTION"
                                },
                                "text": f"<b>{summary_text}</b>"
                            }
                        },
                        {
                            "decoratedText": {
                                "startIcon": {
                                    "knownIcon": "CLOCK"
                                },
                                "topLabel": "Report Generated",
                                "text": local_time
                            }
                        },
                        {
                            "textParagraph": {
                                "text": f"<i>Total CVEs found: {total_cves}<br>CVEs posted: {posted_cves}</i>"
                            }
                        }
                    ]
                }]
            }
        }]
    }
    post_to_google_chat(summary_card)


def main():
    """Main function to fetch and post CVEs"""
    print("="*60)
    print("CVE Monitor - Shodan CVEDB")
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*60)

    # Get yesterday's date from machine host
    yesterday = get_yesterday_date()
    print(f"Checking CVEs for yesterday: {yesterday}")

    # Fetch CVEs for yesterday
    cves = fetch_cves_by_date(yesterday)

    if not cves:
        print("No CVEs found for yesterday")
        send_summary_message(yesterday, 0, 0)
        return

    # Filter and post CVEs
    posted_count = 0
    for i, cve in enumerate(cves):
        if should_alert(cve):
            cve_id = cve.get('cve_id', f'CVE-{i}')
            print(f"Posting {cve_id} to Google Chat...")

            card = format_cve_message(cve)
            if post_to_google_chat(card):
                posted_count += 1
                print(f"✓ Successfully posted {cve_id}")
            else:
                print(f"✗ Failed to post {cve_id}")

            # Rate limiting: wait 1 second between posts to avoid overwhelming the webhook
            if i < len(cves) - 1:
                time.sleep(1)

    # Send summary
    send_summary_message(yesterday, len(cves), posted_count)

    print("="*60)
    print(f"Completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Total: {len(cves)} CVEs | Posted: {posted_count} CVEs")
    print("="*60)


if __name__ == '__main__':
    main()
