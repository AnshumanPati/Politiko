# -*- coding: utf-8 -*-
#The OS module in python provides functions for interacting with the operating system. 
#OS, comes under Python’s standard utility modules.
import os

#To incorporate several functions to remove stop words and facilitate stemming and lemmatization
import nltk

#To read and write csv files (data sets)
import csv 

#To incorporate math modules and functions
import math 

#For stemming (producing morphological variants of a root/base word) to shorten the lookup, and normalize sentences.
from nltk.stem import PorterStemmer

#Incorporating libraries for tokenization and removal of stopwords
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords

#We define this function to sort tuples (key-value pair) based on their key values.
#If key values match, then the tuples are sorted based on their values.

def Sort_Tuple(tp):    
    tp.sort(key = lambda x: (x[0],x[1]))  #tp indicates the key-value pair (tuple).
    return tp

#We define this function to sort tuples (key-value pair) based on their values.
#If values match, then the tuples are sorted based on their keys.

def Sort_Tuple2(tp):    
    tp.sort(key = lambda x: (x[1],x[0]))  
    return tp

#We define this function to merge term indicences documents to create the posting list for each term.

def Convert(tp, di): 
    for a, b in tp: 
        di.setdefault(a, []).append(b)
    return di

#We define this function to remove duplicates of the term

def removeDuplicates(lst): 
      
    return list(set([i for i in lst])) 

#After removing duplicates the result is stored in list.

#'files' stores all the text files from the Corpus folder.

files = []

for i in os.listdir('Corpus'):
    if i.endswith('.txt'):
        files.append(i)

print(files)

fin = []
autocorr = []
#We open the file contents in read mode.
for ft in files:
    #print(ft)
    f = open('Corpus\\'+ft, 'r') 
    file_contents = f.read() 
    
    #We tokenize the words in the 'files' list and store in 'file_contents'.
    file_contents = word_tokenize(file_contents) 
    
    #We convert the tokenized words into lowercase. We then remove unnecessary white spaces.
    #We also remove irrelevant words of length 1 which removes all the articles.
    z = []
    for x in file_contents: 
        z.append(x.lower().strip()) 
   # print(len(z))
    for a in z:
        if(len(a) is 1):
            z.remove(a); 
    for a in z:
        if(len(a) is 1):
            z.remove(a);
   # print(z)
    f.close()


    #We remove the stopwords using library functions from Python's NLTK package.
    sp_words = set(stopwords.words('english'))
    sp_words.add('its')
    sp_words.add('\'\'')
    li=[]
    for wrd in  z:
        if wrd not in sp_words:
            if wrd.isalpha():
                li.append(wrd)

    #print(len(li))
    #print(li)

    for vari in li:
        if(autocorr.count(vari)==0):
            autocorr.append(vari)
            
    #We stem the words to compare the root-words.
    pS = PorterStemmer() 
    n = []
    for w in li:
        n.append(pS.stem(w))
    #print(n)

    for w in n:
        fin.append((w,files.index(ft)))
    
    #Stored the final results in 'fin' list
# print(autocorr)

#We verify and observe that 'fin' list prints the output as expected. 
#The tuple indicates the term and its corresponding document index.

print(len(fin))
print(fin)

#We incorporate the Sort_Tuple() function defined above to sort the tuples in 'fin'.
fin2 = Sort_Tuple(fin)

#We verify and observe that 'fin2' list prints the output as expected. 
#The tuple indicates the term and its corresponding document index.

print(len(fin2))
print(fin2)

#We incorporate the removeDuplicates() function defined above and store the resultant list in fin3.
fin3 = removeDuplicates(fin2)

#We verify and observe that 'fin3' list prints the output as expected. 
#The tuple indicates the term and its corresponding document index.

print(fin3)

#We incorporate the Sort_Tuple() function defined above to sort the tuples in 'fin'.
fin4 = Sort_Tuple(fin3)

#We verify and observe that 'fin4' list prints the output as expected. 
#The tuple indicates the term and its corresponding document index.

print(len(fin4))
print(fin4)

#We convert the fin4 list into an Inverted Index which is designated by 'dt'.

dt = {} 
Convert(fin4, dt)

#We verify the length of the inverted index.
print(len(dt))

lnth = len(files)

#We write the Inverted Index data into 'dict.csv' file.
with open('dict.csv', 'w') as csv_file:
    writer = csv.writer(csv_file)
    for key, value in dt.items():
        writer.writerow([key, len(value),math.log(lnth/len(value)),value])

#We define 'tf_list' to store the term frequency for each term.
tf_list = []

#We initialize the term frequency for each term to be zero.
for i in range(len(dt)):
    tf_list.append(0)
print(len(tf_list))

