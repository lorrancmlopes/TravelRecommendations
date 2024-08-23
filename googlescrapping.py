from bs4 import BeautifulSoup
import requests

headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'}

url='https://www.google.com/search?q="london+tripadvisor"&ie=utf-8&oe=utf-8&num=10'
html = requests.get(url,headers=headers)

soup = BeautifulSoup(html.text, 'html.parser')

allData = soup.find("div",{"class":"g"})

g=0
Data = [ ]
l={}

link = allData.find('a').get('href')
print(link)