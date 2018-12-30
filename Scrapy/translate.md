##Python爬虫--POST请求youdao翻译

**链接**：

1.http://blog.csdn.net/nunchakushuang/article/details/75294947

2.https://blog.csdn.net/ISxiancai/article/details/79349184

有道有反爬虫的机制，需要更改一下代码才可以。

在模拟输入数据的时候，从源代码的JS脚本得到同时传入的数据还有即时时间以及**加密**的数据，而且和上面的两个教程里的有些不一样，需要看懂代码后**处理**才可以模拟。

(```)

	import urllib.request
	import urllib.parse
	import json
	import time
	import random
	import hashlib

	while True:
		content = input('Enter the translateing word(input q stop):')
		if content == 'q':
			print('its over!')
			break

		head = {}
		head['User-Agent'] = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'

		url = 'http://fanyi.youdao.com/translate?smartresult=dict&smartresult=rule'

		data = {}

		curtime = str(int(time.time()*1000))
		num = random.randint(1,10)
		salt = str(int(time.time()*1000)) + str(num)
		e = content

		sign = hashlib.md5(("fanyideskweb" + e + salt + "p09@Bn{h02_BIEe]$P^nG").encode('utf-8')).hexdigest()
		#print(sign)
		data['i'] = content
		data['from'] = 'AUTO'
		data['to'] = 'AUTO'
		data['smartresult'] = 'dict' 
		data['client'] = 'fanyideskweb'
		data['salt'] = salt
		data['sign'] = sign
		data['ts'] = curtime
		data['bv'] = '9deb57d53879cce82ff92bccf83a3e4c'
		data['doctype'] = 'json'
		data['version'] = '2.1'
		data['keyfrom'] = 'fanyi.web'
		data['action'] = 'FY_BY_CLICKBUTTION'
		data['typoResult'] = 'false'

		#对数据进行编码处理
		data = urllib.parse.urlencode(data).encode('utf-8')
		#创建一个Request对象，传入参数，注意使用的是POST请求
		request = urllib.request.Request(url=url,data=data,headers = head,method='POST')
		#request.add_header('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36')

		#打开这个请求
		response = urllib.request.urlopen(request)
		#读取返回来的数据
		html_str = response.read().decode('utf-8')
		#把返回的json字符串解析成字典
		html_dict = json.loads(html_str)
		#读取翻译结果
		print('the result is %s' % html_dict['translateResult'][0][0]['tgt'])
		time.sleep(5)


(```)

