from langchain_core.runnables import RunnableLambda
from langchain_community.retrievers import EnsembleRetriever
def Retriever(db,bm25_retriever):
    dense_retriever=db.as_retriever(
        search_kwargs={"k": 3}
    )

    ensemble=EnsembleRetriever(
        retrievers=[dense_retriever,bm25_retriever],
        weight=[0.5,0.5]
    )
    def get_unique_docs(queries):
        unique_docs={}
        for q in queries:
            docs=(ensemble.invoke(q))
            for doc in docs:
                if doc.page_content not in unique_docs:
                    unique_docs[doc.page_content]=doc
        return list(unique_docs.values())  
    return RunnableLambda(get_unique_docs)
    