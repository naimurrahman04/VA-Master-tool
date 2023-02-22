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
from termcolor import colored


# Prompt the user to input the URL
url = input('Enter the URL: ')

# Check if the input starts with http:// or https://
if not url.startswith('http://') and not url.startswith('https://'):
    url = 'http://' + url

try:
    domain = urlparse(url).netloc
    ip = socket.gethostbyname(domain)
    print(ip)
except (socket.gaierror, ValueError, TypeError, AttributeError) as e:
    print(f"Error: {e}")
target = ip  # Replace with your target IP address
start_port = 1
end_port = 100  # Replace with the highest port you want to scan

for port in range(start_port, end_port+1):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(0.1)  # Set a timeout for the connection attempt
    try:
        s.connect((target, port))
    except (socket.timeout, ConnectionRefusedError):
        pass  # Ignore timeouts and refused connections
    else:
        print(f"Port {port} is open")
    finally:
        s.close()
url = "http://example.com"
data = {"param1": "value1", "param2": "value2"}

response = requests.post(url, data=data)
server_info = response.headers["Server"]
print(f"Server information: {server_info}")
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

#test security header

print(Fore.BLUE + Style.BRIGHT+"Test Security header")

security_headers = [
    "Content-Security-Policy",
    "X-Content-Type-Options",
    "X-Frame-Options",
    "X-XSS-Protection",
    "Strict-Transport-Security",
]

# Make a GET request to the specified URL
response = requests.get(url)

# Check if the security headers are present in the response
for header in security_headers:
    if header in response.headers:
        print(f"{header}: {response.headers[header]}")
    else:
        print(f"{header} header is missing")

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

# Read directory names from the wordlist file
with open(wordlist_file, "r", encoding="iso-8859-1") as f:
    directories = [line.strip() for line in f]

# Iterate through each directory name and send a GET request to the URL
for directory in directories:
    directory_url = f"{url}/{directory}"
    response = requests.get(directory_url)
    status_code = response.status_code
    
    # Print directory URL and response status code
    if status_code == 200:
        print(colored(f"{directory_url} || {status_code}", "yellow"))
    else:
        print(f"{directory_url} || {status_code}")
    	
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


