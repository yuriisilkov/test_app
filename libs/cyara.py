import requests
import base64
import json
import time

from qaart_utils import SetConfig, GetOption, PrintLog


def get_option(name):
    return GetOption(name)


# had to define these here due to a conflict in get in requests and in qaart
def cyara_placeCall_success(whichId):
    assert cyara_placeCall(whichId)


def cyara_agent1_fullname():
    return get_option('Agent1_fullname')


def cyara_agent2_fullname():
    return get_option('Agent2_fullname')


def cyara_agent3_fullname():
    return get_option('Agent3_fullname')


def cyara_agent4_fullname():
    return get_option('Agent4_fullname')


def cyara_get_routing_skill():
    return get_option('RoutingSkill')


def cyara_get_cId():
    return "3124"


RunId = 0


def cyara_placeCall(whichId):

    cyaraAccountId = get_option('cyaraAccountId')
    # cyaraCampaignId = get_option('cyaraCampaignId')
    cyaraCampaignId = str(whichId)
    cyaraUserId = get_option('cyaraUserId')
    cyaraPassWd = get_option('cyaraPassWd')

    url1 = "https://www.cyaraportal.us/CyaraWebPortal/API/2.0/account/" + cyaraAccountId + "/voice/campaign/" + cyaraCampaignId + "/run"
    rh = dict()
    rh["Authorization"] = "Basic " + base64.b64encode(cyaraUserId + ":" + cyaraPassWd)
    rh["Content-Type"] = "application/json"
    params = {'request': {'runDate': '2015-05-12T02:30:00.00-07:00'}}
    PrintLog(url1)
    r = requests.put(url1, headers=rh, data=json.dumps(params))
    PrintLog("First PUT" + r.text)

    # get will retrieve the run id of the request
    r = requests.get(url1, headers=rh)
    result_data = json.loads(r.text)
    PrintLog("Second GET" + r.text)

    if result_data['previous']['run']['status'] == 'Success':
        global RunId
        RunId = result_data['previous']['run']['runId']
        url2 = "https://www.cyaraportal.us/CyaraWebPortal/API/1.0/report/campaignRunTestResults?runId=" + str(RunId)
        PrintLog(url2)
        s = requests.get(url2, headers=rh)
        s1 = json.loads(s.text)
        PrintLog("Third GET" + s.text)
        return s1['status'] == "Running"

    return False


def cyara_start_campaign(whichId):

    cyaraAccountId = get_option('cyaraAccountId')
    cyaraCampaignId = str(whichId)
    cyaraUserId = get_option('cyaraUserId')
    cyaraPassWd = get_option('cyaraPassWd')

    url1 = "https://www.cyaraportal.us/CyaraWebPortal/API/1.0/campaignrun/" + cyaraCampaignId + "/start"
    rh = dict()
    rh["Authorization"] = "Basic " + base64.b64encode(cyaraUserId + ":" + cyaraPassWd)
    rh["Content-Type"] = "application/json"
    params = {'request': {'runDate': '2015-05-12T02:30:00.00-07:00'}}
    PrintLog("POST request" + url1)
    r = requests.post(url1, headers=rh, data=json.dumps(params))
    PrintLog("POST result" + r.text)
    result_data = json.loads(r.text)

    if result_data['runId'] > 0:
        global RunId
        RunId = result_data['runId']
        return True

    return False


def cyara_start_campaign_success(whichId):
    assert cyara_start_campaign(whichId)


def cyara_delete_campaign(whichId):
    cyaraAccountId = get_option('cyaraAccountId')
    # cyaraCampaignId = get_option('cyaraCampaignId')
    cyaraCampaignId = str(whichId)
    cyaraUserId = get_option('cyaraUserId')
    cyaraPassWd = get_option('cyaraPassWd')

    url1 = "https://www.cyaraportal.us/CyaraWebPortal/API/2.0/account/" + cyaraAccountId + "/voice/campaign/" + cyaraCampaignId + "/run"
    rh = dict()
    rh["Authorization"] = "Basic " + base64.b64encode(cyaraUserId + ":" + cyaraPassWd)
    rh["Content-Type"] = "application/json"
    PrintLog("DELETE request" + url1)
    r = requests.delete(url1, headers=rh)
    PrintLog("DELETE result" + r.text)

    return True


def cyara_delete_campaign_success(whichId):
    assert cyara_delete_campaign(whichId)


def cyara_get_runid():
    return RunId


def cyara_get_campaign_results():
    # its assumed that there is only one campaign run ongoing or started
    global RunId

    cyaraUserId = get_option('cyaraUserId')
    cyaraPassWd = get_option('cyaraPassWd')

    url1 = "https://www.cyaraportal.us/CyaraWebPortal/API/1.0/report/campaignRunTestResults?runId=" + str(RunId)
    rh = dict()
    rh["Authorization"] = "Basic " + base64.b64encode(cyaraUserId + ":" + cyaraPassWd)
    rh["Content-Type"] = "application/json"
    PrintLog("GET request" + url1)

    # r = requests.put(url1, headers=rh, payload=payload)
    r = requests.get(url1, headers=rh)
    PrintLog("GET response" + r.text)
    result_data = json.loads(r.text)
    while (result_data['status'] == 'Running'):
        time.sleep(5)
        r = requests.get(url1, headers=rh)
        PrintLog("GET response" + r.text)
        result_data = json.loads(r.text)

    assert result_data['testResults'][0]['result'] == 'Success' or result_data['testResults'][0]['result'] == 'Satisfactory'


def cyara_wait(waitTime):
    time.sleep(int(waitTime))


def cyara_get_max_hold_skill():
    return str('max_hold')


def cyara_get_no_agent_skill():
    return str('no_agents')


def cyara_get_agent_available_skill():
    return str('transfer')