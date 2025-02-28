import streamlit as st
import os
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.docstore.document import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from pypdf import PdfReader
import openai

openai.api_key = os.environ.get("OPENAI_API_KEY")

def parse_pdf(file) -> str:
    pdf = PdfReader(file)
    text = []
    for page in pdf.pages:
        text.append(page.extract_text() or "")
    return "\n".join(text)

def parse_txt(file) -> str:
    return file.read().decode("utf-8")

def embed_documents(docs):
    embeddings = OpenAIEmbeddings(model = "openai.text-embedding-3-large")
    vectordb = Chroma.from_documents(docs, embeddings)
    return vectordb

def get_relevant_chunks(question, vectordb, k=3):
    if vectordb is None:
        return []
    docs = vectordb.similarity_search(question, k=k)
    return docs

def generate_answer(question, relevant_chunks):
    context_text = "\n\n".join([doc.page_content for doc in relevant_chunks])
    print(context_text)

    system_prompt = f"You are a helpful assistant. Use the following context to answer the question.\n\nContext:\n{context_text}"
    user_prompt = f"Question: {question}"

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]

    response = openai.chat.completions.create(
        model="openai.gpt-4o",  
        messages=messages,
        temperature=0.7
    )

    answer = response.choices[0].message.content
    return answer


st.title("📝 Multi-File Q&A with OpenAI")

if "messages" not in st.session_state:
    st.session_state["messages"] = []
if "vectordb" not in st.session_state:
    st.session_state["vectordb"] = None

uploaded_files = st.file_uploader(
    "Upload your documents (PDF or TXT)",
    type=["pdf", "txt"],
    accept_multiple_files=True
)

if st.button("Process Files") and uploaded_files:
    all_docs = []
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=100,   
        chunk_overlap=10 
    )

    for uploaded_file in uploaded_files:
        if uploaded_file.type == "application/pdf":
            file_text = parse_pdf(uploaded_file)
        else:
            file_text = parse_txt(uploaded_file)

        chunks = text_splitter.split_text(file_text)

        docs = [Document(page_content=chunk, metadata={"source": uploaded_file.name})
                for chunk in chunks]
        all_docs.extend(docs)

    st.session_state["vectordb"] = embed_documents(all_docs)
    st.success(f"Processed {len(uploaded_files)} file(s) and created embeddings.")

for msg in st.session_state["messages"]:
    st.chat_message(msg["role"]).write(msg["content"])

user_question = st.chat_input("Ask something about the documents")
if user_question:
    st.chat_message("user").write(user_question)
    st.session_state["messages"].append({"role": "user", "content": user_question})

    relevant_chunks = get_relevant_chunks(user_question, st.session_state["vectordb"], k=3)

    if relevant_chunks:
        answer = generate_answer(user_question, relevant_chunks)
    else:
        answer = "No documents have been processed or no relevant chunks were found."

    st.session_state["messages"].append({"role": "assistant", "content": answer})
    st.chat_message("assistant").write(answer)
