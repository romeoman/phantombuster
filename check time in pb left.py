import os
import requests

def main(event):
    # Define the Phantombuster API endpoint and headers
    url = "https://api.phantombuster.com/api/v2/orgs/fetch-resources"
    headers = {
        "accept": "application/json",
        "X-Phantombuster-Org": "33071",
        "X-Phantombuster-Key": os.getenv('PBAPI')  # Fetch the API key from environment variable
    }

    try:
        # Send GET request to Phantombuster
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            resource_data = response.json()
            print("Resource Data:", resource_data)

            # Get the time left in seconds
            time_left_seconds = resource_data['dailyExecutionTime']

            return {
                "outputFields": {
                    "timeLeft": time_left_seconds
                }
            }
        else:
            response.raise_for_status()

    except Exception as e:
        print('Error:', e)
        return {
            "outputFields": {}
        }
