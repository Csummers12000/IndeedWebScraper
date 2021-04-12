#region 0: Libraries, Functions, and Global Variables
#   Note - the region/endregion notation allows blocks of code to be collapsed in Visual Studio Code.  This makes the program much easier to read and navigate.
#   Functions themselves can also be collapsed.
import time
import requests
import random
import smtplib, ssl
import sys
import traceback
import pandas
from bs4 import BeautifulSoup

starttime = time.time()
def runtime():
    #required libraries - time
    uptime = time.time() - starttime
    days, notdays = divmod(uptime, 86400)
    hours, nothours = divmod(notdays, 3600)
    minutes, seconds = divmod(nothours, 60)
    print("Total Uptime: {:0>2}:{:0>2}:{:0>2}:{:0>2}".format(int(days),int(hours),int(minutes),int(seconds)))
    return(uptime)

def livetimer(waittime):
    #required libraries - time
    #required libraries - sys
    DecTime = float(waittime) - int(waittime)
    time.sleep(DecTime)
    for remaining in range(int(waittime), 0, -1):
        sys.stdout.write("\r")
        days, notdays = divmod(remaining, 86400)
        hours, nothours = divmod(notdays, 3600)
        minutes, seconds = divmod(nothours, 60)
        sys.stdout.write("Timer: {:0>2}:{:0>2}:{:0>2}:{:0>2} ".format(int(days),int(hours),int(minutes),int(seconds)))
        sys.stdout.flush()
        time.sleep(1)
    days, notdays = divmod(int(waittime), 86400)
    hours, nothours = divmod(notdays, 3600)
    minutes, seconds = divmod(nothours, 60)
    sys.stdout.write("\rslept {:0>2}:{:0>2}:{:0>2}:{:0>2} ".format(int(days),int(hours),int(minutes),int(seconds)) + '(' + str(round(waittime,1)) + 's)'"\n")

Safe_Request_Lower_Wait_Bound = 10
Safe_Request_Upper_Wait_Bound = 20
def saferequest(url):
    #required libraries - requests, random
    #required functions - livetimer()
    #optional libraries - nordvpn_switcher (for rotating IP with NordVPN), Beautifulsoup (for parsing html)
    safetime = random.uniform(Safe_Request_Lower_Wait_Bound, Safe_Request_Upper_Wait_Bound)
    livetimer(safetime)
    get = requests.get(url)
    if 'safe_get_counter' not in str(globals()):
        global safe_get_counter
        safe_get_counter = 1
    else:
        safe_get_counter += 1
    print("Request " + str(safe_get_counter) + " complete")
    #region - NordVPN
    #uncomment the next 2 line if nordvpn_switcher is enabled
    #if (int(safe_get_counter) % 100==0):
    #    rotate_VPN(google_check = 1)
    #endregion - NordVPN
    return(get)

with open('D:\Documents\Email_Credentials\SenderEmail.txt', 'r', encoding="utf-8") as cred1: 
    sender = str(cred1.read())
cred1.close()
with open('D:\Documents\Email_Credentials\RecieverEmail.txt', 'r', encoding="utf-8") as cred2: 
    reciever = str(cred2.read())
cred2.close()
with open('D:\Documents\Email_Credentials\Password.txt', 'r', encoding="utf-8") as cred3: 
    password = str(cred3.read())
cred3.close()
def EmailAlert(subject, body):
    #required libraries - smtlib, ssl
    #optional libraries - sys, traceback (for handling errors)
    port = 0
    smpt_server = 'smtp.gmail.com'
    sender_email = sender
    receiver_email = reciever
    sender_password = password
    SUBstring = str(subject)
    BODstring = str(body)
    message = 'Subject: {}\n\n{}'.format(SUBstring, BODstring)
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smpt_server, port, context=context) as server:
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, receiver_email, message)

JobTitles = ['data+analyst', 'data+scientist', 'database+administrator', 'machine+learning+engineer', 'data+engineer']

States = ['Virginia', 'New+York+State', 'California', 'Texas', 'Washington+State']

unformatted_URL = 'https://www.indeed.com/jobs?q={}&l={}&sort=date'

#print(unformatted_URL.format(JobTitles[0], States[0]))

#endregion 0

