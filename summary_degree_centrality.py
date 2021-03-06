import nltk
import math
import re
from nltk.corpus import stopwords
from textblob import TextBlob

data_sen = 'data1.txt'
# sentnce = open(data_sen)

data = open(data_sen,'r').read()

stops = list(stopwords.words('english'))
#setting the type to string in the stops list
stops = [str(x) for x in stops]

#list for storing sentences
list_of_sen = []

s1 = data.decode('utf-8')
sent = TextBlob(s1)

for i in sent.sentences:
	# print i,"\n"
	list_of_sen.append(str(i))
# for s in senetnces:
# 	s.split('.')
# 	# re.split(r'.[\n]*[\r]*',s)
	# i.rstrip('\r\n''.')
	# i.lstrip(' ')
	# print i,"\n"
''' printing the sentences read from the text file '''
# for i in list_of_sen:
	# i.rstrip('\"''.')
	# i.lstrip(' ''\"')
	# print i,"\n"



'''getting the count of all words in the document and a list of list containing the words in a sentences'''
#list of list [s1[w1,w2,....,wn], s2[w1,w2,....,wn]....]
lst_lst_sen_word = []
#list of dict for every sentence [s1:{(w1,freq),...,(w2,freq)},...,s5:{(w1,freq),...,(w2,freq)}]
lst_dict_sen_word = []
#global dictioary of words for the whole doc
word_uniq = {}

for s in list_of_sen:
	# words = s.split(' ')
	words = list(re.findall(r"[\w']+", s))
	
	#temporary list and dictioary for a particular sentence
	list_words_in_sent = []
	dict_words_in_sent ={}

	for w in words:
		w = w.rstrip(')'',''"')
		w = w.lstrip('(''"')
		w = str(w)

		if w not in stops:
			list_words_in_sent.append(w)

			if w not in dict_words_in_sent:
				dict_words_in_sent[w] = 1
			else:
				dict_words_in_sent[w] = dict_words_in_sent[w] + 1

			if w not in word_uniq:
				word_uniq[w] = 1
			else:
				word_uniq[w] = word_uniq[w] + 1

	lst_dict_sen_word.append(dict_words_in_sent)
	lst_lst_sen_word.append(list_words_in_sent)

''' printing the elements of list of list of words in sentences '''
for itemL in lst_lst_sen_word:
		print itemL
# print "".join([str(list_words_in_sent) for list_words_in_sent in lst_lst_sen_word]) 

'''printing the dict of words in sorted order'''
# for itemD in sorted(word_uniq):
# 	print itemD,word_uniq[itemD]


''' printing the elements of list of dict (words in sentences )'''
# for x in lst_dict_sen_word:
# 	print x.keys()	
# 	print x.values()


''' calculating tf '''
#list of dict conataing the tf of each word for each sentence
tf_list_dict = []

for iL in lst_dict_sen_word:
	tf_dict_per_sent = {}
	sum_of_keys = sum(iL.values())
	# print sum_of_keys
	# print sorted(iL)

	for iD in sorted(word_uniq):
		# print iD
		if iD in sorted(iL):
			# print iL[iD]
			tf_dict_per_sent[iD] = float(iL[iD])/sum_of_keys
		else:
			tf_dict_per_sent[iD] = 0

	tf_list_dict.append(tf_dict_per_sent)

''' printing tf : word-sentence matrix '''
# print "\n",len(tf_list_dict)
print "\n printing tf : word-sentence matrix \n" 
for iL in tf_list_dict:
	print iL.keys()
	print iL.values(),'\n'

''' calculating idf '''
### idf = log(N/n(i)) where N = total number of sentences in doc ; n(i) = number of sentences having the word(i)
total_no_sen = len(list_of_sen)
idf_dict_word = {}

for iD in sorted(word_uniq):
	count_sen = 0
	for iL in lst_dict_sen_word:
		if iD in sorted(iL):
			count_sen = count_sen + 1
	idf_dict_word[iD] = 1.0 + math.log((float(total_no_sen)/count_sen))

