import requests
import os
from dotenv import load_dotenv

def set_webhook(url):
    load_dotenv()
    token = os.getenv("TELEGRAM_TOKEN")
    if not token:
        print("Error: TELEGRAM_TOKEN not found in .env")
        return

    # Telegram Webhook URL
    webhook_url = f"https://api.telegram.org/bot{token}/setWebhook"
    
    # Our app's webhook endpoint
    target_url = f"{url.rstrip('/')}/webhook/telegram"
    
    print(f"Setting webhook to: {target_url}")
    
    response = requests.post(webhook_url, data={"url": target_url})
    
    if response.status_code == 200:
        print("Webhook set successfully!")
        print(response.json())
    else:
        print(f"Failed to set webhook. Status code: {response.status_code}")
        print(response.json())

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python3 set_webhook.py <YOUR_PUBLIC_URL>")
        print("Example: python3 set_webhook.py https://mi-app.render.com")
    else:
        set_webhook(sys.argv[1])
