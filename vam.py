import requests
import socket
import nmap
import os
import sys
import webbrowser
import time
from urllib.parse import urlparse
from pprint import pprint
from tqdm import tqdm
from colorama import Fore, Style
from selenium.webdriver.common.by import By



# Prompt the user to input the URL
url = input('Enter the URL: ')
domain = urlparse(url).netloc
print(domain)
ip=socket.gethostbyname(domain)
print(socket.gethostbyname(domain))
# Make a GET request to the specified URL with the headers
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

with tqdm(total=100, desc='Loading') as pbar:
        response = requests.get(url, headers=headers)
for _ in range(100):
        pbar.update(1)
# Print the request header
print(Fore.BLUE + Style.BRIGHT+"request header")
pprint(response.request.headers)
print(Style.RESET_ALL)
# Print the response header
print(Fore.GREEN + Style.BRIGHT +"response header")
pprint(response.headers)
print(Style.RESET_ALL)
# Print the response content
pprint(response.content)

with open('temp01.html', 'w') as f:
    f.write(response.content.decode('utf-8'))

# Open the temporary HTML file in the default web browser
webbrowser.open('temp01.html')
pprint("testing http chunked")
payload = "POST / HTTP/1.1\r\nHost: example.com\r\nContent-Length: 4\r\nTransfer-Encoding: chunked\r\n\r\n0\r\n\r\nPOST / HTTP/1.1\r\nHost: example.com\r\nContent-Length: 4\r\n\r\nabcd"


with tqdm(total=100, desc='Loading') as pbar:
# Send the HTTP request with the payload and headers
        response = requests.request(method='POST', url=url, headers=headers, data=payload)
for _ in range(100):
        pbar.update(1)

# Print the request header
print(Fore.BLUE + Style.BRIGHT+"request header")
pprint(response.request.headers)
print(Style.RESET_ALL)
# Print the response header
print(Fore.GREEN + Style.BRIGHT +"response header")
pprint(response.headers)
print(Style.RESET_ALL)
# Print the response content
pprint(response.content)

with open('temp02.html', 'w') as f:
    f.write(response.content.decode('utf-8'))

# Open the temporary HTML file in the default web browser
webbrowser.open('temp02.html')

#test csp


print(Fore.GREEN + Style.BRIGHT +"Test CSP")

# Send an HTTP request to the target web page
response = requests.get(url)
print(Fore.BLUE + Style.BRIGHT+"request header")
pprint(response.request.headers)
print(Fore.GREEN + Style.BRIGHT +"response header")
pprint(response.headers)

# Check if the response has a Content-Security-Policy header
if 'Content-Security-Policy' in response.headers:
    csp_header = response.headers['Content-Security-Policy']
    print('CSP Header: ', csp_header)
else:
    print('No CSP Header Found')

print(Style.RESET_ALL)


#click jacking test
print(Fore.GREEN + Style.BRIGHT +"Testing Click jacking")
html = '''
<html>
	<head>
		<title>Clickjacking Test Page</title>
	</head>

	<body>
		<h1>Clickjacking Test Results</h1>
		<h2>Target: <a href="%s">%s</a></h2>
		<h3>If you see the target website rendered below, it is <font color="red">VULNERABLE</font>.</h3>
		<iframe width="900" height="600" src="%s"></iframe>
		<iframe style="position: absolute; left: 20px; top: 250px; opacity: 0.8; background: AliceBlue; font-weight: bold;" src="cj-attacker.html"></iframe>
	</body>
</html>
''' % (url, url, url)

html2 = '''
<html>
	<div style="opacity: 1.0; left: 10px; top: 50px; background: PapayaWhip; font-weight: bold;">
		<center><a href="#">THIS IS AN EXAMPLE CLICKJACKING IFRAME AND LINK</a>
		<br>(normally invisible)</center>
	</div>
</html>
'''

cjt = os.path.abspath('cj-target.html')
cja = os.path.abspath('cj-attacker.html')
localurl = 'file://' + cjt

with open(cjt, 'w') as t, open (cja, 'w') as a:
	t.write(html)
	a.write(html2)

webbrowser.open(localurl)

print('\n[+] Test Complete!')


wordlist_file = input("Enter the path to the wordlist file: ")
with open(wordlist_file, "r", encoding="iso-8859-1") as f:
    directories = [line.strip() for line in f]

# Send a GET request to the website and get the response content
response = requests.get(url)
content = response.content.decode("utf-8")

# Find the URLs in the response content that contain the directory names
for directory in directories:
    directory_url = f"{url}/{directory} ||"
    response = requests.get(directory_url)
   
    if response.status_code == 200:
    	print(directory_url+" || "+str(response))
    else:
    	print(directory_url+" || "+str(response))
    	
scanner = nmap.PortScanner()

# Use the PortScanner object to scan the specified IP address
scanner.scan(ip, arguments='-p-')

# Loop through the open ports found by the PortScanner object
for host in scanner.all_hosts():
    print('Host : %s (%s)' % (host, scanner[host].hostname()))
    print('State : %s' % scanner[host].state())

    for proto in scanner[host].all_protocols():
        print('Protocol : %s' % proto)

        ports = scanner[host][proto].keys()
        sorted_ports = sorted(ports)

        for port in sorted_ports:
            print('Port : %s\tState : %s\tService : %s' % (port, scanner[host][proto][port]['state'], scanner[host][proto][port]['name']))


