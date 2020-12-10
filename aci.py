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
    objectData = {"fvTenant" : 
                    {"attributes" : 
                        {"name" : name}
                    }
                }
    return postObject(apic_ip, cookies, objectData)

def deleteTenant(apic_ip, cookies, name):
    objectData = {"fvTenant" : 
                    {"attributes" : 
                        {"name" : name, "status" : "deleted"}
                    }
                }
    return postObject(apic_ip, cookies, objectData)

def createVrf(apic_ip, cookies, name, fvTenant):
    objectData = {"fvCtx": 
                    {"attributes": 
                        {"dn": "uni/tn-" + fvTenant + "/ctx-" + name,
                        "name": name,
                        "rn": "ctx-" + name,
                        "status": "created"}
                    }
                }
    return postObject(apic_ip, cookies, objectData)

def createBD(apic_ip, cookies, name, fvCtx, fvTenant):
    objectData =  {"fvBD": 
                    {"attributes": 
                        {"dn": "uni/tn-" + fvTenant + "/BD-" + name,
                        "name": name,
                        "status": "created"},
                        "children": [
                            {"fvRsCtx": 
                                {"attributes": 
                                    {"tnFvCtxName": fvCtx}
                                }
                            }
                        ]
                    }
                }
    return postObject(apic_ip, cookies, objectData)

def createAppProfile(apic_ip, cookies, name, fvTenant):
    objectData =  {"fvAp": 
                    {"attributes": 
                        {"dn": "uni/tn-" + fvTenant + "/ap-" + name,
                        "name": name,
                        "status": "created"},
                        "children": []
                    }
                }
    return postObject(apic_ip, cookies, objectData)

def createEPG(apic_ip, cookies, name, fvBD,vlanid, AppProfile, fvTenant, paths, physicalDomain):
    objectData =  {"fvAEPg": 
                    {"attributes": 
                        {"dn": "uni/tn-" + fvTenant + "/ap-" + AppProfile +"/epg-" + name,
                        "name": name,
                        "status": "created"},
                        "children": [
                            {"fvRsBd":
                                {"attributes":
                                    {"tnFvBDName": fvBD
                                    }
                                }
                            },
                            {"fvRsDomAtt":
                               {"attributes":
                                   {"tDn": physicalDomain
                                   }
                                }
                            }
                        ]
                    }
                }
    for path in paths:
        fvRsPathAtt = {"fvRsPathAtt":{
                            "attributes":{
                            "encap":"vlan-" + vlanid,
                            "tDn": path
                            }
                        }
                    }
        objectData["fvAEPg"]["children"].append(fvRsPathAtt)
    return postObject(apic_ip, cookies, objectData)