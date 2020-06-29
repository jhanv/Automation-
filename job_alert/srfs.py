import requests
from bs4 import BeautifulSoup
import datetime
import smtplib
import time

URL = 'https://jobsearch.sfs.upenn.edu/seo/job_search/'
#User Agent (User Agent reveal a catalog of technical data about the device and software that the visitor is using)
headers = {"User-Agent" : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'}


def getDate():

    #Returns data from the website
    page = requests.get(URL, headers = headers)
    #Gives the content that is there on the website and 'html.parser' parses every element and 
    soup = BeautifulSoup(page.content, 'html.parser')
    #find the required element (.get_text() return only the text leaving the html code)
    title = soup.find("td", class_ = "jobs", align = "left").get_text()
    date_posted = soup.find("td", class_ = "jobs", align = "right").get_text()
    #.strip() unnecesarry  removes the white spaces from thr text
    month = int(date_posted.strip()[0:2])
    date = int(date_posted.strip()[3:])
    print(title, date)
    return month, date


def today():

    #todays time can be opted form the datetime
    now = datetime.datetime.now()
    #takes the month
    month = int(now.strftime("%m"))
    #takes the date
    date = int(now.strftime("%d"))
    return month, date


def track_job():

    job_month, job_date = getDate()
    current_month, current_date = today()
    if(job_month == current_month & job_date == current_date):
        print("A new job found")

        send_mail()
    else:
        print("nothing new")
        send_mail()


def send_mail():

    #connect an gmail with connection number for google is 587
    server = smtplib.SMTP('smtp.gmail.com', 587)
    #identifies ourselves with the mail server that we are using
    server.ehlo()
    #to encrypt the traffic
    server.starttls()
    server.ehlo()
    server.login('sender@email', 'sender_password' )

    subj = "New Job Posted in SFS website!"
    body = f"Check the student employment website link -- {URL}"
    
    msg = f"Subject : {subj} \n\n {body}"
    server.sendmail('sender@email', 'receiver@email', msg)
    print("email has been sent")
    server.quit()


if __name__ == "__main__":
    
    track_job()
    # while(True):
    #     track_job()
    #     time.sleep(60*60)



