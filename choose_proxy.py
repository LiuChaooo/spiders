import urllib
import urllib2
import time
from bs4 import BeautifulSoup

def build_request(url='http://www.xicidaili.com'):
	headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36 OPR/44.0.2510.1449'}
	url = url
	request = urllib2.Request(url,headers=headers)
	return request


def get_proxies():
	request = build_request()
	response = urllib2.urlopen(request).read()
	soup = BeautifulSoup(response, 'lxml')
	block = soup.find_all('tr')[2:]
	
	proxies = []
	for each in block:
		proxy = {}
		tlist = each.find_all('td')
		if tlist:
			proxy[str(tlist[5].get_text()).lower()] = str(tlist[1].get_text())+':'+str(tlist[2].get_text())
			proxies.append(proxy)

	return proxies


def check_proxy(proxies):
	request = build_request('http://www.baidu.com')
	new_proxies = []
	for proxy in proxies:
		proxy_handler = urllib2.ProxyHandler(proxy)
		opener = urllib2.build_opener(proxy_handler)
		try:
			response = opener.open(request, timeout=5)
			new_proxies.append(proxy)

		except Exception, e:
			pass

		finally:
			time.sleep(0.5)


	return new_proxies

import json
def main():
	proxies = get_proxies()
	print 'finish get_proxies'
	new_proxies = check_proxy(proxies)
	print new_proxies
	
	content = json.dumps(new_proxies)
	with open('proxy_pool.json','w') as f:
		f.write(content.encode('utf-8'))

if __name__ == '__main__':
	main()