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

def CEp(apic_ip, cookies):
    request_url = '/node/class/fvCEp.json'
    base_url = 'https://%s/api/' % apic_ip
    response_data = requests.get(base_url + request_url, cookies=cookies, verify = False)
    return response_data.json()