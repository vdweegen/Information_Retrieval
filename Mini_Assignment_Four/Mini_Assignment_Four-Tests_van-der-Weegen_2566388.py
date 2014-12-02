# File: Mini_Assingment_Four-Tests_van-der-Weegen_2566388.py
#
# Assignment: Mini Assignment Four TESTS
#  Due Data: 02/12/2014
#
# Author:  Cas van der Weegen
#  Student no: 2566388
#  Study: Computer Sciences
#  Course: Information Retrieval
#
# NOTE: THIS FILE CONTAINS ALL THE EXECUTED TESTS AND ALL THE PRE-ASSIGNMENT
#       PYTHON CODE ASWEL AS THE CODE OF QUESTION ONE AND TWO
#

if __name__ == '__main__':
 # Prepare authors set
 prepare_papers_of_author()
 ## 11 ## Prepare coauthors set
 prepare_coauthors()
 ## 19 ## Prepare citings list
 prepare_citings()

 ## 9, 10 ## 
 print_papers_of_author("Eiben AE")
 display_summary( 23144668 )
 
 ## 12 ##
 print ', '.join( coauthors['Eiben AE'] )
 
 ## 13 ##
 for id in papers_of_author['Wilson EO'] & papers_of_author['Nowak MA']:
  display_summary( id )
 
 ## 14 ##
 coauthors[u'Back T'] & coauthors['Haasdijk E']
 
 ## 15 ##
 for id in papers_of_author['Eiben AE'] - papers_of_author['Haasdijk E']:
  display_summary( id )
 
 ## 16 ##
 authors = [ 'Dorigo M', 'Trianni V', 'Lenaerts T' ]
 group_publications = reduce( set.union, [ papers_of_author[a] for a in authors ], set() )
 for id in list(group_publications)[5:10]:
  display_summary( id )
 
 ## 17 ##
 print 'Number of nodes: %8d (node == author)' % len(coauthors)
 print 'Number of links: %8d (link == collaboration between the two linked authors on at least one paper)'  \
  % sum( len(cas) for cas in coauthors.itervalues() )
 
 ## 18 ##
 plt.hist( x=[ len(ca) for ca in coauthors.itervalues() ], bins=range(55), histtype='bar', align='left', normed=True )
 plt.xlabel('number of collaborators')
 plt.ylabel('fraction of scientists')
 plt.xlim(0,50);
 plt.show()
 
 ## 20 ##
 paper_id = 20949101
 refs = { id : Summaries[id].title for id in cited_by[20949101] }
 print len(refs), 'references identified for the paper with id', paper_id
 refs
 
 ## 21 ##
 print { id : Summaries.get(id,['??'])[0]  for id in papers_citing[paper_id] }
 
 ## 22 ##
 paper_id2 = 23903782
 refs2 = { id : Summaries[id].title for id in cited_by[paper_id2] }
 print len(refs2), 'references identified for the paper with id', paper_id2
 refs2
 
 ## 23 ## => DEPENDS ON 21
 # Counter built over list of papers cited by papers that cite a given id
 cocited = Counter([
  ref
  for citers in papers_citing[ paper_id ]
  for ref in cited_by[ citers ]
  if ref != paper_id
  ])
 
 # discard papers cited only once
 cocited = { id : nr_cocits for (id, nr_cocits) in cocited.iteritems() if nr_cocits > 1 }
 
 
 for (id, times_co_cited) in sorted( cocited.items(), key=lambda i:i[1], reverse=True ):
  display_summary( id, ', nr. co-citations: %d' % times_co_cited )
 
 ## 24, 25,26,27,28,29,30 ##
 display_summary( Ids[-1] )
 print papers_citing[ 21373130 ]
 print 21373130 in cited_by
 print cited_by[ 21373130 ] # Fixed
 print 21373130 in cited_by
 
 ## 30 ## Fixes the above 'cited_by[ID]' KeyError
 print cited_by_paper(21373130)

 
 ## 31 ##
 print 'Number of core ids %d (100.00 %%)' % len(Ids)
 
 with_cit = [ id for id in Ids if papers_citing[id]!=[] ]
 print 'Number of papers cited at least once: %d (%.2f %%)' % (len(with_cit), 100.*len(with_cit)/len(Ids))
 
 isolated = set( id for id in Ids if papers_citing[id]==[] and id not in cited_by )
 print 'Number of isolated nodes: %d (%.2f %%)\n\t'   \
       '(papers that are not cited by any others, nor do themselves cite any in the dataset)'% (
     len(isolated), 100.*len(isolated)/len(Ids) )
 
 noCit_withRefs = [ id for id in Ids if papers_citing[id]==[] and id in cited_by ]
 print 'Number of dataset ids with no citations, but known references: %d (%.2f %%)' % (
     len(noCit_withRefs), 100.*len(noCit_withRefs)/len(Ids))
 
 print '(percentages calculated with respect to just the core ids (members of `Ids`) -- exclude outsider ids)\n'
 
 
 ### 32 ## => DEPENDS ON 31
 Ids_set    = set( Ids )
 citing_Ids = set( cited_by.keys() ) # == set( c for citing in papers_citing.itervalues() for c in citing )
 
 outsiders = citing_Ids - Ids_set    # set difference: removes from `citing_Ids` all the ids that occur in `Ids_set`
 nodes     = citing_Ids | Ids_set - isolated     # set union, followed by set difference
 
 print 'Number of (non-isolated) nodes in the graph: %d\n\t(papers with at least 1 known citation, or 1 known reference)' % len(nodes)
 print len( citing_Ids ), 'distinct ids are citing papers in our dataset.'
 print 'Of those, %d (%.2f %%) are ids from outside the dataset.\n' % ( len(outsiders), 100.*len(outsiders)/len(citing_Ids) )
 
 ### 33 ## => DEPENDS ON 31/32
 all_cits      = [ c for citing in papers_citing.itervalues() for c in citing ]
 outsider_cits = [ c for citing in papers_citing.itervalues() for c in citing if c in outsiders ]
 
 print 'Number of links (citations) in the graph:', len(all_cits)
 print 'A total of %d citations are logged in the dataset.' % len(all_cits)
 print 'Citations by ids from outside the dataset comprise %d (%.2f %%) of that total.\n' % (
     len(outsider_cits),
     100.*len(outsider_cits)/len(all_cits) )
 
 ### 34 ##
 nr_cits_per_paper = [ (id, len(cits)) for (id,cits) in papers_citing.iteritems() ]
 
 for (id, cits) in sorted( nr_cits_per_paper, key=lambda i:i[1], reverse=True )[:10]:
  display_summary( id, ', nr. citations: %d' % cits )
  
 ## 35 ##
 G = nx.DiGraph(cited_by)

 ## 36 ##
 #print nx.info(G)
 #print nx.is_directed(G)
 #print nx.density(G)

 ## 37 ## => DEPENDS ON 31
 G.add_nodes_from(isolated)
 
 ## 38 ## => DEPENDS ON 37
 print nx.info(G)
 print nx.is_directed(G)
 print nx.density(G)
 
 ## Q1 ##
 degrees = G.in_degree()
 values = sorted(set(degrees.values()))
 plt.hist(x = [degrees.values().count(x) for x in values], bins=range(55),\
          histtype='bar', align='left', normed=True)
 plt.xlabel('Degree')
 plt.ylabel('Number of Nodes')
 plt.title('Network of Citations of Scientific Papers')
 plt.xlim([0,50])
 plt.show
 
 ## Q2 ##
 # Save pagerank for papers
 papers_pagerank = nx.pagerank_scipy(G)
 print papers_pagerank[11237011]
 
 # Save hubs and Authority Scores
 h,a = nx.hits_scipy(G)
 for (id, hubs) in h.iteritems():
  papers_hub[id] = hubs
 for (id, auth) in a.iteritems():
  papers_auth[id] = auth
 
 