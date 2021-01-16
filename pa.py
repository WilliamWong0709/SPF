import requests
import re

urls=[]
f = open('urls.txt', 'r')
text = f.read()
urls = '\n'.split(text);
f.close()

for url in urls:
	print(url);


'''
headers = {
	'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:84.0) Gecko/20100101 Firefox/84.0'
}

r = requests.get('http://stock.finance.sina.com.cn/stock/go.php/vReport_List/kind/search/index.phtml?t1=4&analysts=%C5%CB%95%A9&symbol=&pubdate=2020-06-24', headers=headers)

pattern = re.compile('<a target=.*?title="(.*?)" href="(.*?)">.*?</a>', re.S)
title_link_pairs = pattern.findall(r.text)

stocks=[]
industry_report_links=[]
stock_pattern = re.compile('(.*?)\(\d{6}\).*', re.S)
for title, link in title_link_pairs:
	matchObj = stock_pattern.match(title)
	if matchObj:
		stocks.append(matchObj.group(1))
	else:
		industry_report_links.append('http:' + link)

print(stocks)
print('-------------------------------------------------------')
for l in industry_report_links:
	print(l)

'''