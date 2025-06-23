import requests
import datetime
import os

api_key = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiI0IiwianRpIjoiYjQzMDgwNzBjMDIyMjg5ZWI1OTU2ZTlkZjE2OGM0NWQ3MGQzMTVhYTkzNzdiN2JlZDVmZjkyNTQ0OTU1NzhiNmE4MjY4NTgwMGFlZTM5YTciLCJpYXQiOjE3NDk3NjEwNTQuNjc2MDIxLCJuYmYiOjE3NDk3NjEwNTQuNjc2MDI1LCJleHAiOjQ5MDU0MzQ2NTQuNjcxNTc3LCJzdWIiOiIxNjA0OTM2Iiwic2NvcGVzIjpbXX0.mAns1XvhF9AMh5IpTsQdW6hZMNpZopVk_1XEOrmMVmCdBhuNRbWc0Ybpvn1YS_m0QStcRiZE4w5lGaFbznf4MKs18C8oYgqCQ_EvpYGYkXyu71qH03ZGjz2jQs7umM19OYOWfwJDO9m9z156CYcdMhDLkWSRSvmP7uvBRO1VvdKTLXaX7UjvtlYnbVoxSNZHTIiCIkXN6UjmIU1iX3icLHWxn98PlT3mBFYfj5x_G9vGhK1teRD8Mj_3LI37-QYDiM51FdFBVkbEhFekguHG9Ya1g0O6wt-FtD3SMeSS-4Gs_kh970mKlNVoJqukNowb_TOyXD4QGwXjOS3xJURNvAcgfU1xZWe4C6y4skf0rYedvCwrT0a4k7s_nUBWblw-MMeZ33doRD6hBIQDUBDK0L7iw3zBc9kl3k7howicBJAn3YEACcvwUkqUyKZSEdWXbpFV_9m05kwamguQEcYX-q_BByAvu2Ey2KwnugY4hHIiGbhn0s7TlbdtSSCI02VrHuxgtBxElksAXEpvQezEWIz1V1oGLiK2rG_-WBmLwKOXStngdQ96eeyY6vg31Qv98bI315ts7yv4JJUvTYM3cGzVnFcyWWlVuTMLozG4v45E9I_aapLGUjIligkod7O4FUhjEWT3jUZlGrM1mASAo8wDwKWBEPvDe8ikWRajq34'
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

