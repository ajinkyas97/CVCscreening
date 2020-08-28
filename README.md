# Tasks 1,2 & 3
This is the submission of tasks for the CVChamp screening.
The 'pdf.rar' contains the 50 PDFs required.
The 'cvchamp.py'is the code for task 2&3.

In the code, the PDF_FOLDER variable stores the directory of all PDFs and the save_to stores the directory where result of task 2 and 3 would be stored as csv files.
The code first gets the file names from the provided directory and creates the path for each pdf file.

Then it extracts the entire text content from each file using the pdfplumber library using 'pdfplumber.open()' command and adds it to a data frame. Then it is saved as csv using '.to_csv' function.
This is the output of the task 2

For task 3:
It cleans the text data of each pdf for the special characters/digits and stopwords.
It does so by splitting the text into individual terms, filtering the ones that don't satisfy the criterion and again combining the individual words into a string. NL toolkit(nltk) library is used for stopwords.

Once filtered, it is again merged into one content string per pdf. This list of contents is then used to do TF-IDF to get a score per word representing its frequency and essence combined, in the document. CountVectorizer, scikit learn library is used for this. It returns a DataFrame(pandas). Then top ten words per document is obtained by converting each row of the dataframe to dictionary. 

Further this list of 10 words per doc along with the names of the PDFs is converted into a DataFrame and saved as csv which is the output for task 3 as required 
