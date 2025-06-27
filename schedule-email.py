import requests
import datetime
import os

api_key = os.environ['MAILER_LITE_API_KEY']
headers = {'Content-Type': 'application/json', 'Accept': 'application/json', 'Authorization': f'Bearer {api_key}'}
daily_subscriber_group_id = 157035977828730203

def create_campaign(email_date):
    with open(f'emails/{email_date}/content.html', 'r') as file:
        html_content = file.read()

    with open(f'emails/{email_date}/subject.txt', 'r') as file:
        subject = file.read().strip()


    data = {
        "name": f"Primed Parents: {email_date}",
        # "subject": subject,
        # "from": {
        #     "email": "carboneauj@gmail.com",
        #     "name": "Primed Parents"
        # },
        "language": "EN",
        "type": "regular",
        "groups": [daily_subscriber_group_id],
        "emails": [{
            "subject": subject,
            "from_name": "Primed Parents",
            "from": "carboneauj@gmail.com",
            "content": html_content
        }]
    }

    response = requests.post("https://connect.mailerlite.com/api/campaigns", headers=headers, json=data)
    campaign = response.json()
    print(campaign)
    campaign_id = campaign['data']['id']
    print(campaign_id)
    return campaign_id

def schedule_campaign(campaign_id, email_date):
    schedule_json = {
        "delivery": "scheduled",
        "schedule": {
            "date": email_date,
            "hours": "6", # 1 PM ET
            "minutes": "00",
        }
    }

    response = requests.post(
        f"https://connect.mailerlite.com/api/campaigns/{campaign_id}/schedule",
        headers=headers,
        json=schedule_json
    )
    print(f"Response code: {response.status_code}")


def run(email_date):
    campaign_id = create_campaign(email_date)
    schedule_campaign(campaign_id, email_date)

email_date = os.getenv('STARTING_DATE')
run(email_date)

