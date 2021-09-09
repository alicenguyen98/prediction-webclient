import requests
from concurrent.futures import ThreadPoolExecutor, as_completed

from . import config
from . import app

def make_requests(data):
    
    results = list()
    try:
        conf = config.get()

        endpoints = conf.get('endpoints', None)
        if not endpoints:
            raise Exception("No available endpoints")       

        with ThreadPoolExecutor() as executor:

            futures = list()

            # Schedule endpoint requests
            for ep_key, make_request in [('watson', make_watson_request), ('prediction_server', make_prediction_server_request)]:
                if endpoint_defs := endpoints.get(ep_key):
                    for ep in endpoint_defs:
                        future = executor.submit(make_request, endpoint=ep, data=data)
                        futures.append(future)
            
            
            for future in as_completed(futures):
                result = future.result()
                if result:
                    results.append(result)
    except Exception as e:
        app.logger.error(e)

    return results

def make_watson_request(endpoint: dict, data: dict):
    try:
        token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey": endpoint["api_key"], "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
        mltoken = token_response.json()["access_token"]

        header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}

        values = [data[x] for x in endpoint["param_names"]]
        payload = {"input_data": [{"fields": [endpoint["param_names"]], "values": [values] }]}

        response = requests.post(endpoint["endpoint"], json=payload, headers={'Authorization': 'Bearer ' + mltoken})

        # Request finished
        response_data = response.json()

        if errors := response_data.get('errors', None):
            raise Exception(f"Failed request:\n{errors[0]['code']}: {errors[0]['message']}")

        # Return the first prediction
        result = {
            "name": endpoint['name'],
            "value": response_data['predictions'][0]['values'][0][0]
            } 

        return result

    except Exception as e:
        print(e)

def make_prediction_server_request(endpoint, data):
    try:
        payload = {
            "params": data
        }

        # Check if a specific model is defined
        if "model" in endpoint:
            payload["model"] = endpoint["model"]

        response = requests.post(endpoint["endpoint"], json=payload)
        response_data = response.json()

        if error := response_data.get('error', None):
            raise Exception(f"Failed request:\n{error}")

        result = {
            "name": endpoint['name'],
            "value": response_data['prediction']
            }

        return result

    except Exception as e:
        app.logger.error(e)