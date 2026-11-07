
import time
import requests

from ai_agent import analyze_incident
from notifications import notify_incident


# Website to monitor
WEBSITE = "https://httpbin.org/status/503"

# Check every 60 seconds
CHECK_INTERVAL = 60

# Prevent duplicate alerts
last_incident = None


def check_website():
    try:
        response = requests.get(
            WEBSITE,
            timeout=10
        )

        status_code = response.status_code

        if status_code >= 400:
            return (
                f"HTTP {status_code}",
                f"Website returned HTTP {status_code}"
            )

        return None

    except requests.exceptions.SSLError:
        return (
            "SSL Error",
            "HTTPS SSL/TLS verification failed"
        )

    except requests.exceptions.ConnectTimeout:
        return (
            "Connection Timeout",
            "Server connection timed out"
        )

    except requests.exceptions.ReadTimeout:
        return (
            "Request Timeout",
            "Server response timed out"
        )

    except requests.exceptions.ConnectionError as error:
        return (
            "Connection Error",
            str(error)
        )

    except requests.exceptions.RequestException as error:
        return (
            "Request Error",
            str(error)
        )


def monitor_website():
    global last_incident

    print("Website monitoring started...")

    while True:

        incident = check_website()

        if incident:

            error, details = incident

            if incident != last_incident:

                print(f"New incident detected: {error}")
                print("AI is investigating the incident...")

                # AI Incident Analysis
                try:
                    ai_analysis = analyze_incident(
                        error,
                        details
                    )

                    print("\nAI ANALYSIS:")
                    print(ai_analysis)

                except Exception as e:
                    print(f"AI analysis failed: {e}")

                    ai_analysis = (
                        "AI analysis unavailable. "
                        "Manual investigation required."
                    )

                # Send incident + AI analysis to Gmail
                notify_incident(
                    WEBSITE,
                    error,
                    details
                    + "\n\nAI INCIDENT ANALYSIS:\n"
                    + ai_analysis
                )

                last_incident = incident

            else:
                print(f"Incident still active: {error}")

        else:
            print("Website healthy: HTTP status below 400")
            last_incident = None

        time.sleep(CHECK_INTERVAL)


if __name__ == "__main__":

    try:
        monitor_website()

    except KeyboardInterrupt:
        print("\nMonitoring stopped.")
