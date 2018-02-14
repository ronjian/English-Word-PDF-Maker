import urllib2 as request
from bs4 import BeautifulSoup
import sys

def crawl_annotation(word):
    try:
        headers = {'User-Agent':
                       'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/535.19\
                       (KHTML, like Gecko) Chrome/18.0.1025.168 Safari/535.19'}
        url = 'http://dict.youdao.com/w/' + word + '/#keyfrom=dict2.top'
        print(url)
        annotation = word + ':\n'
        req = request.Request(url=url,headers=headers)
        r = request.urlopen(req,timeout=120)
        html_txt = r.read().decode('utf-8')
        parsed_html = BeautifulSoup(html_txt, "html5lib")
        list = parsed_html.body.find_all('span', attrs={'class':'pronounce'}, limit=2)
        annotation += list[0].text.encode('utf-8','ignore').replace(' ','').replace('\n','') + ':\n'
        if len(list) == 2:
            annotation += list[1].text.encode('utf-8','ignore').replace(' ','').replace('\n','') + ':\n'
        annotation += parsed_html.body.find('div', attrs={'trans-container'}).text.encode('utf-8','ignore').replace(' ','').strip() + ':\n'
    except Exception as e:
        print(word + " failed")
        print(str(e))
    finally:
        return annotation
        
if __name__ == "__main__":
    if len(sys.argv) ==2 :
        file_name = sys.argv[1]
        with open(file_name,'rb') as f:
            tmp = f.readlines()
            words = []
            for t in tmp:
                # strip '\n' -> lowercase -> split space
                for word in t.strip().lower().split(' '):
                    words.append(word)
        print("there are total {} words to be crawler".format(len(words)))
        output_file = file_name.split('.')[0]+'.dictionary'
        with open(output_file,'wb') as f:
            for word in words:
                f.write('----------------------\n')
                f.write(crawl_annotation(word) )
    else:
        print("Please kick off this as: python2 translator.py sample_words.txt")