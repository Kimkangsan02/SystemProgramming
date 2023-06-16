import webbrowser
import time
def open_url(url):
	webbrowser.open(url)

with open('link.txt', 'r') as file:
	lines=file.readlines()
	for url in lines:
		open_url(url)
		time.sleep(2)
