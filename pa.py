import requests
import re
import copy
import time
import random
import csv

def write_csv(l):
	csv_file = 'stocks.csv'
	row = []
	with open(csv_file, 'w', encoding='utf-8-sig', newline='') as f:
		writer = csv.writer(f)
		writer.writerow(l[0])
		for i in range(0, len(l[0])):
			row = [l[j][i] for j in range(1, len(l[1]))]
			print('-------------------------------')
			print(row)
			writer.writerow(row)

def my_sleep():
	t = 20 + random.randint(2, 9)
	time.sleep(t)

def fetch_by_analyst(url):
	headers = {
		'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:84.0) Gecko/20100101 Firefox/84.0'
	}
	print('***********Entering fetch_by_analyst()**************')
	my_sleep();
	r = requests.get(url, headers=headers)

	pattern = re.compile('<a target=.*?title="(.*?)" href="(.*?)">.*?</a>', re.S)
	title_link_pairs = pattern.findall(r.text)

	stockset = set()
	industry_report_links = []
	stock_pattern = re.compile('(.*?)\(\d{6}\).*', re.S)
	for title, link in title_link_pairs:
		matchObj = stock_pattern.match(title)
		if matchObj:
			stockset.add(matchObj.group(1))
		else:
			industry_report_links.append('http:' + link)

	'''
	print(stocks)
	print('-------------------------------------------------------')
	for l in industry_report_links:
		print(l)
	'''
	stocks = [s for s in stockset]

	#print(stocks)
	return stocks

#def write_csv(file_name, industry, popular_stocks):




'''
url = 'http://stock.finance.sina.com.cn/stock/go.php/vReport_List/kind/search/index.phtml?t1=4&analysts=%BA%FA%D3%D6%CE%C4&symbol=&pubdate=2020-06-15'
stocks = fetch_by_analyst(url)
print(stocks)
'''

urls = []
file_name = 'urls.txt'
f = open(file_name, 'r', encoding='utf-8')
lines = f.readlines()
f.close()

#print(lines)

dict = {}
industry = 'dummy'
analysts = []
for line in lines:
	line = line[:-1]
	if line != '':
		if line[0] == '#':
			dict[industry] = copy.deepcopy(analysts)
			industry = line[1:]
			analysts.clear()
		else:
			analysts.append(line)

dict[industry] = copy.deepcopy(analysts)
dict.pop('dummy')

print(dict)

industries = []
'''
	*l[0]存储一个由行业名称构成的列表，类似表头
	*l[i]存储l[0][i-1]所对应行业的股票列表
'''
l = [industries,]
stock_pool = {}
popular_stocks = []
for industry, analysts in dict.items():
	stock_pool.clear()
	for analyst in analysts:
		stocks = fetch_by_analyst(analyst)
		#print(stocks)
		for stock in stocks:
			if stock in stock_pool:
				stock_pool[stock] += 1
			else:
				stock_pool[stock] = 1

	#print(stock_pool)
	popular_stocks = [k for k, v in stock_pool.items() if v > 1]
	print("length: " + str(len(popular_stocks)))
	#print(popular_stocks)
	l[0].append(industry)
	l.append(copy.deepcopy(popular_stocks))
	print(l)
	stock_pool.clear()
	popular_stocks.clear()


# 由于CSV文件只能按行写入，我们要想实现按列的效果，这里先要对齐各行各列的长度，最终形成一个max_len*max_len的方阵
# 不足的填充dummy_char补齐
dummy_char = ''
max_len = len(max(l, key=lambda item:len(item)))

# 对齐各列
for col in l:
	col_len = len(col)
	for i in range(0, max_len-col_len):
		col.append(dummy_char)

# 补齐成max_len*max_len的方阵
col_cnt = len(l)
dummy_col = [dummy_char for i in range(0, max_len) ]
for i in range(0, max_len-col_cnt):
	l.append(dummy_col)

#for col in l:
#	print(col)

write_csv(l)
