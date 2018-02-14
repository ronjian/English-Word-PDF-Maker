from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import sys
import os
import re
from reportlab.lib.utils import ImageReader
from crawler import load_words

def read_annotation(trans_file):
    word = None
    with open(trans_file, 'rb') as annotation_f:
        lines = annotation_f.readlines()
        dictionary = {}
        for x in lines:
            x = x.strip()
            if x == '----------------------':
                word = None
                continue
            if word == None:
                word = x.replace(':', '')
                dictionary[word] = x
            else:
                dictionary[word] += '\n' + x
    return dictionary

if __name__ == "__main__":
    if len(sys.argv) ==2 :
        file_name = sys.argv[1]
        file_name_wo_postfix = file_name.split('.')[0]
        trans_file = file_name_wo_postfix +'.dictionary'
        dictionary = read_annotation(trans_file)
        words = load_words(file_name)
        pdf_file = file_name_wo_postfix + '.pdf'

        c = canvas.Canvas(pdf_file,pagesize=letter)
        c.setFont("Times-Roman", 25, leading = None)
        width, height = letter
        y = height - 25
        err_cnt=0
        for word in words:
            try:
                #add a new page
                if y <= 235:
                    c.showPage()
                    c.setFont("Times-Roman", 25, leading = None)
                    y = height - 20

                c.drawString(20,y,word)
                c.textAnnotation(dictionary[word], Rect=[200, y+10, 200, y+10], relative=1)
                y -= 15

                folder="./"+ file_name_wo_postfix +"_images/"+word+"/"
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
                print(word + ' is written')
            except Exception as e:
                print(word + " failed")
                print(str(e))
                err_cnt += 1
        c.save()
        print(pdf_file + " generated!")
    else:
        print("Please kick off this as: python2 writer.py sample_words.txt")


