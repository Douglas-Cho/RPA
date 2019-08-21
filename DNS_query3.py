# Whois query version 0.5 written by DKC
import requests
import time
import random
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

# Fake headers to deceive detection tools.
ua = UserAgent()
cUa_text = ua.random
cHeaders = {'User-Agent': cUa_text}


# Define query function.
def whois_query(url):
    time.sleep(random.randint(60, 600))
    response = requests.get(url, headers=cHeaders)
    response_html = response.content
    # Soup the response and determine if already registered.
    souped = BeautifulSoup(response_html, 'html.parser')
    c_registry_data_text = str(souped('pre', {'id': 'registryData', }))
    n_exist = len(souped('a', {'id': 'availableLink'}))
    if n_exist == 1:
        # If not registered, open output file and append the domain name and "No".
        c_results = url + ',' + "No" + '\n'
        f1.write(c_results)
    else:
        # If already registered, open output file and append the domain name and "Yes".
        c_results = url + "," + "Yes" + '\n'
        registry_data_text = c_registry_data_text + '\n'
        # Write the results.
        f1.write(c_results)
        f2.write(registry_data_text)


# Open output file to write.
f1 = open('c:\\Downloads\\Whois_Out.txt', 'wt')
f2 = open('c:\\Downloads\\RegistryData.txt', 'wt')

# Read input file and put into input arrays.
f3 = open('c:\\Downloads\\Input_Functions.txt', 'rt')
f4 = open('c:\\Downloads\\Input_Connectors.txt', 'rt')
cFunctions = f3.readlines()
cConnectors = f4.readlines()

# Without connectors.
for cFunction in cFunctions:
    cxFunction = cFunction.split('\n')[0]
    cUrl = "https://whois.com/whois/" + cxFunction + "xyz.org"
    whois_query(cUrl)

# With connectors.
for cFunction in cFunctions:
    # Combine a url to request.
    cxFunction = cFunction.split('\n')[0]
    for cConnector in cConnectors:
        cxConnector = cConnector.split('\n')[0]
        cUrl = "https://whois.com/whois/" + cxFunction + cxConnector + "xyz.org"
        whois_query(cUrl)

# Close the files.
f1.close()
f2.close()
f3.close()
f4.close()