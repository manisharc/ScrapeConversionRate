# ScrapeConversionRate
Scrapes a website to figure out the USD to INR rate and writes it to a file or sends an email if the rate is above a certain value. 
Run as a cron job daily.
On OSX, 
>crontab -e
Opens up a file.
Add the following, which will run the job daily at 10am.
The python path should be same as the result of >which python
0 10 * * * cd /Users/Projects/ScrapeConversionRate/ && /usr/local/bin/python scrape.py
