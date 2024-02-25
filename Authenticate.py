import requests
import time 

clientID = '526b68c64c4bc9b0d63b'  
scope = 'repo' 

endpoint_url = 'https://github.com/login/device/code'  
veri_params= {
    'client_id': clientID,
    'scope': scope
} 

veri_headers = {
    'Accept': 'application/json' 
}

def getUserCode():
    try:
        response = requests.post(endpoint_url, params = veri_params, headers = veri_headers)
        veriData = response.json() 
        # print(f'veriData: {veriData}')

        userCode = veriData["user_code"]
        veriUri = veriData["verification_uri"] 

        print(f'user code : {userCode}') 
        print(f'please use above user code on this url -> "{veriUri}" for authenfication')

        return veriData
    except Exception as e:
        print(f'Error while getting verification data: {e}')

def getAccessToken():
    veriData = getUserCode()

    access_token_url = 'https://github.com/login/oauth/access_token' 
    at_params = {
        "client_id": clientID,
        "device_code": veriData["device_code"],
        "grant_type": "urn:ietf:params:oauth:grant-type:device_code"
    }

    at_headers = {
        'Accept': 'application/json'
    }

    try: 
        access_token = ''
        while True:
            time.sleep(veriData['interval'])
            response = requests.post(access_token_url, params=at_params, headers=at_headers)
            data = response.json() 
            # print(data)

            if response.status_code == 200: 
                if "error" in data: 
                    print('authorization pending')
                    continue 
                else: 
                    access_token = data['access_token']
                    # print(f'Access Token: {access_token}')
                    break
            else:
                error = data['error']
                print(f'Error: {response.status_code}, {error}') 
                break

        return access_token
    except Exception as e:
        print(f'Error while getting access token: {e}')


