import pandas as pd
import pdfplumber as pp
import os
import numpy as np
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer
from collections import Counter

PDFS_FOLDER = ("C:\\Users\HP\pdfs") #get the pdfs from this directory
save_to = ('C:\\Users\HP\Outputs\\')  #save the csv with all the content in this location

def get_all_pdfs(folder_path):
    """
    :absolute folder path of the pdfs
    :return: a list with all the absolute path of pdfs
    """
    return os.listdir(folder_path)

def create_absolute_path(root_path, file_name):
    """
    :absolute route path
    :param file_name: file name
    :return: absolute path of the file name
    """
    root_path = root_path + '/' if root_path[-1] != '/' else root_path
    return "%s%s" %(root_path, file_name)

#This function converts each pdf to text and returns a list of one element i.e. the content
def convert_pdf_to_text(pdf_path):
    pdf = open(pdf_path, "rb")
    pdf = pp.open(pdf)   #opens the pdf
    #text_byte_array = bytearray()
    t = []
    for n in range(0, len(pdf.pages)):
        current_page = pdf.pages[n]
        page_content = current_page.extract_text()
        if n == 0:
            t.append(page_content)
        else:
            t[0] = t[0] + " " + page_content
    return t
    
all_pdfs = get_all_pdfs(PDFS_FOLDER)
df = pd.DataFrame(columns=['Content'])
l = 0
for pdf_file_name in all_pdfs:
    abs_path_pdf = create_absolute_path(PDFS_FOLDER, pdf_file_name)
    text = convert_pdf_to_text(abs_path_pdf)
    df.loc[l] = list(text)          #saves the content in a dataframe with one column of the content per doc
    l += 1
#download the contents of all pdfs as a csv. Enter the location where the csv should be stored
df.to_csv(save_to+'first.csv')
#first task of getting content as csv ends


#task_2
final_text = []                     #list to store the cleaned string

#splits each content and filters out stopwords and terms with special characters and digits
for n in range(len(df.index)):
    split_text = df.loc[n][0].split()  #splits the content
    split_text = [a for a in split_text if (a.isalpha() and (a not in set(stopwords.words('english'))))]  #filters out stopwords and terms with special characters and digits
    final_text.append(split_text)   #list of contents from all docs, split and filtered
#merging the split content into a string
merged_text = []
for n in final_text:
    m = ''
    for x in n:
        m += (' ' + x)
    merged_text.append(m)           #ultimately would be a list of all contents

#getting the top 10 essential and frequent words for each pdf from the cleaned content using sklearn

#doing tf-idf
vectorizer = CountVectorizer()
vectors = vectorizer.fit_transform(merged_text)
feature_names = vectorizer.get_feature_names()
dense = vectors.todense()
denselist = dense.tolist()
final_df = pd.DataFrame(denselist, columns=feature_names) #Gives the tf-idf output for each doc in form of a dataframe

#getting top 10 words with highest score
nlargest = 10
result = []
for x in range(len(final_df.index)):
    my_dict = dict(final_df.loc[x]) #gets each row as dictionary
    k = Counter(my_dict)            
    high = k.most_common(10)        #gets 10 most common words and their value
    temp = []
    for i in high: 
        temp.append(i[0])           #removes the value and gets only the 10 words
    result.append(temp)             #list of list top 10 words for all docs

#converting the result as a dataframe name of the pdf and 10 words as columns
output_df = pd.DataFrame(columns=['File Name', 'Content'])
file_names = os.listdir(PDFS_FOLDER)#names of all the pdf files
for n in range(len(file_names)):
    output_df.loc[n] = [file_names[n], result[n]]
output_df.to_csv(save_to+'final.csv')#saves the df as csv