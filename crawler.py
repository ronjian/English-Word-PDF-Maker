from bs4 import BeautifulSoup
import urllib2
import os
import json
from PIL import Image
import sys

def load_words(file_name):
    with open(file_name,'rb') as f:
        tmp = f.readlines()
        words = []
        for t in tmp:
            # strip '\n' -> lowercase -> split space
            for word in t.strip().lower().split(' '):
                words.append(word)
    words = set(words)
    print("there are total {} words".format(len(words)))
    return words

if __name__ == "__main__":
    if len(sys.argv) ==2 :
        file_name = sys.argv[1]
        words = load_words(file_name)
        err_cnt = 0
        DIR = file_name.split('.')[0] + '_images'
        if not os.path.exists(DIR):
            os.mkdir(DIR)
        for query in words:
            subDIR = os.path.join(DIR, query)
            if not os.path.exists(subDIR):
                os.mkdir(subDIR)
                count = 2
                image_type="ActiOn"
                url="https://www.google.com/search?q="+query+"&source=lnms&tbm=isch"
                print(url)
                header={'User-Agent':"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36"
                }
                soup = BeautifulSoup(urllib2.urlopen(urllib2.Request(url,headers=header)),'html.parser')
                ActualImages=[]# contains the link for Large original images, type of  image
                for a in soup.find_all("div",{"class":"rg_meta"})[:count]:
                    link , Type =json.loads(a.text)["ou"]  ,json.loads(a.text)["ity"]
                    ActualImages.append((link,Type))
                for i , (img , Type) in enumerate(ActualImages):
                    try:
                        req = urllib2.Request(img, headers={'User-Agent' : header})
                        raw_img = urllib2.urlopen(req, timeout=180).read()
                        if len(Type)==0:
                            path = os.path.join(subDIR , image_type + "_"+ str(i + 1)+".jpg")
                        else :
                            path = os.path.join(subDIR , image_type + "_"+ str(i + 1)+"."+Type)
                        with open(path, 'wb') as f:
                            f.write(raw_img)
                        # compression
                        pic = Image.open(path)
                        w, h = pic.size
                        n_h = 100
                        n_w = int(round(float(n_h) / float(h) * float(w)))
                        pic = pic.resize((n_w, n_h), Image.ANTIALIAS)
                        pic.save(path, optimize=True, quality=95)
                    except Exception as e:
                        print("could not load : "+img)
                        print(str(e))
                        err_cnt += 1

        print('{} errors happened when crawling pitcutres.'.format(err_cnt))
    else:
        print('Please kick off this as: python2 crawler.py sample_words.txt')
