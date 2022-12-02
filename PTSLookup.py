'''
= Date: 2022-12-01
= Title/Project: API wrapper for PTS (Post-Tele-Styrelsen: Swedish Postal and Telecom Authorities)
= Description: Look up swedish phone numbers and find out which ISP/Operator they belong to
= Author: Aex63/Leonard
= Github: @aex63
= Todo/Ideas: Integrate support to look up phonenumbers from file or database (stored procedure)
'''

# System requirements: Third party module (lxml) for HTML parsing
# pip install lxml

#Required libraries 
import requests
from bs4 import BeautifulSoup
from urllib3.exceptions import InsecureRequestWarning

# Disable SSL Warnings
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

# Input variable: Which phone should we check?
phoneLookup = '076xxxxxx'

# Lets pretend to be a normal browser to disable security
headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:107.0) Gecko/20100101 Firefox/107.0'
}

# Post data: Phone number to check ISP/Operator
login_data = {       
    'NbrToSearch' : phoneLookup
}

# Start a session
with requests.Session() as s:
    # PTS: Swedish Postal and Telecom Authorities
    url = 'https://nummer.pts.se/NbrSearch'

    # Get inutial content and parse
    r = s.get(url, headers = headers, verify = False)
    soup = BeautifulSoup(r.text, 'lxml')

    # Find CSRF-token so we can bypass bot protection
    csrfToken = soup.find('input',attrs = {'name':'__RequestVerificationToken'})['value']

    # Add CSRF-token to POST data
    login_data['__RequestVerificationToken'] = csrfToken

    # POST request: Lookup phonenr
    r = s.post(url, data = login_data, headers = headers, verify = False)
    
    # Reparse the results
    soupResults = BeautifulSoup(r.text, 'lxml')
    
    # Parse and extract the result data
    OperatorData = soupResults.find('div', class_='alert-success').text
    Results = OperatorData.strip().split('tillhör') # Split data into a list for easier access
    Results[0] = Results[0].strip() # Trim whitespace on PhoneNr
    Results[1] = Results[1].strip() # Trim whitespace on Operator

    # Output the results from the Request
    print(Results)
