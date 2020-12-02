import json,requests

def login(apic_ip,apic_username,apic_password):

    credentials = {'aaaUser':
                {'attributes':
                    {'name': apic_username, 'pwd': apic_password }
                }
    }

    base_url = 'https://%s/api/' % apic_ip
    login_url = base_url + 'aaaLogin.json'

    json_credentials = json.dumps(credentials)
    post_response = requests.post(login_url, data=json_credentials, verify=False)
    post_response_json = json.loads(post_response.text)
    login_attributes = post_response_json['imdata'][0]['aaaLogin']['attributes']
    cookies = {}
    cookies['APIC-Cookie'] = login_attributes['token']
    return cookies

def fvCEp(apic_ip, cookies):
    request_url = '/node/class/fvCEp.json'
    base_url = 'https://%s/api/' % apic_ip
    response_data = requests.get(base_url + request_url, cookies=cookies, verify = False)
    return response_data.json()

def fvTenant(apic_ip, cookies):
    request_url = '/node/class/fvTenant.json'
    base_url = 'https://%s/api/' % apic_ip
    response_data = requests.get(base_url + request_url, cookies=cookies, verify = False)
    return response_data.json()

def postObject(apic_ip, cookies, objectData):
    request_url = '/mo/uni.json'
    base_url = 'https://%s/api/' % apic_ip
    response_data = requests.post(base_url + request_url, cookies=cookies, json = objectData, verify = False)
    return response_data.json()

def createTenant(apic_ip, cookies, name):
    jsonData = '{"fvTenant" : {"attributes" : {"name" : "%s"}}}' % name
    objectData = json.loads(jsonData)
    return postObject(apic_ip, cookies, objectData)

def deleteTenant(apic_ip, cookies, name):
    jsonData = '{"fvTenant" : {"attributes" : {"name" : "%s", "status" : "deleted"}}}' % name
    objectData = json.loads(jsonData)
    return postObject(apic_ip, cookies, objectData)

def createVrf(apic_ip, cookies, name, fvTenant):
    jsonData = '{"fvCtx": {"attributes": {"dn": "uni/tn-%s/ctx-%s","name": "%s","rn": "ctx-%s","status": "created"}}}' % (fvTenant,name, name, name)
    objectData = json.loads(jsonData)
    return postObject(apic_ip, cookies, objectData)

def createBD(apic_ip, cookies, name, fvCtx, fvTenant):
    jsonData =  '{"fvBD": {"attributes": {"dn": "uni/tn-%s/BD-%s","name": "%s","status": "created"},"children": [{"fvRsCtx": {"attributes": {"tnFvCtxName": "%s"}}}]}}' % (fvTenant,name,name,fvCtx)
    print(jsonData)
    objectData = json.loads(jsonData)
    return postObject(apic_ip, cookies, objectData)