import pathlib
import pandas
import requests 
from bs4 import BeautifulSoup 
import re
import os
  

''' 
URL of the archive web-page which provides link to 
all video lectures. It would have been tiring to 
download each video manually. 
In this example, we first crawl the webpage to extract 
all the links and then download videos. 
'''
  

def get_sheet_links_names(year=2019): 
    #specify the URL of the archive here 
    archive_url = f"https://www.gov.pl/web/finanse/udzialy-za-{year}-r"
    data_url = "https://www.gov.pl"
      
    # create response object 
    r = requests.get(archive_url) 
      
    # create beautiful-soup object 
    soup = BeautifulSoup(r.content,'html5lib') 
      
    # find all links on web-page 
    links = soup.findAll('a') 
  
    # filter the names for our .xlsx files
    names = []
    for link in links:
        try:
            names.append(link['aria-label'])
        except:
#             This exception is necessaty as most of the links don't have this key
            continue
        
    sheet_links = [data_url + link[r'href'] for link in links]
    
    sheet_links = re.findall("https://www.gov.pl/attachment/.{36}", " ".join(sheet_links))
    
    names = re.findall("[0-9].+\.xlsx", " ".join(names))
  
    return sheet_links, names



def download_sheet_series(sheets): 
  
    for link, file_name in zip(sheets[0], sheets[1]): 
  
        '''iterate through all links in sheets 
        and download them one by one'''
          
  
        print( "Downloading file: %s"%file_name) 
          
        # create response object 
        r = requests.get(link, stream = True) 
        
        filename = f"./data/"
        if not os.path.exists(os.path.dirname(filename)):
            try:
                os.mkdir(os.path.dirname(filename))
            except OSError as exc:  # Guard against race condition
                if exc.errno != errno.EEXIST:
                    raise
          
        # download started 
        with open(f"./data/{file_name}", 'wb') as output:
            output.write(r.content)
            
        p = pathlib.Path(filename)
        p = p.resolve()
        print(p.joinpath(file_name).parent)
          
        print( "%s downloaded!\n"%file_name )
  
    print ("All sheets downloaded!")
    return

if __name__ == '__main__':
#     Zbieramy ze strony wsztstkie linki do arkuszy i ich nazwy
    sheets = get_sheet_links_names() 

    download_sheet_series(sheets)