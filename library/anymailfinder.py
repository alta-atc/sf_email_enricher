import requests
import json


def get_api_key():
    
    # Obtain the credentials from Google Cloud Secrets
    with open('/anymailFinder_apiKey/credential', 'r') as secret_accessToken:
        api_key = secret_accessToken.read().strip()
        return api_key



def get_email(contact):
    api_key = get_api_key()

    url = "https://api.anymailfinder.com/v5.0/search/person.json"
    
    headers = {
        "Authorization": f"Bearer {api_key}", 
        "Content-Type": "application/json"
    }

    # Prepare the data payload
    data = {
        "full_name": f"{contact['FirstName']} {contact['LastName']}"
    }

    if 'Account_Email_Domain__c' in contact and contact['Account_Email_Domain__c']:
        data["domain"] = contact['Account_Email_Domain__c']
    elif 'Account_Name__c' in contact and contact['Account_Name__c']:
        data["company_name"] = contact['Account_Name__c']

    # Send the API request
    response = requests.post(url, headers=headers, data=json.dumps(data))

    # Initialize returned variables
    email_address = None
    success = None
    validation = None
    error_explained = None

    # Check the response status
    if response.status_code == 200:
        result = response.json()
        email_address = result['results']['email']
        success = result['success']
        validation = result['results']['validation']
        error_explained = None
        print(f"Retrieved email: {email_address} for contact: {contact['Id']} {contact['FirstName']} {contact['LastName']}")
        print(f"Complete API response: {json.dumps(result, indent=4)}")
    else:
        result = response.json()
        success = result['success']
        error_explained = result.get('error_explained', None)  # Get 'error_explained' field if exists
        print(f"Failed to retrieve email for contact: {contact}. Status code: {response.status_code}")
        print(f"Response content: {response.content}")

    return email_address, success, validation, error_explained


