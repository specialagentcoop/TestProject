from bs4 import BeautifulSoup
import requests

url = 'https://www.cvmarket.lt/darbo-skelbimai?op=search&search%5Bjob_salary%5D=3&ga_track=homepage&search%5Bcategories%5D%5B%5D=8&search%5Bkeyword%5D='

response = requests.get(url)
# print(response)

soup = BeautifulSoup(response.content, 'html.parser')

print(soup.prettify())