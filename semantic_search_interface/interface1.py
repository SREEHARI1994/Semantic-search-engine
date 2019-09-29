from flask import Flask, render_template, request
import pymongo

import re
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["travelbig1"]
mycol3=mydb["topicwords"]
mycol4=mydb["doc_words"]

mydb2 = myclient["travelbig2"]
mycol2 = mydb2["big_col2"]

#mycol3 used for storing topic numbers and the words in each topic
#mycol2 in travelbig2 database contains numbered documents. this db is to be used for displaying the results
#mycol4 is used to store each word and the document number to which it belongs


def process_text(query):
  stop_words = set(stopwords.words('english')) 

  query=re.sub(r"[^A-Za-z]"," ",query)

  word_tokens = word_tokenize(query.lower()) 

  filtered_sentence = [w for w in word_tokens if not w in stop_words] 

  
  return filtered_sentence


app = Flask(__name__)

@app.route('/')
def student():
   return render_template('search.html')

@app.route('/result',methods = ['POST', 'GET'])
def result():
	if request.method == 'POST':


		search=request.form.get("sname")


		search_query=process_text(search)

		search_query=list(set(search_query))
		twords=mycol3.find_one()
		
		del twords['_id']
		result=[]

		for word in search_query:
			for key in twords:
				if word in twords[key]:
					result=result+twords[key]

		result_dict={}
		docmap=mycol4.find_one()
		for word in result:
			k=docmap[word]

			result_dict[k]=result_dict.get(k,0)+1
		counts=list(set(list(result_dict.values())))
		counts.sort(reverse=True)
		
		i=0
		data=[]
		for count in counts:
			if i==10:
				break
			i=i+1
			for v in result_dict:
				if result_dict[v]==count:
					myquery = { "no": v }
					#print(mycol2.find(myquery))
					data.append(mycol2.find_one(myquery))



      # User entered query is now contained in search_query

      #using that do all the word2vec modelling and clutering to obtain the final results

      # final result- consists of dictionaries each having title,url,text

      #take them from the databse and add them to the data list in the order of their priority, most ranked title,url,text coming first

      # here just for the sake of displaying, I have  taken all documents from my database and displayed it one by one

      
      






      #data is a list containing the dictionary of contents from the databse to  be displayed.each dict having title,url and text

	return render_template("result.html", users=data,search=search)

if __name__ == '__main__':
   app.run(debug = True)