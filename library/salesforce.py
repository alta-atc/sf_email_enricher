import requests
import json

def get_access_token():
    
    # Obtain the credentials from Google Cloud Secrets
    # with open('/secret_accessToken/credential', 'r') as secret_accessToken:
    #    access_token = secret_accessToken.read().strip()
    #    sf_url = "https://daxorcorporation.my.salesforce.com"

    #    return access_token, sf_url
     
    access_token = "00D5e000003Ts3R!AQsAQMsltctyWfOtflv.5gJjRh.ZeoJzyFYlXp2WmA16NzFLS9aeP6HniOwg5mzcEx2GulfDHoq9ZMrnf.zx08wxKXMoFE_i"
    sf_url = "https://daxorcorporation.my.salesforce.com"

    return access_token, sf_url


def get_contacts():
    print("Getting Contact records...")

    access_token, sf_url = get_access_token()

    # Construct Salesforce API URL for Account object using the global variable
    url = f"{sf_url}/services/data/v58.0/query"

    # Prepare headers for the request
    headers = {
        "Authorization": "Bearer " + access_token,
        "Content-Type": "application/json"
    }

    # Prepare SOQL query
    query = {
        "q": "SELECT Id, FirstName, LastName, Account_Name__c, AccountId, Account_Email_Domain__c "
             "FROM Contact "
             "WHERE Trigger_Email_Enrichment__c = True "
             "LIMIT 250"
    }

    # Send the API request
    response = requests.get(url, headers=headers, params=query)

    # Check the response status
    if response.status_code == 200:
        contacts = response.json()['records']
        
        # Prune 'attributes' from each contact
        for contact in contacts:
            contact.pop('attributes', None)
        
        print(f"Retrieved {len(contacts)} Contact records.")
        return contacts
    else:
        print(f"Failed to retrieve Contacts. Status code: {response.status_code}")
        print(f"Response content: {response.content}")
        raise Exception("Failed to retrieve Contacts.")



def update_contact(sf_contact):
    access_token, sf_url = get_access_token()

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json;charset=UTF-8"
    }

    contact_id = sf_contact.pop('Id', None)
    if not contact_id:
        print("No 'Id' field in contact data.")
        return

    contact_url = f"{sf_url}/services/data/v58.0/sobjects/Contact/{contact_id}"
    response = requests.patch(contact_url, headers=headers, json=sf_contact)

    if response.status_code == 204:
        print(f"Successfully updated contact {contact_id}.")
    else:
        print(f"Failed to update contact {contact_id}. Status code: {response.status_code}")
        print(f"Response content: {response.content}")

