4.3
1. Which method performs better for this query? Why?

I think both methods don't perform well for the queries because they don't return the products users look for, although they are somehow related. 

2. Are there cases where BM25 fails but semantic search succeeds?

Yes, for query "yoga mat 6mm non-slip", BM25 returns "Gun Bundle", which is not related at all. 

3. Are there cases where semantic search fails?

Yes, for query "waterproof 2 person camping tent", semantic search returns "Helmet". 

4. Are the top results actually useful for the user’s intent?

Not really, although some are related to user's intent, they are not exactly what users want. 

5. How does performance vary across query types (keyword vs semantic vs complex)?

keyword and semantic tend to have a bit better performance than complex. 


4.4
1. What are the strengths and weaknesses of each method?

For keyword queries, BM25 performs better because it matches the keywords exactly, it's not good at understanding underlying meaings. For semantic queries, semantic search performs better because it understands the underlying meanings, but it requires more computational resources. 

2. What types of queries are challenging for both methods?

Those complex queries are challenging for both methods because they may include logics such as less than $100, which is hard to be understood. 

3. Where might more advanced methods (e.g., RAG or reranking) help?
(Adopted from GPT)
A reranker looks at the query and the document simultaneously to determine if they truly match. It’s good at filtering out the near-misses that Semantic search often includes.