''' printing the idf values of each word '''
print "\nprinting the idf values of each word\n"
for iD in sorted(idf_dict_word):
	print iD,idf_dict_word[iD]

''' calculating tf-idf of words in each sentence '''
# tf*idf score for eachc word in each sentence list of dict for each sentence
tf_idf_list_dict = []

for iL in tf_list_dict:
	idf_dict_sen = {}
	for iD in sorted(iL):
		# print iL[iD]
		idf_dict_sen[iD] = iL[iD]*idf_dict_word[iD]
		# print idf_dict_sen[iD]
	tf_idf_list_dict.append(idf_dict_sen)


''' printing tf*idf matrix for each sentence row = sentence col = words '''
# print "\nprinting tf*idf matrix "
# print len(tf_idf_list_dict)
# for iL in tf_idf_list_dict:
# 	#print iL.keys()
# 	print iL.values()


''' calculating idf-modified-cosine between sentences '''

# sum of (tf Xi,X * idf Xi) ^2

cosine_sim_list_list = []

for i in range(len(tf_list_dict)):
	temp_list = []
	

	for j in range(len(tf_list_dict)):
		temp11 = 0.0
		temp22 = 0.0
		temp33 = 0.0
		
		for item1, item2 in zip ((tf_list_dict[i]) ,(tf_list_dict[j])):
			temp1 = 0
			temp2 = 0
			temp3 = 0

			temp = round(idf_dict_word[item1],6)**2
			temp = round(temp,6)
			# print temp
			
			temp1 = round(tf_list_dict[i][item1],6)*round(tf_list_dict[j][item2],6)
			temp11 += round(temp1,6)*round(temp,6)
			temp11 = round(temp11,6)

			temp2 = round(tf_list_dict[i][item1],6)*round(idf_dict_word[item1],6)
			temp22 += round(temp2,6)*round(temp2,6)
			temp22 = round(temp22,6)

			temp3 = round(tf_list_dict[j][item2],6)*round(idf_dict_word[item2],6)
			temp33 += round(temp3,6)*round(temp3,6)
			temp33 = round(temp33,6)

		temp = round((math.sqrt(temp22))*(math.sqrt(temp33)),6)
		temp = round(temp,6)
		temp = round((temp11/float(temp)),6)
		# print i, j, temp
		temp_list.append(temp)

	cosine_sim_list_list.append(temp_list)

''' printing cosine_sim_list_list matrix '''
for i in cosine_sim_list_list:
	print i


''' getting degree centrality '''

threshold1 = 0.1
threshold2 = 0.2

degree_centrality = []

for i in (range(len(cosine_sim_list_list))):
	t1 = 0
	t2 = 0
	temp = []
	for j in range(len(cosine_sim_list_list[i])):
		# print "i ",i," j ",j
		if i != j:
			if cosine_sim_list_list[i][j] > threshold1:
				t1 += 1
			if cosine_sim_list_list[i][j] > threshold2:
				t2 += 1
	temp.append(t1)
	temp.append(t2)
	degree_centrality.append(temp)

''' printing degree centrality '''
for i in degree_centrality:
	print i		

''' genarting summary sentences using degree centrality '''

summary_t1 = []
summary_t2 = []

# taking 5 as the cutoff for a sentence to be central threshold = 0.1
# taking 1 as the cutoff for a sentence to be central threshold = 0.2
for i in range(len(degree_centrality)):
	for j in range(len(degree_centrality[i])):
		
		if j == 0:
			if degree_centrality[i][j] >= 3:
				summary_t1.append(list_of_sen[i])

		if j == 1:
			if degree_centrality[i][j] >= 1:
				summary_t2.append(list_of_sen[i])

''' printing summary with degree centrality  '''
print "\nsummary with centrality cutoff >=4\n"
print len(summary_t1)
for i in summary_t1:
	print i

''' printing summary with degree centrality  '''
print "\nsummary with centrality cutoff >=1\n"
for i in summary_t2:
	print i




