# File: Mini_Assingment_One-Sub1_van-der-Weegen_2566388.py
#
# Assignment: Mini Assignment One [Sub1]
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

paper_year = [ p.year for p in Summaries.itervalues() ]
 
papers_per_year = defaultdict(list)

for p in Summaries.itervalues():
 if p.year >= 1950:
  papers_per_year[ p.year ].append(p.authors)
  
years = sorted(papers_per_year.keys())
pltlist = []
for year in years:
 pltlist.insert(year, len(papers_per_year[year])) 

plt.bar( left=years, height=pltlist, width=1.0 )
plt.xlim(1950,2016)
plt.xlabel('year')
plt.ylabel('Authors that published at least 1 paper');
plt.show()