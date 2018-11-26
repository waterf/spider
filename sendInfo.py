#!usr/bin/python/
#-*-encoding=utf8-*-

'''
使用crontab -e
*/60 18-22 * * * python /home/jin/python/sendInfo/py 
>>/home/jin/python/testcrontab.log 2>&1
'''
from lxml import etree
import urllib
from bs4 import BeautifulSoup #html
import os
import requests
import random

# mail
import smtplib
from email.mime.text import MIMEText
from email.header import Header


def send_mail(text):
	mail_host = "smtp.qq.com"
	mail_user = "985926011@qq.com"
	mail_pass = "***************"

	sender = "985926011@qq.com"
	receivers = ["985926011@qq.com", "2214137007@qq.com"]

	message = MIMEText(text, 'plain', 'utf-8')
	message['From'] = Header("jin", 'utf-8')
	message['To'] = Header('jin', 'utf-8')

	subject = "数学讲座更新提醒"
	message['Subject'] = Header(subject, 'utf-8')

	try:
		smtpObj = smtplib.SMTP_SSL("smtp.qq.com", 465)
		smtpObj.login(mail_user, mail_pass)
		smtpObj.sendmail(sender, receivers, message.as_string())
		print "success"
	except smtplib.SMTPException:
		print "Error: failed"

def get_content(url):
	header = {
		'User-Agent': "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:56.0) Gecko/20100101 Firefox/56.0",
		'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
		'Accept-Language': "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
		'Accept-Encoding': "gzip, deflate",
		'Connecting': "keep-alive"
	}
	timeout = random.choice(range(100, 120))
	content = requests.get(url, headers=header, timeout=timeout).content
	return content

def analyse_html(html):
	soup = BeautifulSoup(html, 'lxml');
	data = soup.select('.NewsBody > p') # path: according to firfox	
	return data # change nth-child to nth-of-type(3)
	# type(data)=unicode

def write_data(info):
	os.chdir("/home/jin/python/") # pwd
	file = open("data.txt", 'w') # no 'rw'
	file.truncate() # flip file
	flag = 0
	for ele in info:
		trueEle = ele.get_text().encode('utf8').lstrip();
		if len(trueEle) and ord(trueEle[0]) >= ord('1') and ord(trueEle[0]) <= ord('9'):
			if flag==0:
				sum = int(ele.get_text().encode('utf8')[1]) + int(ele.get_text().encode('utf8')[0]) * 10
				if sum > 49:
					send_mail("数学讲座已更新，速去报名！http://www.math.zju.edu.cn/news.asp?id=6624&TabName=%B1%BE%BF%C6%BD%CC%D1%A7")	
				flag = 1
			file.write(ele.get_text().encode('utf8')) #type(ele.encode('utf8'))='str'
			file.write('\n')
	file.close()


if '__name__ == __main__':
	url = 'http://www.math.zju.edu.cn/news.asp?id=6624&TabName=%B1%BE%BF%C6%BD%CC%D1%A7'
	html = get_content(url)
	#print html.encode('utf8') #after encode:str before:unicode
	data = analyse_html(html)
	write_data(data)
