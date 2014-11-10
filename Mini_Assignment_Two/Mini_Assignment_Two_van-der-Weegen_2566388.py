# File: Mini_Assingment_Two_van-der-Weegen_2566388.py
#
# Assignment: Mini Assignment Two
#  Due Data: 12/11/2014
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
from collections import namedtuple
from collections import defaultdict

# Do some housekeeping
Summaries = cPickle.load( bz2.BZ2File( Summaries_file, 'rb' ) )
paper = namedtuple( 'paper', ['title', 'authors', 'year', 'doi'] )
for (id, paper_info) in Summaries.iteritems():
 Summaries[id] = paper( *paper_info )
Abstracts = cPickle.load( bz2.BZ2File( Abstracts_file, 'rb' ) )

# Define the inverted Index
inverted_index = defaultdict(set)

# Provided Function
def tokenize(text):
 """
 Function that tokenizes a string in a rather naive way. Can be extended later.
 """
 return text.split(' ')

# Provided Function
def preprocess(tokens):
 """
 Perform linguistic preprocessing on a list of tokens. Can be extended later.
 """
 result = []
 for token in tokens:
  result.append(token.lower())
 return result

# Provided Function [Modified for Console Use]
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
 print '<blockquote>%s</blockquote>' % '<br>'.join(lines)

# Provided Function [Modified for Console Use]
def display_abstract( id, highlights=[]):
 """
 Function for displaying an abstract. Includes optional (naive) highlighting
 """
 a = Abstracts[ id ]
 for h in highlights:
  a = re.sub(r'\b(%s)\b'%h,'<mark>\\1</mark>',a, flags=re.IGNORECASE)
 print ('<blockquote>%s</blockquote>' % a)

def or_query(query):
 print "\nSearching for Documents containing: "+" OR ".join(n for n in tokenize(query))
 return_list = []
 # Tokenize and Preprocess
 for query_word in preprocess(tokenize(query)):
  return_list  = return_list + list(inverted_index[query_word])
 return return_list

def and_query(query):
 print "\nSearching for Documents containing: "+" AND ".join(n for n in tokenize(query))
 return_list = []
 first_iteration = True
 # Tokenize and Preprocess
 for query_word in preprocess(tokenize(query)):
  # First pass should fill the return_list
  if(first_iteration == True):
   return_list = list(inverted_index[query_word])
   first_iteration = False
  else:
   return_list = [n for n in return_list if n in list(inverted_index[query_word])]
 return return_list

def prepare_inverted_index():
 # Make sure we can access the global inverted index
 global inverted_index
 # Takes a while
 for (id, abstract) in Abstracts.iteritems():
  for term in preprocess(tokenize(abstract)):
   inverted_index[term].add(id)

# Main Function (keep it all neat)
if __name__ == '__main__':
 # Prepare the inverted Index
 prepare_inverted_index()
 # Setup Query
 query = "Evolutionary Process"
 #print len(or_query("The Who"))
 #print display_abstract(23144668)

 print or_query(query)
 print and_query(query)
 # Print Results OR_QUERY
 #for result in or_query(query):
  #print display_abstract(result)
 
 # Print results AND_QUERY
 #for result in and_query(query):
  #print display_abstract(result)