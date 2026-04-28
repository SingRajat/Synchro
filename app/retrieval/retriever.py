from langchain_core.runnables import RunnableLambda
from langchain_community.document_compressors.flashrank_rerank import FlashrankRerank

def Retriever(db,bm25_retriever):
    dense_retriever=db.as_retriever(
        search_kwargs={"k": 3}
    )

    reranker=FlashrankRerank(
        top_n=3
    )

    def get_unique_docs(queries):
        doc_scores={}
        for q in queries:
            vector_docs=dense_retriever.invoke(q)
            bm25_docs=bm25_retriever.invoke(q)

            for rank,doc in enumerate(bm25_docs):
                if doc.page_content not in doc_scores:
                    doc_scores[doc.page_content]={"docs":doc,"score":0}
                doc_scores[doc.page_content]["score"]+=1/(rank+60)
            
            for rank,doc in enumerate(vector_docs):
                if doc.page_content not in doc_scores:
                    doc_scores[doc.page_content]={"docs":doc,"score":0}
                doc_scores[doc.page_content]["score"]+=1/(rank+60)

        # 2. Sort outside the query loop, so scores accumulate across all queries
        ranked=sorted(doc_scores.values(),key=lambda x:x["score"], reverse=True )
        top_docs=[item["docs"] for item in ranked][:5]
        
        if not top_docs:
            return []
            
        rerank_docs=reranker.compress_documents(top_docs,query=queries[0])
        return rerank_docs  
    return RunnableLambda(get_unique_docs)