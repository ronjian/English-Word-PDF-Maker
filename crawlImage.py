from bs4 import BeautifulSoup
import urllib2
import os
import json
from PIL import Image
import sys

def get_soup(url,header):
    return BeautifulSoup(urllib2.urlopen(urllib2.Request(url,headers=header)),'html.parser')

#reading flat file
if len(sys.argv) ==2 :
    file_name = sys.argv[1]
    input = open(file_name,'rb')
    words = input.readlines()
    err_cnt = 0
    DIR = file_name+'Image'
    if not os.path.exists(DIR):
        os.mkdir(DIR)
    for query in words[:]:
        # query = raw_input("please search here:")# you can change the query for the image  here
        #count = int(raw_input("please input image count:"))
        count = 2
        image_type="ActiOn"
        query= query.replace('\n', '').split()
        query='+'.join(query)
        url="https://www.google.com/search?q="+query+"&source=lnms&tbm=isch"
        print url
        #add the directory for your image here
        #DIR="Pictures"

        header={'User-Agent':"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36"
        }
        soup = get_soup(url,header)

        ActualImages=[]# contains the link for Large original images, type of  image
        for a in soup.find_all("div",{"class":"rg_meta"})[:count]:
            link , Type =json.loads(a.text)["ou"]  ,json.loads(a.text)["ity"]
            ActualImages.append((link,Type))

        print  "there are total" , len(ActualImages),"images"

        subDIR = os.path.join(DIR, query.split()[0])

        if not os.path.exists(subDIR):
                    os.mkdir(subDIR)
        ###print images
        for i , (img , Type) in enumerate( ActualImages):
            try:
                req = urllib2.Request(img, headers={'User-Agent' : header})
                raw_img = urllib2.urlopen(req, timeout=180).read()

                cntr = len([i for i in os.listdir(subDIR) if i in i]) + 1
                print cntr
                if len(Type)==0:
                    path = os.path.join(subDIR , image_type + "_"+ str(cntr)+".jpg")
                    f = open(path, 'wb')
                else :
                    path = os.path.join(subDIR , image_type + "_"+ str(cntr)+"."+Type)
                    f = open(path, 'wb')


                f.write(raw_img)
                f.close()

                # compression
                pic = Image.open(path)
                w, h = pic.size
                n_h = 100
                n_w = int(round(float(n_h) / float(h) * float(w)))
                pic = pic.resize((n_w, n_h), Image.ANTIALIAS)
                pic.save(path, optimize=True, quality=95)

            except Exception as e:
                print "could not load : "+img
                print e
                err_cnt += 1

    input.close()

    print(str(err_cnt),'errors happened when crawling pitcutres.')
else:
    print('Please kick off this as: "python crawlImage.py myword.txt"')
