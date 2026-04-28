from langchain_core.runnables import RunnableLambda
def Retriever(db):
    retriever=db.as_retriever(
        search_kwargs={"k": 3}
    )
    def get_unique_docs(queries):
        for q in queries:
            docs=(retriever.invoke(q))
        unique_docs={}
        for doc in docs:
            if doc.page_content not in unique_docs:
                unique_docs[doc.page_content]=doc
        return list(unique_docs.values())  
    return RunnableLambda(get_unique_docs())