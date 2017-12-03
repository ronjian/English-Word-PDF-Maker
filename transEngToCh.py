import urllib2 as request
from bs4 import BeautifulSoup

def crawl_annotation(word):
    try:
        headers = {'User-Agent':
                       'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/535.19\
                       (KHTML, like Gecko) Chrome/18.0.1025.168 Safari/535.19'}
        url = 'http://dict.youdao.com/w/' + word + '/#keyfrom=dict2.top'
        print url
        req = request.Request(url=url,headers=headers)
        r = request.urlopen(req,timeout=120)
        html_txt = r.read().decode('utf-8')
        parsed_html = BeautifulSoup(html_txt, "html5lib")
        list = parsed_html.body.find_all('span', attrs={'class':'pronounce'}, limit=2)

        annotation = word + ':\n'
        annotation += list[0].text.encode('utf-8','ignore').replace(' ','').replace('\n','') + ':\n'
        if len(list) == 2:
            annotation += list[1].text.encode('utf-8','ignore').replace(' ','').replace('\n','') + ':\n'
        annotation += parsed_html.body.find('div', attrs={'trans-container'}).text.encode('utf-8','ignore').replace(' ','').strip() + ':\n'
        return annotation

    except Exception as e:
        print word + " failed"
        print e
        return annotation

import sys

if len(sys.argv) ==2 :
    file_name = sys.argv[1]
    input = open(file_name, 'rb')
    words = input.readlines()
    input.close()

    output_file = file_name+'.dictionary'
    output = open(output_file,'wb')
    for word in words[:]:
        word = word.replace('\n', '')
        output.write('----------------------\n')
        output.write( crawl_annotation(word) )
        print(word+' queried annotation')

    output.close()
else:
    print('Please kick off this as: "python transEngToCh.py myword.txt"')



    # word=None
    # annotation_f = open(output_file,'rb')
    # lines = annotation_f.readlines()
    # dictionary = {}
    # for x in lines:
    #     if x == '----------------------\n':
    #         word = None
    #         continue
    #
    #     if word == None :
    #         word = x.replace(':','').replace('\n','')
    #         dictionary[word] = x
    #     else:
    #         dictionary[word] += x
    #
    # annotation_f.close()
    #
    # print dictionary

