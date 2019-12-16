import json
import requests

from es_utils import send_to_es


def get_api_url_base(pod_ip):
    api_url_base = "http://%s:4040/api/v1" %(pod_ip)
    return (api_url_base)

def get_all_application(api_url_base):
    url = "%s/%s" %(api_url_base, "applications")
    try:
        response = requests.get(url)
        data = json.loads(response.content.decode('utf-8'))
        send_to_es(data)
        return (data)
    except requests.exceptions.RequestException as e:
        print (e)
        return (None)

def get_all_jobs_application(api_url_base, app_id):
    url = "%s/applications/%s/jobs" %(api_url_base, app_id)
    try:
        response = requests.get(url)
        data = json.loads(response.content.decode('utf-8'))
        send_to_es(data)
        return (data)
    except requests.exceptions.RequestException as e:
        print (e)
        return (None)
