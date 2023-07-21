import json
import requests
import time
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
def cleanup():
    # Delete the scan
    dummy = requests.delete(MyAXURL + '/scans/' + MyScanID, headers=MyRequestHeaders, verify=False)
    # Delete the target
    dummy = requests.delete(MyAXURL + '/targets/' + MyTargetID, headers=MyRequestHeaders, verify=False)

# Declare variables
MyAXURL = "https://192.168.10.138:3443/api/v1"
MyAPIKEY = "1986ad8c0a5b3df4d7028d5f3c06e936c1081212f1cfb4f2495dcd769a71d035b"
MyTargetURL = "http://testphp.vulnweb.com/"
MyTargetDESC = "Test PHP Site - created via ax-python-api.py"
FullScanProfileID = "11111111-1111-1111-1111-111111111111"
MyRequestHeaders = {'X-Auth': MyAPIKEY, 'Content-Type': 'application/json'}

# Create our intended target - target ID is in the JSON response
MyRequestBody = {"address": MyTargetURL, "description": MyTargetDESC, "type": "default", "criticality": 10}
MyTargetIDResponse = requests.post(MyAXURL + '/targets', json=MyRequestBody, headers=MyRequestHeaders, verify=False)
MyTargetIDjson = json.loads(MyTargetIDResponse.content)
MyTargetID = MyTargetIDjson["target_id"]

# Trigger a scan on the target - scan ID is in the HTTP response headers
MyRequestBody = {
    "profile_id": FullScanProfileID,
    "incremental": False,
    "schedule": {"disable": False, "start_date": None, "time_sensitive": False},
    "user_authorized_to_scan": "yes",
    "target_id": MyTargetID
}

MyScanIDResponse = requests.post(MyAXURL + '/scans', json=MyRequestBody, headers=MyRequestHeaders, verify=False)
MyScanID = MyScanIDResponse.headers["Location"].replace("/api/v1/scans/", "")

LoopCondition = True
while LoopCondition:
    MyScanStatusResponse = requests.get(MyAXURL + '/scans/' + MyScanID, headers=MyRequestHeaders, verify=False)
    MyScanStatusjson = json.loads(MyScanStatusResponse.content)
    MyScanStatus = MyScanStatusjson["current_session"]["status"]
    if MyScanStatus == "processing":
        print("Scan Status: Processing - waiting 30 seconds...")
    elif MyScanStatus == "scheduled":
        print("Scan Status: Scheduled - waiting 30 seconds...")
    elif MyScanStatus == "completed":
        LoopCondition = False
    else:
        print("Invalid Scan Status: Aborting")
        cleanup()
        exit()
    MyScanStatus = ""
    time.sleep(30)

# Obtain the scan session ID
MyScanSessionResponse = requests.get(MyAXURL + '/scans/' + MyScanID, headers=MyRequestHeaders, verify=False)
MyScanSessionjson = json.loads(MyScanSessionResponse.content)
MyScanSessionID = MyScanSessionjson["current_session"]["scan_session_id"]

# Obtain the scan result ID
MyScanResultResponse = requests.get(MyAXURL + '/scans/' + MyScanID + "/results", headers=MyRequestHeaders, verify=False)
MyScanResultjson = json.loads(MyScanResultResponse.content)
MyScanResultID = MyScanResultjson["results"][0]["result_id"]

# Obtain scan vulnerabilities
MyScanVulnerabilitiesResponse = requests.get(MyAXURL + '/scans/' + MyScanID + '/results/' + MyScanResultID + '/vulnerabilities',
                                             headers=MyRequestHeaders, verify=False)

print("")
print("Target ID: " + MyTargetID)
print("Scan ID: " + MyScanID)
print("Scan Session ID: " + MyScanSessionID)
print("Scan Result ID: " + MyScanResultID)
print("")
print("")
print("Scan Vulnerabilities")
print("====================")
print("")
print(MyScanVulnerabilitiesResponse.content)