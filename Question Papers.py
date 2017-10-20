print ("Importing modules... please wait...")
import requests as req
from bs4 import BeautifulSoup as bs
import urllib.request as urlr
import os, time

def getCampus(campusNo):
    campi = {
        '1': 'VSP',
        '2': 'HYD',
        '3': 'BLR'
    }
    return campi[campusNo]

def getCollege(collegeNo):
    colleges = {
        '1': 'GIT',
        '2': 'GSA',
        '3': 'GSP',
        '4': 'GSS',
        '5': 'HBS',
        '6': 'SA'
    }
    return colleges[collegeNo]
    
def getBranchName(branchNo):
    branches = {
        '01': 'BIOTECH',
        '02': 'CIVIL',
        '03': 'CSE',
        '04': 'EC-5',
        '05': 'EC-6',
        '06': 'ECE',
        '07': 'EEE',
        '08': 'EIE',
        '09': 'IE',
        '10': 'IT',
        '11': 'MC-5',
        '12': 'MC-6',
        '13': 'MECH'
    }
    return branches[branchNo]
  
def getStudentDetails(rollNo, sem, year):

    """
    Takes a roll number and returns a dict
    having details like the campus,
    year of joining, branch, etc.

    0        1         2         34 56 
    1        2         1         03 14 XXX
    Campus   Student   College   Br Yr
    """

    campus = getCampus(rollNo[0:1])
    college = getCollege(rollNo[2:3])
    branch = getBranchName(rollNo[3:5])

    det = {
        'ddlcampus': campus,
        'ddlcollege': college,
        'ddldegree': 'UG',
        'ddlbranch': branch,
        'ddlyear': str((1+int(sem))//2),
        'ddlacyear': str(year),
        'ddlsem': sem
    }
    return det

def downloadPapers(papers, dirName="QuestionPapers"):

    """
    Downlaods the actual question
    papers using the paper links
    passed as the 'papers' dictionary
    of the form {title: link}.

    dirName is the fully qualified path
    where the papers will be saved.
    """
    
    for subject in papers:
        file = subject
        if '.pdf' not in file:
            file += '.pdf'
        a = urlr.urlretrieve(papers[subject], filename=file)
        print ("Downloaded : " + subject)    
    
def getQuestionPaperLinks(studentData):

    """
    Returns a dict {title:link}
    where title is the subject name
    and the link is the link for the
    question paper.
    """

    # Link for every question paper
    link = "http://krc.gitam.edu/papers"

    # POST Request the link with the student
    # data in the headers
    raw = req.post(link, data=studentData)

    # Check if POST was successfull
    if raw.status_code != 200:
        print ('Failed :', raw.reason)
        
    # If it was, parse the response html using
    # BeautifulSoup
    code = bs(raw.text, 'html.parser')

    # We want every element of the form
    # .papers.lst
    elements = code.find(class_ = 'papers').findChildren(class_ = 'lst')

    # Each element has a link and the title for
    # that linkm both enclosed in div blocks.
    papers = dict()
    for eachElement in elements:
        divs = eachElement.findAll('div')
        title = divs[1].text
        link = "http://krc.gitam.edu" + divs[2].find('a').attrs['href']

        # Add these to the papers dict
        papers[title] = link

    # Return the question paper links
    return papers
    
# Some default data...
defaultFolder = "AllQuestionPapers"
depth = 1  # How many years back should the program start looking for papers

try:
    rollNo = input('Enter your roll number : ')
    sem = input('Enter your semester : ')
    path = input('Where should I save theses papers ? (Eg-C:/Users/Name/Desktop) : ')
    

    # Point to the place where the papers
    # have to be saved. (Check for MAC Users)
    try:
        path += "/" + defaultFolder + "/"
        os.makedirs(path)
        os.chdir(path)
    except:
        print ("Folder already exists!")
        exit(0)

    # We need papers of each academic year
    currentYear = time.localtime().tm_year
    
    for year in range(currentYear - depth, currentYear+1):
        studentDetails = getStudentDetails(rollNo, sem, year)
        papers = getQuestionPaperLinks(studentDetails)
        downloadPapers(papers, path)

    print ("\nDone! Thanks for using ... ☮ADK ... Happy Studying")
    
except Exception as e:
    print ("Failed :", e)
    
