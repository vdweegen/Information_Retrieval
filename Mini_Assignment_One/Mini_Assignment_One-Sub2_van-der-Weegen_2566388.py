# File: Mini_Assingment_One-Sub2_van-der-Weegen_2566388.py
#
# Assignment: Mini Assignment One [Sub2]
#  Due Data: 04/11/2014
#
# Author:  Cas van der Weegen
#  Student no: 2566388
#  Study: Computer Sciences
#  Course: Information Retrieval
#  Date:    04/11/2014
#
search_term = 'evolution' # Define Search Term
search_folder = '../../Datasets/' # Define folder where files are located
                                  # note: I try to maintain a neatly sorted
                                  #  folder structure for my university work,
                                  #  hence the need for a search_folder
Summaries_file = search_folder + search_term + '__Summaries.pkl.bz2'

# Keep our imports organized
import cPickle, bz2
import matplotlib.pyplot as plt
import re
from collections import namedtuple
from collections import Counter
from collections import defaultdict

# Configuration
plt.rcParams['savefig.dpi'] = 100

# Use cPickle to load the Summeries
Summaries = cPickle.load( bz2.BZ2File( Summaries_file, 'rb' ) )

# Put in tumple
paper = namedtuple( 'paper', ['title', 'authors', 'year', 'doi'] )

# Order in List
for (id, paper_info) in Summaries.iteritems():
 Summaries[id] = paper(*paper_info)
 
# assemble list of words in paper titles, convert them to lowercase, and remove eventual trailing '.'
title_words = Counter([
    ( word if word[-1]!='.' else word[:-1] ).lower()
    for paper in Summaries.itervalues()
    for word in paper.title.split(' ')
    if word != ''     # the split by spaces generates empty strings when consecutive spaces occur in the title; this discards them
    ])

print len(title_words), 'distinct words occur in the paper titles.\n'
print '100 most frequently occurring words:'
srted = sorted(title_words.items(), key=lambda i:i[1])[-100:]
print srted
pltlist = []
for index, val in enumerate(srted):
 pltlist.insert(index, val[1])
 
plt.plot(pltlist)
plt.ylabel("Frequency")
plt.xlabel("100 Most Used words [index 100 is most used]")
plt.show()