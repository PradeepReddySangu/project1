#importing all the important modules
from bs4 import BeautifulSoup
from bs4.element import NamespacedAttribute
import requests
import time
from collections import Counter
import pandas as pd
import matplotlib.pyplot as plt



#defining the functions that we need
def getting_values(x):
    soup = BeautifulSoup(x, 'lxml')
    count = soup.find('h1')
    total =count.span
    return(list(str(total.text).split())[0])

def chart():
    l=[]
    jobs_name =['application developer','front end developer','back end developer','data scientist','game developer','quality analyst','full stack engineer','cloud engineer']
    if(int(input("Do you want the detailed analysis on how many number of the jobs that are present in the industry\nEnter the 1 to continue or 0 otherwise"))):
        print("wait getting the details")

        #1 application developer
        html = requests.get('https://www.timesjobs.com/candidate/job-search.html?searchType=personalizedSearch&from=submit&txtKeywords=Application+Developer&txtLocation=').text
        l.append(int(getting_values(html)))

        #2front end developer
        html2 = requests.get('https://www.timesjobs.com/candidate/job-search.html?searchType=personalizedSearch&from=submit&txtKeywords=Front+End+Developer&txtLocation=').text
        l.append(int(getting_values(html2)))
        
        #3 back end developer
        html3 = requests.get('https://www.timesjobs.com/candidate/job-search.html?searchType=personalizedSearch&from=submit&txtKeywords=back+end+developer&txtLocation=').text
        l.append(int(getting_values(html3)))

        #4 data scientist
        html4 = requests.get('https://www.timesjobs.com/candidate/job-search.html?searchType=personalizedSearch&from=submit&txtKeywords=data+scientist&txtLocation=').text
        l.append(int(getting_values(html4)))

        #5 game developer
        html5 = requests.get('https://www.timesjobs.com/candidate/job-search.html?searchType=personalizedSearch&from=submit&txtKeywords=Game+Developer&txtLocation=').text
        l.append(int(getting_values(html5)))

        #6 quality analyst
        html6 = requests.get('https://www.timesjobs.com/candidate/job-search.html?searchType=personalizedSearch&from=submit&txtKeywords=Quality+Analyst&txtLocation=').text
        l.append(int(getting_values(html6)))


        #7 full stack engineer
        html8 = requests.get('https://www.timesjobs.com/candidate/job-search.html?searchType=personalizedSearch&from=submit&txtKeywords=full+stack+engineer&txtLocation=').text
        l.append(int(getting_values(html8)))



        #8 cloud engineer
        html10 = requests.get('https://www.timesjobs.com/candidate/job-search.html?searchType=personalizedSearch&from=submit&txtKeywords=cloud+engineer&txtLocation=').text
        l.append(int(getting_values(html10)))


        #making the chart
        plt.barh(jobs_name, l)
        for index, value in enumerate(l):
            plt.text(value, index,str(value))
        plt.title(" Present Job vacancies in the industry ")

        plt.show()

    #getting the information from the user 
    print("\nenter the job number you need to get information,enter the number before it")
    j=0
    for i in jobs_name:
        print(j,i)
        j=j+1
    job_choosen = int(input())
    if(job_choosen<8):
        job_choosen = jobs_name[job_choosen]
    else:
        print("Enter the correct value")
        job_choosen = int(input())
        job_choosen = jobs_name[job_choosen]
        
    def getting_job_data(url_list):
        #printing the skills
        print("\nwait getting the details about the top 20 skills about the job")
        for i in url_list:
            html_text = requests.get(i).text
            soup = BeautifulSoup(html_text, 'lxml')
            jobs = soup.find_all('li', class_ = 'clearfix job-bx wht-shd-bx' )
            for job in jobs:
                skills = job.find('span', class_ = 'srp-skills').text.replace(' ','')
                s = skills.split()
                skill_list = s[0].split(",")
                for i in skill_list:
                    final.append(i)
                
        d = dict(Counter(final))
        d= sorted(d.items(), key =lambda kv:(kv[1], kv[0]))
        d.reverse()
        for i in range(20):
            skills_name.append(d[i][0])
            frequencies.append(d[i][1])
        print()
        plt.bar(skills_name, frequencies, color ='maroon',width = 0.5)
        plt.xticks(rotation = 90)
        plt.title("The top 20 skills")
        
        plt.show()

        #getting the text files containing the data
        print('put some skill that you are not familiar with')
        unfamiliar_skills  = input('>').split()
        print(f'Filtering out {unfamiliar_skills}')
        for j, i in enumerate(url_list):
                html_text = requests.get(i).text
                soup = BeautifulSoup(html_text, 'lxml')
                jobs = soup.find_all('li', class_ = 'clearfix job-bx wht-shd-bx' )
                print("the number of jobs scraped from this  webpage is ",len(jobs))
                for index,job in enumerate(jobs):
                    flag =0
                    published_date = job.find('span', class_ = 'sim-posted').span.text.replace(' ','')
                    if 'few' in published_date:
                        company_name = job.find('h3', class_ = 'joblist-comp-name').text.replace(' ','')
                        skills = job.find('span', class_ = 'srp-skills').text.replace(' ','')
                        more_info =job.header.h2.a['href']
                        s=skills.split()
                        d=s[0].split(",")
                        for i in d:
                            if i in unfamiliar_skills:
                                flag=1
                                break
                            else:
                                continue
                        if(flag):
                                continue
                        else:
                            with open(f'posts/{unfamiliar_skills,j}.txt', 'a') as f:
                                f.write(f"company name: {company_name.strip()}\n")
                                f.write(f"required skills: {skills.strip()}\n")

                                f.write(f"More info:{more_info}\n\n\n\n")
                            print(f'File saved ')
        

    if(job_choosen == 'application developer'):
        print("the job you choosed is ",job_choosen)
        html = requests.get('https://www.timesjobs.com/candidate/job-search.html?searchType=personalizedSearch&from=submit&txtKeywords=Application+Developer&txtLocation=').text
        values =getting_values(html)
        print("The number of jobs that has the required job is",values)
        skill_list =[]
        final = []
        page_number =[]
        url_list =[]
        frequencies =[]
        skills_name = []
        no_of_pages = int(values)//25+1
        if(no_of_pages<20):
            for i in range(1,no_of_pages+1):
                page_number.append(i)
        else:
            page_number = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20]
        for i in page_number:
            url_list.append(f'https://www.timesjobs.com/candidate/job-search.html?from=submit&actualTxtKeywords=Application%20Developer&searchBy=0&rdoOperator=OR&searchType=personalizedSearch&txtLocation=india&luceneResultSize=25&postWeek=60&txtKeywords=0DQT0application%20developer0DQT0&cboWorkExp1=0&pDate=I&sequence={i}&startPage=1')
        getting_job_data(url_list)
                        
    elif(job_choosen =='front end developer'):
        print("the job you choosed is ",job_choosen)
        html2 = requests.get('https://www.timesjobs.com/candidate/job-search.html?searchType=personalizedSearch&from=submit&txtKeywords=Front+End+Developer&txtLocation=').text
        values =getting_values(html2)
        print("the number of jobs that the required job has",values)
        
        skill_list =[]
        final = []
        page_number =[]
        url_list =[]
        frequencies =[]
        skills_name = []
        no_of_pages = int(values)//25+1
        if(no_of_pages<20):
            for i in range(1,no_of_pages+1):
                page_number.append(i)
        else:
            page_number = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20]
        for i in page_number:
            url_list.append(f'https://www.timesjobs.com/candidate/job-search.html?from=submit&actualTxtKeywords=Front%20End%20Developer&searchBy=0&rdoOperator=OR&searchType=personalizedSearch&luceneResultSize=25&postWeek=60&txtKeywords=0DQT0front%20end%20developer0DQT0&pDate=I&sequence={i}&startPage=1')
        getting_job_data(url_list)

    elif(job_choosen == 'back end developer'):
        print("the job you choosed is ",job_choosen)
        html3 = requests.get('https://www.timesjobs.com/candidate/job-search.html?searchType=personalizedSearch&from=submit&txtKeywords=back+end+developer&txtLocation=').text
        values = getting_values(html3)
        print("the number of jobs that the required job has",(html3))
        
        
        skill_list =[]
        final = []
        page_number =[]
        url_list =[]
        frequencies =[]
        skills_name = []
        no_of_pages = int(values)//25+1
        if(no_of_pages<20):
            for i in range(1,no_of_pages+1):
                page_number.append(i)
        else:
            page_number = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20]
        for i in page_number:
            url_list.append(f'https://www.timesjobs.com/candidate/job-search.html?from=submit&actualTxtKeywords=back%20end%20developer&searchBy=0&rdoOperator=OR&searchType=personalizedSearch&txtLocation=india&luceneResultSize=25&postWeek=60&txtKeywords=back%20end%20developer&cboWorkExp1=0&pDate=I&sequence={i}&startPage=1')
        getting_job_data(url_list)

    elif(job_choosen == 'data scientist'):
        print("the job you choosed is ",job_choosen)
        html4 = requests.get('https://www.timesjobs.com/candidate/job-search.html?searchType=personalizedSearch&from=submit&txtKeywords=data+scientist&txtLocation=').text
        values = getting_values(html4)
        print("the number of jobs that the required job has",values)

        
        skill_list =[]
        final = []
        page_number =[]
        url_list =[]
        frequencies =[]
        skills_name = []
        no_of_pages = int(values)//25+1
        if(no_of_pages<20):
            for i in range(1,no_of_pages+1):
                page_number.append(i)
        else:
            page_number = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20]
        for i in page_number:
            url_list.append(f'https://www.timesjobs.com/candidate/job-search.html?from=submit&actualTxtKeywords=Data%20Scientist&searchBy=0&rdoOperator=OR&searchType=personalizedSearch&txtLocation=india&luceneResultSize=25&postWeek=60&txtKeywords=data%20scientist&cboWorkExp1=0&pDate=I&sequence={i}&startPage=1')
        getting_job_data(url_list)

    elif(job_choosen =='game developer'):
        print("the job you choosed is ",job_choosen)
        html5 = requests.get('https://www.timesjobs.com/candidate/job-search.html?searchType=personalizedSearch&from=submit&txtKeywords=Game+Developer&txtLocation=').text
        values  =getting_values(html5)
        print("the number of jobs that the required job has",values)
        
        skill_list =[]
        final = []
        page_number =[]
        url_list =[]
        frequencies =[]
        skills_name = []
        no_of_pages = int(values)//25+1
        if(no_of_pages<20):
            for i in range(1,no_of_pages+1):
                page_number.append(i)
        else:
            page_number = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20]
        for i in page_number:
            url_list.append(f'https://www.timesjobs.com/candidate/job-search.html?from=submit&actualTxtKeywords=Game%20Developer&searchBy=0&rdoOperator=OR&searchType=personalizedSearch&luceneResultSize=25&postWeek=60&txtKeywords=0DQT0game%20developer0DQT0&pDate=I&sequence={i}&startPage=1')
        getting_job_data(url_list)

    elif(job_choosen =='quality analyst'):
        print("the job you choosed is ",job_choosen)
        html6 = requests.get('https://www.timesjobs.com/candidate/job-search.html?searchType=personalizedSearch&from=submit&txtKeywords=Quality+Analyst&txtLocation=').text
        values = getting_values(html6)
        print("the number of jobs that the required job has",values)
        
        skill_list =[]
        final = []
        page_number =[]
        url_list =[]
        frequencies =[]
        skills_name = []
        no_of_pages = int(values)//25+1
        if(no_of_pages<20):
            for i in range(1,no_of_pages+1):
                page_number.append(i)
        else:
            page_number = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20]
        for i in page_number:
            url_list.append(f'https://www.timesjobs.com/candidate/job-search.html?from=submit&actualTxtKeywords=Quality%20Analyst&searchBy=0&rdoOperator=OR&searchType=personalizedSearch&txtLocation=india&luceneResultSize=25&postWeek=60&txtKeywords=0DQT0quality%20analyst0DQT0&cboWorkExp1=0&pDate=I&sequence={i}&startPage=1')
        getting_job_data(url_list)

    elif(job_choosen == 'full stack engineer'):
        print("the job you choosed is ",job_choosen)
        html8 = requests.get('https://www.timesjobs.com/candidate/job-search.html?searchType=personalizedSearch&from=submit&txtKeywords=full+stack+engineer&txtLocation=').text
        values = getting_values(html8)
        print("the number of jobs that the required job has",values)
        
        skill_list =[]
        final = []
        page_number =[]
        url_list =[]
        frequencies =[]
        skills_name = []
        no_of_pages = int(values)//25+1
        if(no_of_pages<20):
            for i in range(1,no_of_pages+1):
                page_number.append(i)
        else:
            page_number = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20]
        for i in page_number:
            url_list.append(f'https://www.timesjobs.com/candidate/job-search.html?from=submit&actualTxtKeywords=full%20stack%20engineer&searchBy=0&rdoOperator=OR&searchType=personalizedSearch&txtLocation=india&luceneResultSize=25&postWeek=60&txtKeywords=full%20stack%20engineer&cboWorkExp1=0&pDate=I&sequence={i}&startPage=1')
        getting_job_data(url_list)

    elif(job_choosen =='cloud engineer'):
        print("the job you choosed is ",job_choosen)
        html10 = requests.get('https://www.timesjobs.com/candidate/job-search.html?searchType=personalizedSearch&from=submit&txtKeywords=cloud+engineer&txtLocation=').text
        values =getting_values(html10)
        print("the number of jobs that the required job has",values)
        skill_list =[]
        final = []
        page_number =[]
        url_list =[]
        frequencies =[]
        skills_name = []
        no_of_pages = int(values)//25+1
        if(no_of_pages<20):
            for i in range(1,no_of_pages+1):
                page_number.append(i)
        else:
            page_number = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20]
        for i in page_number:
            url_list.append(f'https://www.timesjobs.com/candidate/job-search.html?from=submit&actualTxtKeywords=cloud%20engineer&searchBy=0&rdoOperator=OR&searchType=personalizedSearch&txtLocation=india&luceneResultSize=25&postWeek=60&txtKeywords=cloud%20engineer&cboWorkExp1=0&pDate=I&sequence={i}&startPage=1')
        getting_job_data(url_list)


chart()
