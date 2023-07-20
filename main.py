
from library.salesforce import get_contacts, update_account, update_contacts, get_domain_contacts
from library.anymailfinder import get_email
from datetime import datetime
import pytz

def daxor_emailEnricher():
    # Get records from salesforce to enrich 
    contacts_to_enrich = get_contacts()
    sf_contacts = []

    # begin loop through contacts_to_enrich 
    for contact in contacts_to_enrich:
        print(f"Processing contact: {contact}")

        # for each, determine if an email-domain field is set 
        domain = contact.get("EmailDomain__c")
        if not domain:
            # if not set, work out the email domain and set that field 
            domain = set_domain(contact)
            update_account(domain, contact)
            print(f"Updated domain for contact: {contact} to {domain}")

        # for each contact, make an API call to anymailfinder 
        email_address = get_email(contact, domain)

        # if email not found 
        if email_address is None:
            enrichment_status = "Email Not Found"
            print(f"No email found for contact: {contact}")
        else:
            # if email found 
            enrichment_status = "Email Succesfully Found"
            print(f"Email found for contact: {contact}")

        # get current datetime for Mexico city
        mexico_tz = pytz.timezone('America/Mexico_City')
        current_time = datetime.now(mexico_tz).strftime('%Y-%m-%dT%H:%M:%S')

        # build the contact object 
        sf_contact = {
            "Email": email_address,
            "Email_Enrichment_Status__c": enrichment_status,
            "Email_Last_Enriched__c": current_time
        }

        # append sf_contact to sf_contacts list
        sf_contacts.append(sf_contact)

    # end loop 

    # update all contacts using the batch API 
    update_contacts(sf_contacts)
    print("All contacts updated successfully.")

    return


from collections import Counter



def set_domain(contact):
    # get 100 contacts from the account, where an email address is set 
    domain_contacts = get_domain_contacts(contact)

    # to store the domain of each contact
    domains = []

    # for the 100 returned records in domain_contacts
    for domain_contact in domain_contacts:
        # look at the field domain_contact("Email")
        email = domain_contact.get("Email")
        if email:
            # break each email after the @ symbol to get the domain 
            domain = email.split('@')[1]
            domains.append(domain)

    # then, after this is complete 
    # we will look for the most common domain 
    domain_counter = Counter(domains)
    most_common_domain = domain_counter.most_common(1)[0][0]

    # example, 26 contacts have emails ending in @google.com
    # and 70 contacts have domains at @gmail.com - we use @gmail.com as the selected domain 
    selected_domain = most_common_domain

    # note, selected_domain should not include an @
    return selected_domain
