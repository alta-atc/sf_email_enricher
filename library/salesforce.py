        # Get contacts where 
        # email enrich = true 
        # get first name, last name, email domain, accountId 

        # make new field in salesforce on account - email domain 
        # make new field on contact to mirror this data 
        # make logic in salesforce to select on the correct contacts for enrichment 
            # that means, NPI is populated and successfully synced 
            # and the user has a HF score of D or higher 
            # OR the user has a taxonomy in the selection criteria

import requests

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


    # get the maximum number of contacts in one query 
    # find contacts where ""

    return contacts