import requests
from bs4 import BeautifulSoup
import datetime
import smtplib
import time

URL = 'https://jobsearch.sfs.upenn.edu/seo/job_search/'
#User Agent (User Agent reveal a catalog of technical data about the device and software that the visitor is using)
headers = {"User-Agent" : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'}


def getData():

    #Returns data from the website
    page = requests.get(URL, headers = headers)
    #Gives the content that is there on the website and 'html.parser' parses every element and 
    soup = BeautifulSoup(page.content, 'html.parser')
    #find the required element (.get_text() return only the text leaving the html code)
    title = soup.find("td", class_ = "jobs", align = "left").get_text().strip()
    href = soup.find("td", class_ = "jobs", align = "left").find('a', href = True).get('href')
    link = URL+href
    date_posted = soup.find("td", class_ = "jobs", align = "right").get_text()
    #.strip() unnecesarry  removes the white spaces from thr text
    month = int(date_posted.strip()[0:2])
    date = int(date_posted.strip()[3:])
    # print(link,title, month, date)
    return link, title, month, date


def get_details():

    job_link, job_title, job_month, job_date = getData()
    page = requests.get(job_link, headers = headers)
    soup = BeautifulSoup(page.content, 'html.parser')
    any = soup.find_all("div", class_ = "boxed")
    work_study = any[1].find('b').get_text()
    pay = any[1].get_text().split('\n')[2].strip()
    print(pay)
    return work_study, pay
    

def today():

    #todays time can be opted form the datetime
    now = datetime.datetime.now()
    #takes the month
    month = int(now.strftime("%m"))
    #takes the date
    date = int(now.strftime("%d"))
    return month, date


def track_job():

    job_link, job_title, job_month, job_date = getData()
    current_month, current_date = today()
    work_study, pay = get_details()
    print(work_study, type(work_study), type('Work-Study Only') )
    condition = 'Work-Study Only'
    if(job_month == current_month and job_date == current_date and work_study != 'Work-Study Only'):
        print("A new job found", job_title)
        send_mail(job_title, pay)
    else:
        print("nothing new")


def send_mail(title, pay):

    #connect an gmail with connection number for google is 587
    server = smtplib.SMTP('smtp.gmail.com', 587)
    #identifies ourselves with the mail server that we are using
    server.ehlo()
    #to encrypt the traffic
    server.starttls()
    server.ehlo()
    server.login('sender@email', 'sender_password')
    #the content to be written in the email
    subj = "New Job Posted in SFS website!"
    body = f"Hi,  \n\n A New Employment Oppurtunity !\n\n The position '{title}' is available with pay {pay}\n For more details, Check the student employment website link -- {URL} \n \n Be Quick ..!"
    msg = f"Subject : {subj} \n\n {body}"
    server.sendmail('sender@email', 'receiver@email', msg)
    print("email has been sent")
    server.quit()



if __name__ == "__main__":
    while(True):
        track_job()
        #checks for the job every half an hour
        time.sleep(60*30)



