
from library.salesforce import get_contacts, update_contact
from library.anymailfinder import get_email
from datetime import datetime
import pytz
import time
from cloudevents.http import CloudEvent
import functions_framework

@functions_framework.cloud_event
def daxor_emailEnricher(cloud_event: CloudEvent) -> None:

    print("Email Enricher Starting...")
    
    # Get records from salesforce to enrich 
    contacts_to_enrich = get_contacts()

    if not contacts_to_enrich:
        print("No contacts returned for enrichment.")
        print("Ending Script Run")
        return

    # begin loop through contacts_to_enrich 
    for contact in contacts_to_enrich:
        print(f'Processing contact: {contact["Id"]} {contact["FirstName"]} {contact["LastName"]}')
        
        # get current datetime for Mexico city
        tz = pytz.timezone('America/Mexico_City')
        current_time = datetime.now(tz).strftime('%Y-%m-%dT%H:%M:%S')

        # Check if "AccountId" is set
        if not contact.get("AccountId"):
            sf_contact = {
                "Id": contact["Id"],
                "Email_Enrichment_Status__c": "Account not set",
                "Force_Enrich_Email__c": False,
                "Email_Last_Enriched__c": current_time
            }
            print("AccountId is not set for this contact. Skipping...")
            update_contact(sf_contact)
            continue  # Skip the rest of the loop and move to the next contact

        # for each contact, make an API call to anymailfinder 
        email_address, result, validation, error = get_email(contact)

        # if there is an error 
        if error is not None:
            sf_contact = {
                "Id": contact["Id"],
                "Email_Enrichment_Status__c": error,
                "Force_Enrich_Email__c": False,
                "Email_Last_Enriched__c": current_time
            }
            print(f'Error for contact: {contact["Id"]} {contact["FirstName"]} {contact["LastName"]} - Error {error}')
            update_contact(sf_contact)
            continue  # Skip the rest of the loop and move to the next contact

        # if email not found 
        if email_address is None:
            enrichment_status = "Email Not Found"
            print(f'No email found for contact: {contact["Id"]} {contact["FirstName"]} {contact["LastName"]} - Result {result} - Validation {validation}')
        else:
            # if email found 
            enrichment_status = "Email Succesfully Found"
            print(f'Email found for contact: {contact["Id"]} {contact["FirstName"]} {contact["LastName"]} - found email {email_address} - Result {result} - Validation {validation}')



        # build the contact object 
        sf_contact = {
            "Id": contact["Id"],
            "Email": email_address,
            "Email_Enrichment_Status__c": enrichment_status,
            "Email_Last_Enriched__c": current_time,
            "Force_Enrich_Email__c": False,
            "Email_Validation_Status__c": validation
        }

        print(f'Constructed Contact: {sf_contact}')

        # update the contact in salesforce
        print("Updating contact in salesforce...")
        update_contact(sf_contact)
        print("Contact updated successfully.")

        # wait for 2 seconds before processing the next contact
        time.sleep(2)

    # end loop 

    print("All contacts updated successfully. Ending Script")

    return



