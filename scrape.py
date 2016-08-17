#Resources used
#http://naelshiab.com/tutorial-send-email-python/
#http://www.thegeekstuff.com/2009/06/15-practical-crontab-examples/
#https://first-web-scraper.readthedocs.io/en/latest/#what-you-will-make

#!/usr/local/bin/python
import ConfigParser
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
import csv
import datetime as dt
import requests
from BeautifulSoup import BeautifulSoup

url = 'http://www.dollar2rupee.net/'
response = requests.get(url)
html = response.content

soup = BeautifulSoup(html)
table = soup.find('table')
list_of_cells = []
list_of_cells.append(dt.datetime.today().strftime("%m/%d/%Y"))

#find the values for axis and indus
for row in table.findAll('tr')[2:3]:
    for td in row.findAll('td')[1:2]:
        axis  = float(td.text)
        list_of_cells.append(axis)   
    for td in row.findAll('td')[3:4]:
        indus = float(td.text)
        list_of_cells.append(indus)
#print list_of_cells

def sendEmail():
    config = ConfigParser.ConfigParser()
    config.readfp(open(r'emaildetails.txt'))
    fromaddr = config.get('Accounts', 'fromAddr')
    toaddr = config.get('Accounts', 'toAddr')
    pwd = config.get('Accounts', 'pwd')
    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = "USD to INR exchange rate today"
    body = "Axis Rate: " + str(axis) + " Indus Rate: " + str(indus)
    msg.attach(MIMEText(body, 'plain'))

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(fromaddr, pwd)
    text = msg.as_string()
    server.sendmail(fromaddr, toaddr, text)
    server.quit()

#write to a file with the current date
def writeToFile():
    with open("./conversiondata.csv", "a") as fp:
        wr = csv.writer(fp, dialect='excel')
        wr.writerow(list_of_cells)

# if the value > 66.5, send email
if axis > 66.4 or indus > 66.5:
    sendEmail()

writeToFile()
