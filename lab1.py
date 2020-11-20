from pathlib import Path
from tkinter import *
import tkinter.ttk as ttk
from tkinter import messagebox
from tkinter import filedialog
from checklist import *
from nltk import *
from operator import itemgetter
from string import punctuation
from nltk.corpus import stopwords

docs = []
searchDocs = []
lemmatizer = WordNetLemmatizer()
root=Tk()

def get_words_from(text):
    words = set()
    for sentence in sent_tokenize(text):
        for word in word_tokenize(sentence):
            if word not in punctuation and word not in stopwords.words("english"):
                words.add(lemmatizer.lemmatize(word.lower()))
    return words

def get_relevant_docs(query):
    result = []
    query_words = get_words_from(query)
    for i, text in enumerate([item[2] for item in docs]):
        matches = get_words_from(text) & query_words
        matches_count = len(matches)
        if matches_count > 0:
            result.append((matches_count, i, ", ".join(matches)))
    return sorted(result, key=itemgetter(0), reverse=True)

space0 = Label(root,text='\n')
chooseDocsButton=Button(root,text='Choose docs',width=55,height=2,bg='light grey')
space1 = Label(root,text='\n')
checklist = ChecklistBox(root, [])
space2 = Label(root,text='\n')
searchEntry=Entry(root,width=55)
space3 = Label(root,text='\n')
searchButton=Button(root,text='Search',width=55,height=2,bg='light grey')
space4 = Label(root,text='\n')
checklistSearch = ChecklistBox(root, [])
space5 = Label(root,text='\n')
metricsButton=Button(root,text='Metrics',width=55,height=2,bg='light grey')
space6 = Label(root,text='\n')


def nameOf(path):
	return Path(path).stem

def chooseDocsClicked():
	global docs, searchDocs
	docs = []
	searchDocs = []
	files = filedialog.askopenfilename(multiple=True)
	splitlist = root.tk.splitlist(files)
	filePaths = []
	for f in splitlist:
		filePaths.append(f)
	filePaths = sorted(filePaths)
	for i, doc in enumerate(filePaths):
		docs.append((i, doc, Path(doc).read_text()))
	checklist.update([nameOf(item[1]) for item in docs])

def searchClicked():
	global searchDocs
	searchDocs = get_relevant_docs(searchEntry.get())
	checklistSearch.update([nameOf(docs[item[1]][1]) + "     [" + item[2] + "]" for item in searchDocs])

def metricsClicked():
	allLen = len(docs)
	searchLen = len(searchDocs)
	allRelevant = checklist.getCheckedItems()
	searchRelevant = set([searchDocs[item][1] for item in checklistSearch.getCheckedItems()])
	a = len(searchRelevant) # search relevant
	b = searchLen - a # search not relevant
	c = len(allRelevant - searchRelevant) # not search relevant
	d = len((set(range(len(docs))) - allRelevant) - (set([item[1] for item in searchDocs]) - searchRelevant)) # not search not relevant
	messagebox.showinfo("Metrics","recall = " + str(a/(a+c)) +
		                "\nprecision = " + str(a/(a+b)) +
		                "\naccuracy = " + str((a+d)/(a+b+c+d)) +
		                "\nerror = " + str((b+c) / (a+b+c+d)) +
		                "\nf-measure = " + str(2 / ((1/(a/(a+b))) + (1/(a/(a+c))))))


chooseDocsButton.config(command=chooseDocsClicked)
searchButton.config(command=searchClicked)
metricsButton.config(command=metricsClicked)



aboutButton = Button(root,text='About',width=8,height=2,bg='light grey')
def aboutButtonClicked():
	messagebox.showinfo("Lab 1", "Usage: Choose docs, enter query and search.\n\nDeveloped by: Artyom Gurbovich and Pavel Kalenik.")
aboutButton.config(command=aboutButtonClicked)
aboutButton.pack()

space0.pack()
chooseDocsButton.pack()
space1.pack()
checklist.pack()
space2.pack()
searchEntry.pack()
space3.pack()
searchButton.pack()
space4.pack()
checklistSearch.pack()
space5.pack()
metricsButton.pack()
space6.pack()
root.mainloop()



