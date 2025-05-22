from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import OpenAIEmbeddings
from langchain.chains.question_answering import load_qa_chain
from langchain.chat_models import ChatOpenAI
from langchain.docstore.document import Document

def query_documents(query: str):
    embedding = OpenAIEmbeddings()
    db = FAISS.load_local("data/faiss_index", embeddings=embedding)
    
    docs = db.similarity_search(query, k=4)
    
    llm = ChatOpenAI(temperature=0)
    chain = load_qa_chain(llm, chain_type="stuff")
    
    answer = chain.run(input_documents=docs, question=query)
    
    sources = [{"page": i+1, "content": doc.page_content[:200]} for i, doc in enumerate(docs)]
    return {"answer": answer, "sources": sources}