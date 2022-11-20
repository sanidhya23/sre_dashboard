import requests
from requests.auth import HTTPBasicAuth
import json
from pprint import pprint

def get_project_issues(host='mytest12123.atlassian.net', project='TESTTEAM1', 
    email='sannidhya.pagare@gmail.com', api_token='zhxQfCNNQgfZECEibxNy899E'):

    url = f"https://{host}/rest/api/3/search"
    auth = HTTPBasicAuth(email, api_token)
    headers = {"Accept": "application/json"}
    query = {'jql': f"project={project}"}

    response = requests.request(
    "GET",
    url,
    headers=headers,
    params=query,
    auth=auth
    )

    # print(json.dumps(json.loads(response.text), sort_keys=True, indent=4, separators=(",", ": ")))
    return response.json()["issues"]


if __name__ == '__main__':
    pprint(get_project_issues())