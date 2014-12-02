# File: Mini_Assingment_Four_van-der-Weegen_2566388.py
#
# Assignment: Mini Assignment Four
#  Due Data: 02/12/2014
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
Ids_file = search_folder + search_term + '__Ids.pkl.bz2'
Summaries_file = search_folder + search_term + '__Summaries.pkl.bz2'
Citations_file = search_folder + search_term + '__Citations.pkl.bz2'
Abstracts_file = search_folder + 'evolution__Abstracts.pkl.bz2'

# Keep our imports organized
import cPickle, bz2
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import networkx as nx
import sys
from collections import namedtuple
from collections import defaultdict
from collections import Counter
from collections import *
from itertools import islice
from math import log10

plt.rcParams['savefig.dpi'] = 100

# Do some housekeeping
Ids = cPickle.load( bz2.BZ2File( Ids_file, 'rb' ) )
Citations = cPickle.load( bz2.BZ2File( Citations_file, 'rb' ) )
Abstracts = cPickle.load( bz2.BZ2File( Abstracts_file, 'rb' ) )
Summaries = cPickle.load( bz2.BZ2File( Summaries_file, 'rb' ) )
paper = namedtuple( 'paper', ['title', 'authors', 'year', 'doi'] )
for (id, paper_info) in Summaries.iteritems():
 Summaries[id] = paper( *paper_info )

# Define our Global Vars
papers_of_author = defaultdict(set)
coauthors = defaultdict(set)
papers_citing = Citations
cited_by = defaultdict(list)
papers_pagerank = defaultdict(set)
papers_hub = defaultdict(set)
papers_auth = defaultdict(set)
G = None
inverted_index = defaultdict(set)
tf_matrix = defaultdict(Counter)

def display_summary( id, extra_text='' ):
 """
 Function for printing a paper's summary through IPython's Rich Display System.
 Trims long titles or author lists, and links to the paper's  DOI (when available).
 
 Modified for Pretty Console Printing
 """
 s = Summaries[ id ]
 
 title = ( s.title if s.title[-1]!='.' else s.title[:-1] )
 title = title[:150].rstrip() + ('' if len(title)<=150 else '...')

 authors = "\n\t"+', '.join( s.authors[:5] ) + ('' if len(s.authors)<=5 else ', ...')
 
 lines = [
  "\n"+title,
  authors,
  "\t"+str(s.year),
  '\tid: %d%s' % (id, extra_text)
  ]
 
 print(" ".join(lines)) 

# Construct the Global Citings list
def prepare_citings():
 global cited_by
 for ref, papers_citing_ref in papers_citing.iteritems():
  for id in papers_citing_ref:
   cited_by[ id ].append( ref )
 cited_by = dict(cited_by)

# Construct the Global papers_of_author set
def prepare_papers_of_author():
 global papers_of_author
 for id,p in Summaries.iteritems():
  for a in p.authors:
   papers_of_author[a].add( id )

# Construct the Global coauthors set
def prepare_coauthors():
 global coauthors
 for p in Summaries.itervalues():
  for a in p.authors:
   coauthors[ a ].update( p.authors )

  # the code above results in each author being listed as
  # having co-autored with himself. We now remove such references here
 for a,ca in coauthors.iteritems():
  ca.remove( a )

def construct_network():
 global G
 ## Construct Network ##
 with_cit = [ id for id in Ids if papers_citing[id]!=[] ] 
 isolated = set( id for id in Ids if papers_citing[id]==[] and id not in cited_by )
 noCit_withRefs = [ id for id in Ids if papers_citing[id]==[] and id in cited_by ]

 G = nx.DiGraph(cited_by)
 G.add_nodes_from(isolated)

def prepare_pagerank():
 global papers_pagerank
 # Save pagerank for papers
 papers_pagerank = nx.pagerank_scipy(G)

def prepare_hubs_auth():
 global papers_auth
 global papers_hub
  # Save Hubs and Authority Scores
 h,a = nx.hits_scipy(G)
 for (id, hubs) in h.iteritems():
  papers_hub[id] = hubs
 for (id, auth) in a.iteritems():
  papers_auth[id] = auth

def print_papers_of_author(author):
 for id in papers_of_author[author]:
  display_summary(id)

# Since casting the a dict causes a KeyError when the key doens't exist,
# Catch!
def cited_by_paper(id):
 try:
  return id in cited_by
 except KeyError:
  return False

def tokenize(text):
 return text.split(' ')

def preprocess(tokens):
 result = []
 for token in tokens:
  result.append(token.lower())
 return result

def prepare_inverted_index():
 global inverted_index
 # Takes a while
 for (id, abstract) in Abstracts.iteritems():
  for term in preprocess(tokenize(abstract)):
   inverted_index[term].add(id)

def prepare_tf_matrix():
 global tf_matrix
 for (id, abstract) in Abstracts.iteritems():
  tf_matrix[id] = Counter(preprocess(tokenize(abstract)))

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
  return_dict.items()], reverse=True)[:10]

def query_with_pagerank(query_string):
 tmp_dict = {}
 return_dict = {}
 # Tokenize and Preprocess
 for query_word in preprocess(tokenize(query_string)):
  for document in list(inverted_index[query_word]):
   if (document not in tmp_dict):
    tmp_dict[document] = tfidf(query_word, document)
   else:
    tmp_dict[document] += tfidf(query_word, document)
 
 for id,score in tmp_dict.iteritems():
  # Normalize the Pagerank by adding 1
  return_dict[id] = score * (float(1)+ float(papers_pagerank[id]))
  
 return sorted([(key, value) for (value, key) in\
  return_dict.items()], reverse=True)[:10]

def query_with_hits_auth(query_string):
 tmp_dict = {}
 return_dict = {}
 # Tokenize and Preprocess
 for query_word in preprocess(tokenize(query_string)):
  for document in list(inverted_index[query_word]):
   if (document not in tmp_dict):
    tmp_dict[document] = tfidf(query_word, document)
   else:
    tmp_dict[document] += tfidf(query_word, document)
 
 for id,score in tmp_dict.iteritems():
  # Normalize the HUBS+HITS by adding 1
  return_dict[id] = score * (float(1) + float(papers_hub[id]) +\
                             float(papers_auth[id]))
  
 return sorted([(key, value) for (value, key) in\
  return_dict.items()], reverse=True)[:10]


# Main Function (keep it all neat)
if __name__ == '__main__':
 prepare_papers_of_author()
 prepare_coauthors()
 prepare_inverted_index()
 prepare_tf_matrix() 
 prepare_citings()
 construct_network()
 prepare_pagerank()
 prepare_hubs_auth()
 
 ## ALL THE TESTS HAVE BEEN MOVED TO Mini_Assingment_Four-Tests_van-der-Weegen_2566388.py
 
 query_string = "evolutionary embodied"
 print "\nRegulur Query"
 for n in query(query_string):
  print n
 
 print "\nPagerank Query"
 for n in query_with_pagerank(query_string):
  print n
  
 print "\nHITS and AUTH Query"
 for n in query_with_hits_auth(query_string):
  print n
