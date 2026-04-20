
def Retriever(db):
    retriever=db.as_retriever(
        search_kwargs={"k": 3}
    )
    return retriever