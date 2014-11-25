# File: Mini_Assingment_Three_van-der-Weegen_2566388.py
#
# Assignment: Mini Assignment Three
#  Due Data: 25/11/2014
#
# Author:  Cas van der Weegen
#  Student no: 2566388
#  Study: Computer Sciences
#  Course: Information Retrieval
#
search_term = 'evolution' # Define Search Term
search_folder = '../../Datasets/' # Define folder where files are located
                                  # note: I try to maintain a neatly sorted
                                  #  folder structure for my university work,
                                  #  hence the need for a search_folder
Summaries_file = search_folder + 'evolution__Summaries.pkl.bz2'
Abstracts_file = search_folder + 'evolution__Abstracts.pkl.bz2'

# Keep our imports organized
import cPickle, bz2
import re
import nltk
from collections import namedtuple
from collections import defaultdict
from collections import Counter
from nltk.tokenize import word_tokenize
from nltk.stem.snowball import EnglishStemmer
from math import log10

# Do some housekeeping
Summaries = cPickle.load( bz2.BZ2File( Summaries_file, 'rb' ) )
Abstracts = cPickle.load( bz2.BZ2File( Abstracts_file, 'rb' ) )
paper = namedtuple( 'paper', ['title', 'authors', 'year', 'doi'] )
for (id, paper_info) in Summaries.iteritems():
 Summaries[id] = paper( *paper_info )
nltk.download('punkt')
stemmer = EnglishStemmer()

# Define our Global Vars
inverted_index = defaultdict(set)
smarter_index = defaultdict(set)
tf_matrix = defaultdict(Counter)


# Display the summary of a document
def display_summary( id, extra_text='' ):
 """
 Function for printing a paper's summary through IPython's Rich Display System.
 Trims long titles or author lists, and links to the paper's  DOI (when available).
 """
 s = Summaries[ id ]
 
 title = ( s.title if s.title[-1]!='.' else s.title[:-1] )
 title = title[:150].rstrip() + ('' if len(title)<=150 else '...')
 if s.doi!='':
  title = '<a href=http://dx.doi.org/%s>%s</a>' % (s.doi, title)
   
 authors = ', '.join( s.authors[:5] ) + ('' if len(s.authors)<=5 else ', ...')
 
 lines = [
  title,
  authors,
  str(s.year),
  '<small>id: %d%s</small>' % (id, extra_text)
 ]
 
 print('<blockquote>%s</blockquote>' % '<br>'.join(lines))

# Display the abstract of a document
def display_abstract( id, highlights=[]):
 """
 Function for displaying an abstract. Includes optional (naive) highlighting
 """
 a = Abstracts[ id ]
 for h in highlights:
  a = re.sub(r'\b(%s)\b'%h,'<mark>\\1</mark>',a, flags=re.IGNORECASE)
 print('<blockquote>%s</blockquote' % a )

def tokenize(text):
 """
 Function that tokenizes a string in a rather naive way. Can be extended later.
 """
 return text.split(' ')

def preprocess(tokens):
 """
 Perform linguistic preprocessing on a list of tokens. Can be extended later.
 """
 result = []
 for token in tokens:
  result.append(token.lower())
 return result

def smarter_tokenize(text):
 return word_tokenize(text)

def smarter_preprocess(tokens):
 result = []
 for token in tokens:
  result.append(stemmer.stem(token.lower()))
 return result

def prepare_inverted_index():
 global inverted_index
 # Takes a while
 for (id, abstract) in Abstracts.iteritems():
  for term in preprocess(tokenize(abstract)):
   inverted_index[term].add(id)

def prepare_smarter_inverted_index():
 global smarter_index
 # Create a subset of around 1400 document IDs
 subset = set(Abstracts.keys()).intersection(set(xrange(23100000,23200000)))

 for (id, abstract) in ((k, Abstracts[k]) for k in subset):
  for term in smarter_preprocess(smarter_tokenize(abstract)):
   smarter_index[term].add(id)

def prepare_tf_matrix():
 global tf_matrix
 for (id, abstract) in Abstracts.iteritems():
  tf_matrix[id] = Counter(preprocess(tokenize(abstract)))

# Short (one-liner) versions of and_query and or_query
def or_query(query):
 return reduce(lambda a, e: a.union(e),
               [inverted_index[term] for term in preprocess(tokenize(query))])

def and_query(query): 
 return reduce(lambda a, e: a.intersection(e),
               [inverted_index[term] for term in preprocess(tokenize(query))])
 
# Regular and_query using smarter_tokenize and smarter_preprocess
def smarter_and_query(query):
 return reduce(lambda a, e: a.intersection(e),
               [smarter_index[term] for term in \
                smarter_preprocess(smarter_tokenize(query))])

# Return Term Frequency
def tf(t,d):
 return float(tf_matrix[d][t])

# Return document frequency
def df(t):
 return float(len(inverted_index[t]))

# Return the number of Documents (N)
def num_documents():
 return float(len(Abstracts))

# tf-idf weighting
def tfidf(t, d):
 # Make sure we don't divide by 0 [not working? Make sure python >= 2.5]
 return float(0.0) if ((tf(t,d) == 0.0) or (df(t) == 0.0)) else \
  float((1.0+log10(tf(t,d))) * float(log10(num_documents()/df(t))))

# Return top results [based on regular tokenize and preprocess]
def query(query_string):
 return_dict = {}
 # Tokenize and Preprocess
 for query_word in preprocess(tokenize(query_string)):
  for document in list(inverted_index[query_word]):
   if (document not in return_dict):
    return_dict[document] = tfidf(query_word, document)
   else:
    return_dict[document] += tfidf(query_word, document)
 return sorted([(key, value) for (value, key) in\
  return_dict.items()], reverse=True)[:9]

# Main Function (keep it all neat)
if __name__ == '__main__':
 # Prepare the inverted Index
 prepare_inverted_index()
 prepare_tf_matrix() 
 #prepare_smarter_inverted_index()
 query_string = "evolutionary embodied"
 #print and_query(query_string)
 #print smarter_and_query(query_string)
 #print 23144668 in and_query(query_string)
 #print 23144668 in smarter_and_query(query_string)
 #print display_abstract(23145344)
 #print display_abstract(23116592)
 #print smarter_preprocess(smarter_tokenize(query_string))
 #print display_abstract(23144668)

 #print tf('evolution',23144668)
 #print df('evolution')
 #print num_documents()
 #print tfidf('embodied',23144668)
 #print tfidf('evolution',23144668)
 #print tfidf('notinthedocument',23144668)
 
 #print "19665560:"
 #print tfidf('evolutionary', 19665560)
 #print tfidf('embodied', 19665560)
 #print "23098601:"
 #print tfidf('evolutionary', 23098601)
 #print tfidf('embodied', 23098601)
 #print "21241334:"
 #print tfidf('evolutionary', 21241334)
 #print tfidf('embodied', 21241334)
 
 print query(query_string)