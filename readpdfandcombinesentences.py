# -*- coding: utf-8 -*-
"""
專題實驗 meeting作業 Final Version
資工三B
何冠緯
"""
import fitz # pymupdf(讀pdf的套件)
import re #用以同時刪除多種不同字元
#使用CKIP Chinese Parser進行小規模的句子剖析和斷詞測試(送HTTP request撈結果)
from ckippy import parse_tree

# 定義讀PDF文字並且將行與行之間的句子合併的函式
def readPDFandCombineSentences(pdf_document):
    doc = fitz.open(pdf_document) #將路經中的PDF讀入
    print("\nFile name:",pdf_document)
    print("Number of pages: %i" % doc.pageCount)
    #print(doc.metadata)

    for i in range(0,doc.pageCount): #一頁一頁讀
        page = doc.loadPage(i) #讀第i頁的文字
        pagetext = page.getText("text")
        if pagetext =="": #若此頁沒有文字，則跳到下一次迭代(讀下一頁)
            continue
        print("\npage",i+1,":")
        
        # block 1:句子合併處理前(做為對照用)
        print("[未處理]:")
        print(pagetext)
        
        # block 2:句子合併處理後
        print("[處理後]:")
        text_list = pagetext.split('\n') #用行分隔開
        combine_flag = False
        sentence_flag = False
        counter = 1
        line_text = "" #在迴圈外宣告，以提供跨迭代時使用
    
        for j in range(0,len( text_list ) ): #一行一行判斷&處理
            # part 1: 特殊情況處理
            #讀到最後一行且上一次迭代中前面的句子和此行合併後為句子S
            if combine_flag == True and j == len( text_list )-1:
                print('sentence',counter,':',line_text)            
                continue
            if combine_flag == False: #沒有和上一行合併句子，則直接讀入此行句子
                line_text = re.sub('[\uf0a7\uf0fc\uf0d8]', '', text_list[j]) #去除特定字元符號
            combine_flag = False #設回預設的False
            if line_text == "": #若此行為空字串，則跳過
                continue
            if len(line_text)== 1 : #若發現此行句子只有一個字，則可以直接印出句子
                print('sentence',counter,':',line_text)
                counter += 1
                continue
            if line_text[-1] == "。": #若發現句子結尾為句號，則表示句子結束，可以直接印出句子
                print('sentence',counter,':',line_text)
                counter += 1
                continue
            
            # part 2: 實際做句子剖析
            
            """
            # part 2-1: 目前此行的句子剖析
            parse = parse_tree(line_text) #做句子剖析
            print( 'text type:', parse )
            #用split把句子剖析系統的結果抓出來
            line_type = parse[0].split(' ', 1 )[1].split('(',1)[0] 
            print( 'text type:', line_type ) #將此行的句子剖析系統的結果印出
            """
            
            # part 2-2: 和下一行合併後的句子剖析
            if j != ( len( text_list )-1 ): #在不是最後一行的情況下，才可與下一行做合併
                nextline_text = re.sub('[\uf0a7\uf0fc\uf0d8]', '', text_list[j+1]) #讀取下一行的文字
                
                # condition 1: 特殊情況處理
                #若下一行為空字串或只有一個字元，則將目前此行印出後直接進到下一次迭代
                if (nextline_text == "") or (nextline_text[0]=="•") or ( len(nextline_text)== 1 ):
                    print('sentence',counter,':',line_text)
                    counter += 1
                    continue
                #若此行和下一行都有冒號，則將目前此行印出後直接進到下一次迭代
                if (line_text.find("：") >= 0 or line_text.find(":") >= 0) and (
                        nextline_text.find("：") >= 0 or nextline_text.find(":") >= 0):
                    print('sentence',counter,':',line_text)
                    counter += 1
                    continue
                #若此行有左括號且下一行有右括號，則直接將兩行合併進到下一次迭代
                if (line_text.find("(") >= 0 and line_text.find(")") == -1) and (
                        nextline_text.find(")") >= 0 and nextline_text.find("(") == -1):
                    combine_flag = True
                    #將合併的句子存入line_text以進到下一次的迭代判斷
                    line_text = line_text + nextline_text 
                    continue
                
                # condition 2: 正常情況合併句子做句子剖析
                combine_text = line_text + nextline_text #將此行文字和下一行合併            
                parse_combine = parse_tree(combine_text) #將合併後的文字做句子剖析
                #combine_type = parse_combine[0].split(' ', 1 )[1].split('(',1)[0]
                #print('combine text type:', combine_type )
                
                #此for迴圈用以應付含有英文或是較為複雜(parse陣列不只一個元素)的句子的判斷
                for k in range(0,len(parse_combine)):
                    #用split把句子剖析系統系統的結果抓出來
                    combine_type = parse_combine[ k ].split(' ', 1 )[1].split('(',1)[0]
                    if combine_type == 'S': #一旦發現為句子，就停止掃描parse陣列中的其他部分
                        sentence_flag = True
                        break
                    
                #if combine_type == 'S':
                if sentence_flag == True: #若合併後的文字做句子剖析的結果為S(句子)
                    combine_flag = True
                    line_text = combine_text #將合併的句子存入line_text以進到下一次的迭代判斷
                    sentence_flag = False
                else: #若合併後的文字做句子剖析的結果不是句子，就將目前此行直接印出
                    print('sentence',counter,':',line_text)
                    counter += 1

# 主程式區塊：讀入指定檔案
# 讀test1.pdf
readPDFandCombineSentences("test1.pdf")
# 讀test2.pdf
readPDFandCombineSentences("test2.pdf")