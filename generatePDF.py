from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import sys
import os
import re
from reportlab.lib.utils import ImageReader



def read_annotation(trans_file):
    word = None
    annotation_f = open(trans_file, 'rb')
    lines = annotation_f.readlines()
    dictionary = {}
    for x in lines:
        if x == '----------------------\n':
            word = None
            continue

        if word == None:
            word = x.replace(':', '').replace('\n', '')
            dictionary[word] = x
        else:
            dictionary[word] += x

    annotation_f.close()

    return dictionary



if len(sys.argv) ==2 :
    file_name = sys.argv[1]
    trans_file = file_name+'.dictionary'
    dictionary = read_annotation(trans_file)

    input = open(file_name,'rb')
    words = input.readlines()

    pdf_file = file_name+'.pdf'
    c = canvas.Canvas(pdf_file,pagesize=letter)
    width, height = letter
    y = height - 20
    err_cnt=0
    for word in words[:]:
        try:
            #add a new page
            if y <= 235:
                c.showPage()
                y = height - 20

            word = word.replace('\n','')
            c.drawString(20,y,word)
            c.textAnnotation(dictionary[word], Rect=[100, y+10, 100, y+10], relative=1)
            y -= 15

            # img = query_img(word)
            folder="./"+file_name+"/"+word+"/"
            pic_re1 = re.compile(r"ActiOn_1.*")
            pic_path1 = filter(pic_re1.match, os.listdir(folder))
            pic1 = ImageReader(folder + pic_path1[0])
            w1 , h1 = pic1.getSize()
            y -= 115
            width1 = int(round( float(100) / float(h1) * float(w1)))
            c.drawImage(pic1 ,x=1 , y=y+15
                        ,width = width1
                        ,height=100,mask='auto')

            pic_re2 = re.compile(r"ActiOn_2.*")
            pic_path2 = filter(pic_re2.match, os.listdir(folder))
            pic2 = ImageReader(folder + pic_path2[0])
            w2 , h2 = pic2.getSize()
            width2 = int(round(float(100) / float(h2) * float(w2)))
            c.drawImage(pic2 ,x=width1+10 , y=y+15
                        ,width =width2
                        ,height=100,mask='auto')

            print(word + 'is drew')

        except Exception as e:
            print word + " failed"
            print e
            err_cnt += 1

    c.save()
    input.close()
    print(pdf_file,"generated!")
else:
    print('Please kick off this as: "python generatePDF.py myword.txt"')


