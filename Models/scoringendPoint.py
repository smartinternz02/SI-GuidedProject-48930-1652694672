import requests

# NOTE: you must manually set API_KEY below using information retrieved from your IBM Cloud account.
API_KEY = "<lzvVjuXgmUKxoSIR5xkFsvexxqCGxXOZd4EkR2a2iHPj>"
token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey":
 API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
mltoken = token_response.json()["access_token"]

header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}

# NOTE: manually define and pass the array(s) of values to be scored in the next line
payload_scoring = {"input_data": [{"fields":[["f0","f1","f2","f3","f4","f5","f6"]],"values":[[19,6,207,90,4504,15,81]] }]}
response_scoring = requests.post('https://us-south.ml.cloud.ibm.com/ml/v4/deployments/309ed04f-6b22-434b-ae54-b5a3804c0d9f/predictions?version=2022-06-02', json=payload_scoring,
 headers={'Authorization': 'Bearer ' + mltoken})
print("Scoring response")
print(response_scoring.json())
pred = response_scoring.json()
output=pred['prediction'][0]['values'][0][0][0]