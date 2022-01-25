from flask import Flask, render_template,request
from bs4 import BeautifulSoup
import requests
table=[]
app = Flask(__name__)   
def find_url(q,l):
    site='https://in.indeed.com/jobs?q={}&l={}'
    url=site.format(q,l)
    return url

def details(link):
    return BeautifulSoup(requests.get(link).text, 'html.parser').find('div','jobsearch-jobDescriptionText').text

def get_all(cells,skills):
    for c in range(10):
        cell=cells[c]
        title= cell.find('h2',{'class': 'jobTitle'}).text
        title=title.replace("new","")
        try:
            company=cell.find('span','companyName').text
        except AttributeError:
            company=''
        try:
            location=cell.find('div','companyLocation').text
        except AttributeError:
            location=''
        loc=''
        for i in location:
            if(i=='•' or i==','):
                break
            else:
                loc=loc+i
        try:
            salary= cell.find('div','metadata salary-snippet-container').text
        except AttributeError:
            salary=''
        link='https://in.indeed.com'+cell.get('href')
        try:
            detail=details(link)
        except AttributeError:
            detail=''
        skil=''
        for j in skills:
            if detail.lower().find(j.lower())!=-1:
                if len(skil):
                    skil=skil+','+j
                else:
                    skil=j
        if(len(detail)!=0):
            if (len(skil)!=0 ):
                table.append([title,company,loc,salary,skil,link])
        else:
            table.append([title,company,loc,salary,skil,link])
def search(q,l,skills):
    url=find_url(q,l)
    while True:
        request=requests.get(url)
        soup=BeautifulSoup(request.text, 'html.parser')
        cells= soup.find_all('a',{'class': 'tapItem'})
        get_all(cells,skills)
        if len(table)>8:
            break
        try:
            url='https://in.indeed.com'+soup.find('a', {'aria-label': 'Next'}).get('href')
        except AttributeError:
            break

@app.route('/', methods=['GET', 'POST'])
def hello_world():
    if request.method=='POST':
        table.clear()
        Domain = request.form['Domain']
        Location = request.form['Location']
        Skills= request.form['Skills']
        s=Skills.replace(' ','')
        skills=s.split(',')
        search(Domain,Location,skills)
    return render_template('index.html', table=table)
if __name__ == '__main__':
   app.run(debug=False,port=8000)