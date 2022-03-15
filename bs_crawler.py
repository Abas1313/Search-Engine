# -*- coding: utf-8 -*-
"""
Created on Thu Apr  8 19:22:52 2021

@author: abasd
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
%matplotlib inline
import re
import time
from datetime import datetime
import matplotlib.dates as mdates
import matplotlib.ticker as ticker
from urllib.request import urlopen
from bs4 import BeautifulSoup
import requests

headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0",
           "Accept-Encoding":"gzip, deflate", "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
           "DNT":"1","Connection":"close", "Upgrade-Insecure-Requests":"1"}

## request  and open the main link 

R = requests.get('https://scholar.google.co.uk/citations?view_op=view_org&hl=en&org=9117984065169182779')
base_link = 'https://scholar.google.co.uk'
content =R.content
soup = BeautifulSoup(content,'html.parser')

#==================================================================================

next_url = "https://scholar.google.com/citations?view_op=view_org&hl=en&org=9117984065169182779"
max_pages = 1
page = 0
# Lists to store the scraped data in
Profile_name = []
Co_Authors = []
Title = []
descriptions_links = []
description = []
journal_name =[]
publication_date = [] 
Authors_link = []
publisher = []
volume = []
Total_citation = []
Pages = []
data={}
df=pd.DataFrame(columns=['Title','Co_Authors','Title','descriptions_links','description','publisher'])
while True:
    page += 1
 
    webpage = requests.get(next_url, headers = headers)
    soup = BeautifulSoup(webpage.content, 'html.parser')
    authors = soup.find_all('h3', class_='gs_ai_name')
 
    for author in authors:
    #author = author.text
        Profile_name.append(author.text)
    # print("============== FOR AUTHOR ", author.text, " =================")

        author_url = base_link + author.find('a')['href']
        print(author_url)

        Authors_link.append(author_url)
        print(author_url, end='\n')
        time.sleep(3)
        
        
        # For each author go to profile
        
        webpage_author = requests.get(author_url,headers=headers )
        soup_author = BeautifulSoup(webpage_author.content, 'html.parser')
        papers = soup_author.find_all('tr', class_='gsc_a_tr')
        for paper in papers:
            title = paper.find("td", class_ = "gsc_a_t")
            Title.append(title)

            
            description_link = base_link + title.find("a")["data-href"]
            descriptions_links.append(description_link)
            time.sleep(3)

              # For each paper go to description
            webpage_description = requests.get(description_link)
            
            soup_description = BeautifulSoup(webpage_description.content, 'lxml')
            fields = soup_description.find_all("div", class_ = "gsc_vcd_field")
            values = soup_description.find_all("div", class_ = "gsc_vcd_value")

            print("----")

            for field, value in zip(fields, values):
                if  field.text == 'Authors':
                    Co_Authors.append(value.text)
                elif field.text == 'Publication date':
                    publication_date.append(value.text)
                    print(publication_date)
            #print(publication_date)
                elif field.text == 'Journal':
                     journal_name.append(value.text)
                
                    #print(Pages)
                elif field.text == 'Pages':
                     Pages.append(value.text)
                        #print(Pages)
                elif field.text == 'Publisher':
                     publisher.append(value.text)
                #print(description)
                elif field.text == 'Total citations':
                     Total_citation.append(value.text)
                #print(Total_citation)
                elif field.text == 'description':
                     description.append(value.text)
                #print('desc===',description)



  # getting next page

    next_page =  soup.find('button', class_ = "gs_btnPR gs_in_ib gs_btn_half gs_btn_lsb gs_btn_srt gsc_pgn_pnx")["onclick"]
    print(next_page)
    try:
        next_url = base_url + next_page[17:-1].replace("\\x26","&").replace("\\x3d", "=")
        print(next_url)
    except:
        print("END")
        break
 
    if page == max_pages:
        break


# ===========================================

next_url = "https://scholar.google.com/citations?view_op=view_org&hl=en&org=9117984065169182779"

def level_1(level_0_data):
    data1={}
    start = 1
    level_1_data=pd.DataFrame(columns=['paper_title','paper_link'])
    counter = 0
    for i in range(0,5):
        ##len(level_0_data['Profile_link']
        while True:       
            Author_page = requests.get(level_0_data['Profile_link'][i] + "&pagesize=100" + "&cstart=" + str(start*100),headers=headers )

            Author_page_soup = BeautifulSoup(Author_page.content, 'html.parser')
            papers = Author_page_soup.find_all('tr', class_='gsc_a_tr')
            time.sleep(1)

            for paper in papers:
                data1['paper_title']= paper.find("a", class_ = "gsc_a_at").text ## get paper title
                data1['paper_link'] = base_link + paper.find("a")["data-href"]  # get paper link
                print(data1['paper_title'])
                print(data1['paper_link'])
                #descriptions_links.append(description_link)
                level_1_data = level_1_data.append(data1, ignore_index=True)
                counter += 1
            start += 1
            
            if Author_page_soup.find("button",id="gsc_bpf_more").has_attr("disabled"):
                break
            
        start = 0
            
    return level_1_data

level_0_data = level_0(next_url,base_link)
level_0_data.to_csv("C:/Users/abasd/OneDrive - Coventry University/Masters/Information retrieval/level_0.csv")
level_0_data = pd.read_csv("C:/Users/abasd/OneDrive - Coventry University/Masters/Information retrieval/level_0.csv")


#======================================================================
next_url = "https://scholar.google.com/citations?view_op=view_org&hl=en&org=9117984065169182779"

def level_1(level_0_data):
    data1={}
    start = 1
    level_1_data=pd.DataFrame(columns=['paper_title','paper_link'])
    counter = 0
    for i in range(0,5):
        ##len(level_0_data['Profile_link']
        while True:       
            Author_page = requests.get(level_0_data['Profile_link'][i] + "&pagesize=100" + "&cstart=" + str(start*100),headers=headers )

            Author_page_soup = BeautifulSoup(Author_page.content, 'html.parser')
            papers = Author_page_soup.find_all('tr', class_='gsc_a_tr')
            time.sleep(1)

            for paper in papers:
                data1['paper_title']= paper.find("a", class_ = "gsc_a_at").text ## get paper title
                data1['paper_link'] = base_link + paper.find("a")["data-href"]  # get paper link
                print(data1['paper_title'])
                print(data1['paper_link'])
                #descriptions_links.append(description_link)
                level_1_data = level_1_data.append(data1, ignore_index=True)
                counter += 1
            start += 1
            
            if Author_page_soup.find("button",id="gsc_bpf_more").has_attr("disabled"):
                break
            
        start = 0
            
    return level_1_data


level_1_data.to_csv("C:/Users/abasd/OneDrive - Coventry University/Masters/Information retrieval/level_1.csv")

#=====================================================================


def level_2(level_1_data):
    data2={}
    level_2_data=pd.DataFrame(columns=['Authors','publication_date','Journal','pages_number','Publisher','Total_citation','description'])
    counter = 0
    for i in range(0,2):
        
          
            paper_page_link = requests.get(level_1_data['paper_link'][i],headers=headers )
            paper_description_soup = BeautifulSoup(paper_page_link.content, 'lxml')
            fields = paper_description_soup.find_all("div", class_ = "gsc_vcd_field")
            values = paper_description_soup.find_all("div", class_ = "gsc_vcd_value")
            print(level_1_data['paper_link'][i])
            time.sleep(1)

            for field, value in zip(fields, values):
                if  field.text == 'Authors':
                    data2['Authors'] = value.text
                    print('Authors====',Authors)
                    #Co_Authors.append(value.text)
                elif field.text == 'Publication date':
                    data2['publication_date'] = value.text
                    print('publication_date====',publication_date)
                    #publication_date.append(value.text)
                    print(publication_date)
            #print(publication_date)
                elif field.text == 'Journal':
                    data2['Journal'] = value.text
                    print('Journal====')
                    #print(data2['Journal'])
                     #journal_name.append(value.text)
                
                elif field.text == 'Pages':
                    data2['pages_number'] = value.text
                    print('pages_number====')
                    #print(pages_number)
                    
                     #Pages.append(value.text)
                        #print(Pages)
                elif field.text == 'Publisher':
                    data2['Publisher'] = value.text
                    print('Publisher====')#
                    #print(Publisher)
                     #publisher.append(value.text)
                #print(description)
                elif field.text == 'Total citations':
                    data2['Total_citation'] = value.text
                    print('Total_citation====')
                    #print(Total_citation)
                     #Total_citation.append(value.text)
                #print(Total_citation)
                elif field.text == 'Description':
                    data2['Description'] = value.text
                    print('description====')
                    #print(description)
            level_2_data = level_2_data.append(data2, ignore_index=True)
                    
                     #description.append(value.text)
                #print('desc===',description)
    
            counter += 1       
    return level_2_data