#We store the term frequency. Corresponding rows store the document and columns store the unique terms in the corpus.
#We calculate the tf-score for each term.
with open('vct.csv', 'w') as csv_file:
    writer = csv.writer(csv_file)
    for ft in files:
        f = open('Corpus\\'+ft, 'r')
        file_contents = f.read()
        file_contents = word_tokenize(file_contents)
        z = []
        for x in file_contents:
            z.append(x.lower().strip())
       # print(len(z))
        for a in z:
            if(len(a) is 1):
                z.remove(a);
        for a in z:
            if(len(a) is 1):
                z.remove(a);
       # print(z)
        f.close()



        sp_words = set(stopwords.words('english'))
        sp_words.add('its')
        sp_words.add('\'\'')
        li=[]
        for wrd in  z:
            if wrd not in sp_words:
                if wrd.isalpha():
                    li.append(wrd)

    #print(len(li))
    #print(li)

        pS = PorterStemmer() 
        n = []
        for w in li:
            n.append(pS.stem(w))
            
        lst = []
        t = 0;
        for i in dt:
            p = n.count(i)
            if(p is 0):
                lst.append(p)
            else:
                lst.append(1+math.log(p))
            tf_list[t] += p
            t += 1
        writer.writerow(lst)
    #We assign the tf score for each term
    tf_score = []
    for i in tf_list:
        tf_score.append(1+math.log(i))
    print(tf_score)
    writer.writerow(tf_score)

#Incorporating the autocompletion feature. 
pg = []
query = "nar* modi" #We pass the query here.
qr = ""
qrl= []
nrt=query.split()
for vr in nrt:
    if vr[-1]=='*':
        qr = vr
qr = qr[0:-1]
qr = qr.lower().strip()
for i in autocorr:
    if(i.find(qr) == 0):
        qrl.append(i)
fqrl = []
countf = 0
lg = len(qrl)
while countf<lg:
    st = ""
    for i in nrt:
        if i[-1]!='*':
            st+=i
            st+=" "
        else:
            st+=qrl[countf]
            st+=" "
    fqrl.append(st)
    countf += 1

for i in fqrl:
    print(i)

user_query = "Gram - Panchayat"
file_contents = word_tokenize(user_query)
z = []
for x in file_contents:
    z.append(x.lower().strip())
# print(len(z))
for a in z:
    if(len(a) is 1):
        z.remove(a);
for a in z:
    if(len(a) is 1):
        z.remove(a);

sp_words = set(stopwords.words('english'))
sp_words.add('its')
sp_words.add('\'\'')
li=[]
for wrd in  z:
    if wrd not in sp_words:
        if wrd.isalpha():
            li.append(wrd)
            
pS = PorterStemmer() 
n = []
for w in li:
    n.append(pS.stem(w))
print(n)

rows = []
with open('dict.csv', 'r') as csvfile:
    csvreader = csv.reader(csvfile)
    for row in csvreader:
        if(len(row)>0):
            if row[0] in n:
                rows.append(row[3].replace('[',', ').replace(']',', ').split(', '))
# print(rows)

final=[]
for i in range(len(rows)):
     for j in rows[i]:
            if j!='':
                final.append(int(j))
                
# print(final)
final = removeDuplicates(final)
final.sort()
if len(final)>0:
    print("################################# 😀 Search Results Found :-D ###########################")
else:
    print("#################################😓 Sorry No Results Found :-(##########################")
for j in final:
    print(files[j])
print("##########################################################################################")
query_occ = []
query_idf = []
for i in n:
    query_occ.append(n.count(i))
pz = []
for i in range(len(n)):
    pz.append((n[i],1+math.log(query_occ[i])))
# print(pz)
pzd = removeDuplicates(pz)
# print(pzd)
mag = 0
for i in range(len(pzd)):
    mag += pzd[i][1]**2
mag = math.sqrt(mag)
# print(mag)
query_vect=[]
for i in range(len(n)):
    query_vect.append((n[i],(1+math.log(query_occ[i]))/mag))
# print(query_vect)
query_vectf=[]
query_vectf = removeDuplicates(query_vect)
# print(query_vectf)
queryVector = []
for i in dt:
    p = n.count(i)
    if p == 0:
        queryVector.append(0)
    else:
#         print(i)
        for j in query_vectf:
            if j[0]==i:
                queryVector.append(j[1])
# print(queryVector)
counter = 0
significance = []
idfsc = []
with open('dict.csv', 'r') as csvfile:
    csvreader = csv.reader(csvfile)
    for ro in csvreader:
        counter += 1
        if(counter%2==1):
            idfsc.append(float(ro[2]))
# print(idfsc)
counter = 0
with open('vct.csv', 'r') as csvfile:
    csvreader = csv.reader(csvfile)
    for ro in csvreader:
        counter += 1
        if((counter-1)/2 in final):
            mg = 0
            for z in ro:
                mg += float(z)**2
            mg = math.sqrt(mg)
            val = 0
            counter2 =0
            for z in ro:
                val += float(z)*queryVector[counter2]*idfsc[counter2]
                counter2 +=1
            val /= mg
            significance.append(val)
print(significance)

ultimate = []
for i in range(len(final)):
    ultimate.append((files[final[i]],significance[i]))
# print(ultimate)

ultimate2 = Sort_Tuple2(ultimate)
# print(ultimate2)
i = len(ultimate2)
if len(final)>0:
    print("########################### 😀 Top 10 Ranked Based Search Results :-D #########################")
tlt = 0
while i>0:
    tlt +=1
    i -= 1
    print(ultimate2[i][0])
    if tlt is 10:
        break;

