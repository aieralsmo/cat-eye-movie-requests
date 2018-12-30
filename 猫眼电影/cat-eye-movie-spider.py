import re
import json

import pprint
import requests
from requests.exceptions import RequestException

def get_one_page(url):
	try:
		resp = requests.get(url)
		
		if resp.status_code == requests.codes.ok:
			return resp.text
		return None

	except RequestException as e:
		return None

def parse_one_page(html):
	pattern = re.compile(r'<dd>.*?board-index.*?>(\d+)</i>.*?data-src="(.*?)".*?movie-item-info.*?title="(.*?)".*?star">(.*?)</p>.*?releasetime">(.*?)</p>.*?integer">(\d+).*?</dd>', re.S)
	items = re.findall(pattern,html)
	if items:

		for item in items:
			yield{
				'index':item[0].strip(),
				'image':item[1].strip(),
				'title':item[2].strip(),
				'actor':item[3].strip(),
				'date':item[4].strip(),
				'score':item[5].strip()
			}
	else:
		yield '匹配不到任何结果'


def write_to_file(content):
	item = json.dumps(content,indent=4,ensure_ascii=False)
	with open('cat-eye-movie-spider-data.json', "a",encoding="utf-8") as wf:
		wf.write(item + '\n')

def main(offset):
	url = "https://maoyan.com/board/4?offset="+str(offset)
	html = get_one_page(url)
	for item in parse_one_page(html):
		if isinstance(item, dict):
			write_to_file(item)

if __name__ == "__main__":

	for i in range(10):
		main(i * 10)
