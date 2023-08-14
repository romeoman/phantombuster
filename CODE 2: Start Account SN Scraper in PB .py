import os
import requests

def main(event):
    # Extract the required input fields
    linkedinCompanyPage = event['inputFields']['linkedin_company_page']
    hsObjectId = event['object']['objectId']

    # Define the Phantombuster API endpoint, headers, and payload for launch
    launch_url = "https://api.phantombuster.com/api/v2/agents/launch"
    headers = {
        "Content-Type": "application/json",
        "X-Phantombuster-Key": os.getenv('PBAPI')  # Fetch the API key from environment variable
    }
    payload = {
        "id": "8637067489167032",
        "arguments": {
            "sessionCookie": os.getenv('PB_SESSION_COOKIE'),  # Fetch the session cookie from environment variable
            "spreadsheetUrl": linkedinCompanyPage
        },
        "manualLaunch": False
    }

    # Print out the payload for debugging
    print("Payload:", payload)

    try:
        # Send POST request to Phantombuster for launch
        response = requests.post(launch_url, json=payload, headers=headers)

        # Check for a successful response and extract the containerId
        if response.status_code == 200:
            response_data = response.json()
            if 'containerId' in response_data:
                return {
                    "outputFields": {
                        "containerId": response_data['containerId'],
                        "hs_object_id": hsObjectId
                    }
                }
            else:
                raise ValueError('Unexpected response from Phantombuster: No containerId.')
        else:
            response.raise_for_status()

    except Exception as e:
        print('Error:', e)
        return {
            "outputFields": {}
        }