#region 1: Initializing saved files
#I know it's just 25 requests, but I'd still like to make as few requests as possible. Saving scraped data and using that instead of re-scraping is the best way I know how to do that

try:
    with open('scraped_data.csv', 'r', encoding="utf-8") as scrape_data:
        None
    scrape_data.close()
    print('CSV detected - Skipping web scrape')
    csvfound = True
except:
    with open('scraped_data.csv', 'w', encoding="utf-8") as scrape_data:
        scrape_data.write('Job_Title' + '|' + 'Company_Name' + '|' + 'Job_Location' + '|' + 'Salary' + '|' + 'Job_Description' + '|' + 'Posting_Date' + '|' + 'Company_Rating' + '\n')
    scrape_data.close()
    print('CSV not detected - CSV initialized')
    csvfound = False
time.sleep(0.1)

#endregion 1

#region 2: Scraping Data
if csvfound == False:
    for job in JobTitles:
        for state in States:
            link = unformatted_URL.format(job, state)
            page = saferequest(link)
            runtime()
            bs = BeautifulSoup(page.content, "html.parser")
            divs = bs.find_all("div", class_="jobsearch-SerpJobCard")
            for div in divs:
                #setting up job_listing_info list - elements will be [Job Title, Company Name, Job Location, Salary, Job Description, Date of Posting, Company Rating]
                job_listing_info = []

                #finding job title
                h2_tags = div.find_all('h2')
                if len(h2_tags) == 1:
                    a_tags = h2_tags[0].find_all("a")
                    if len(a_tags) == 1:
                        jobtitle = a_tags[0].get('title')
                        job_listing_info.append(jobtitle)
                    elif len(a_tags) == 0:
                        job_listing_info.append('Missing')
                    else:
                        print('error: found more than one job title a_tag')
                        print(a_tags)
                        print(len(a_tags))
                        input('stop')
                elif len(h2_tags) == 0:
                    job_listing_info.append('Missing')
                else:
                    print('error: found more than one job title h2_tag')
                    print(h2_tags)
                    print(len(h2_tags))
                    input('stop')

                #finding company name
                company_spans = div.find_all("span", class_="company")
                if len(company_spans) == 1:
                    almost_companyname = company_spans[0].text.replace('\n', '')
                    companyname = almost_companyname.replace('|', '<pipe>')
                    job_listing_info.append(companyname)
                elif len(company_spans) == 0:
                    job_listing_info.append('Missing')
                else:
                    print('error: found more than one company span element')
                    print(company_spans)
                    print(len(company_spans))
                    input('stop')  
                
                #finding job location
                location_spans = div.find_all(["div","span"], class_="location")
                if len(location_spans) == 1:
                    location = location_spans[0].text.replace('\n', '')
                    job_listing_info.append(location)
                elif len(location_spans) == 0:
                    job_listing_info.append('Missing')
                else:
                    print('error: found more than one location span element')
                    print(location_spans)
                    print(len(location_spans))
                    input('stop')

                #finding salary
                salary_spans = div.find_all("span", class_="salaryText")
                if len(salary_spans) == 1:
                    salary = salary_spans[0].text.replace('\n', '')
                    job_listing_info.append(salary)
                elif len(salary_spans) == 0:
                    job_listing_info.append('Missing')
                else:
                    print('error: found more than one salary span element')
                    print(salary_spans)
                    print(len(salary_spans))
                    input('stop')

                #finding job desc
                summaryDivs = div.find_all('div', class_="summary")
                if len(summaryDivs) == 1:
                    listItems = summaryDivs[0].find_all('li')
                    if len(listItems) > 0:
                        desc = ''
                        for listItem in listItems:
                            item = listItem.text
                            desc += item
                            desc += ' '
                        job_listing_info.append(desc)
                    else:
                        job_listing_info.append('Missing')
                elif len(summaryDivs) == 0:
                    job_listing_info.append('Missing')
                else:
                    print('error: found more than one summary div element')
                    print(summaryDivs)
                    print(len(summaryDivs))
                    input(stop)
                
                #finding date of posting
                date_spans = div.find_all('span', class_="date")
                if len(date_spans) == 1:
                    dateposted = date_spans[0].text
                    job_listing_info.append(dateposted)
                elif len(date_spans) == 0:
                    job_listing_info.append('Missing')
                else:
                    print('error: found more than one date span element')
                    print(date_spans)
                    print(len(date_spans))
                    input('stop')
                
                #finding company rating
                rating_spans = div.find_all('span', class_="ratingsDisplay")
                if len(rating_spans) == 1:
                    rating = rating_spans[0].text.replace('\n','')
                    job_listing_info.append(rating)
                elif len(rating_spans) == 0:
                    job_listing_info.append('Missing')
                else:
                    print('error: found more than one rating span element')
                    print(rating_spans)
                    print(len(rating_spans))
                    input('stop')

                #writing scraped data to save file
                if len(job_listing_info) == 7:
                    clean_info = []
                    for item1 in job_listing_info:
                        item2 = str(item1)
                        item3 = item2.replace('\n', '')
                        item4 = item3.replace('|', '<pipe>')
                        clean_info.append(item4)
                else:
                    print('error: found more than seven job elements')
                    print(job_listing_info)
                    print(len(job_listing_info))
                    input('stop')
                if len(clean_info) == 7:
                    with open('scraped_data.csv', 'a', encoding="utf-8") as scrape_data: 
                        #scrape_data contents: Job Title, Company Name, Job Location, Salary, Job Description, Date of Posting, Company Rating
                        scrape_data.write(clean_info[0] + '|' + clean_info[1] + '|' + clean_info[2] + '|' + clean_info[3] + '|' + clean_info[4] + '|' + clean_info[5] + '|' + clean_info[6] + '\n')
                    scrape_data.close()
                else:
                    print('error: found more than seven job elements')
                    print(clean_info)
                    print(len(clean_info))
                    input('stop')
    csvfound = True
