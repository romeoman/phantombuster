import os
import requests
import json

def main(event):
    # Extract the required input fields
    containerId = event['inputFields']['containerId']
    hsObjectId = event['inputFields']['hs_object_id']

    # Define the Phantombuster API endpoint and headers to fetch the result
    result_url = f"https://api.phantombuster.com/api/v2/containers/fetch-result-object?id={containerId}"
    headers = {
        "Content-Type": "application/json",
        "X-Phantombuster-Key": os.getenv('PBAPI')  # Fetch the API key from environment variable
    }

    # Logging for debugging
    print(f"Container ID: {containerId}")
    print(f"HubSpot Object ID: {hsObjectId}")
    print(f"Fetching data from: {result_url}")

    try:
        # Send GET request to Phantombuster to fetch the result
        result_response = requests.get(result_url, headers=headers)

        # Logging the status for debugging
        print(f"Response Status: {result_response.status_code}")
        print(f"Response Data: {result_response.text}")

        # Check if the response status is 200 (OK)
        if result_response.status_code == 200:
            result_data = result_response.json()
    
            # Convert the string representation of list back to a JSON object
            company_data_list = json.loads(result_data['resultObject'])
    
            # Assuming the result is the first item in the list
            if not company_data_list:
                print("No data in the response.")
                return {
                    "outputFields": {}
                }
                
            company_data = company_data_list[0]
            return {
                "outputFields": {
                    "growth6Mth": company_data['growth6Mth'],
                    "growth1Yr": company_data['growth1Yr'],
                    "growth2Yr": company_data['growth2Yr']
                }
            }
        else:
            result_response.raise_for_status()

    except Exception as e:
        print('Error:', e)
        return {
            "outputFields": {}
        }