#endregion 2

#region 3: Data Manipulation

if csvfound == True:
    csv = pandas.read_csv('scraped_data.csv', delimiter='|')
    df = pandas.DataFrame(csv)

    #pretty sure I already removed all the newline charechters, but the directions say I need this line of code anyway
    df=df.replace('\n','', regex=True)
    df.head()

    #splitting the job location column into two columns
    stateABBRV = ['VA', 'NY', 'CA', 'TX', 'WA']
    def label_state(row):
        if row['Job_Location'] == 'Missing':
            return('Missing')
        else:
            for state in stateABBRV:
                if row['Job_Location'].find(state) != -1:
                    return(state)
                elif row['Job_Location'].find('New York State') != -1:
                    return('NY')
                elif row['Job_Location'].find('Washington State') != -1:
                    return('WA')
                elif row['Job_Location'].find('California') != -1:
                    return('CA')
                elif row['Job_Location'].find('Virginia') != -1:
                    return('VA')
                elif row['Job_Location'].find('Texas') != -1:
                    return('TX')
                elif row['Job_Location'].find('United States') != -1:
                    return('Missing')
            print('error: no state found and value not missing')
            print(row)
            print('')
            print(row['Job_Location'])
            input('stop')
    df['State'] = df.apply(lambda row: label_state(row), axis=1)
    def label_city(row):
        if row['Job_Location'] == 'Missing':
            return('Missing')
        else:
            for state in stateABBRV:
                if row['Job_Location'].find(state) != -1:
                    findindex = int(row['Job_Location'].find(state)) - 2
                    city = row['Job_Location'][:findindex]
                    return(city)
                elif row['Job_Location'].find('New York State') != -1:
                    return('Missing')
                elif row['Job_Location'].find('Washington State') != -1:
                    return('Missing')
                elif row['Job_Location'].find('California') != -1:
                    return('Missing')
                elif row['Job_Location'].find('Virginia') != -1:
                    return('Missing')
                elif row['Job_Location'].find('Texas') != -1:
                    return('Missing')
                elif row['Job_Location'].find('United States') != -1:
                    return('Missing')
            print('error: no state found and value not missing')
            print(row)
            print('')
            print(row['Job_Location'])
            input('stop')
    df['City'] = df.apply(lambda row: label_city(row), axis=1)

    #printing percentage of jobs in each city
    value_counts = df.City.value_counts(normalize=True, ascending=True)
    for city, rel_freq in zip(value_counts.index, value_counts.values):
        print(str(city)+':', str(round(float(rel_freq)*100, 1))+'%')

#endregion 3

#region 4: Saving to CSV

df.to_csv('Summers_Chris_INST447_PA2.csv', index=False)

#endregion 4