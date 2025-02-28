---

# 📌 RAG App

---

## 🛠️ Prerequisites  

Before starting, ensure you have the following installed on your system:  

- [Docker](https://www.docker.com/get-started) (Ensure Docker Desktop is running)  
- [VS Code](https://code.visualstudio.com/)  
- [VS Code Remote - Containers Extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers)  
- [Git](https://git-scm.com/)  
- OpenAI API Key  

---

## 🚀 Setup Guide  

### 1️⃣ Clone the Repository  

Open a terminal and run:  

```bash
git clone https://github.com/Aarav-Khanna/RAG-App.git
cd RAG-App
```

---

### 2️⃣ Open in VS Code with Docker  

1. Open **VS Code**, navigate to the `RAG-App` folder.  
2. Open the Command Palette (`Ctrl+Shift+P` or `Cmd+Shift+P` on Mac) and search for:  
   ```
   Remote-Containers: Reopen in Container
   ```
3. Select this option. VS Code will build and open the project inside the container.  

📌 **Note:** If you don’t see this option, ensure that the **Remote - Containers** extension is installed.  

---

### 3️⃣ Configure OpenAI API Key  

Since `docker-compose.yml` expects environment variables, follow these steps:  

#### ➤ Set the API Key in `.env` (Recommended)  

1. Inside the project folder, create a `.env` file:  

   ```bash
   touch .env
   ```

2. Add your API key and base URL:  

   ```plaintext
   OPENAI_API_KEY=your-api-key-here
   OPENAI_BASE_URL=https://api.ai.it.cornell.edu/
   TZ=America/New_York
   ```

3. Restart the container:  

   ```bash
   docker-compose up --build
   ```

Now, your API key will be automatically loaded inside the container.  

---
## Overview of RAG App  

This application demonstrates **Retrieval Augmented Generation (RAG)** using **LangChain** and **OpenAI**. Below is a high-level overview of the main steps performed in the `rag_app.py` code:

1. **File Upload**  
   - Users can upload multiple PDF or TXT files simultaneously through Streamlit’s `file_uploader`.
   - The application detects the file type and uses an appropriate parser:
     - **PDF**: Parsed by iterating over each page using `PdfReader`.
     - **TXT**: Simply decoded as UTF-8 text.

2. **Chunking and Text Splitting**  
   - Each document’s text is broken into smaller, more manageable pieces (chunks) via the `RecursiveCharacterTextSplitter`.
   - You can control the chunk size (`chunk_size=100` in the example) and overlap (`chunk_overlap=10`). This helps maintain context between chunks.

3. **Embedding & Vector Storage**  
   - The text chunks are embedded using an OpenAI embedding model (`openai.text-embedding-3-large`).
   - These embeddings are stored in a **Chroma** in-memory vector database, which allows for fast similarity searches later on.

4. **User Queries & Similarity Search**  
   - When a user asks a question in the Streamlit chat input:
     1. The question is used to query the vector database.
     2. The database returns the top-k most relevant chunks (`k=3` by default).

5. **OpenAI GPT-4 Prompt Construction**  
   - The retrieved chunks are combined into a “Context” block, which is then passed to the GPT-4 model (or `openai.gpt-4o` in the example code) along with the user’s question. 
   - This ensures that GPT-4 has direct, relevant context at prompt time, increasing the accuracy and relevance of its response.

6. **Answer Generation**  
   - GPT-4 generates a response (`ChatCompletion` endpoint).
   - The final answer is displayed in the Streamlit chat interface, preserving the conversational flow.

Overall, this **RAG** workflow enables the model to reference specific, retrieved pieces of text from your uploaded documents rather than requiring the entire file content in each prompt—leading to more efficient and contextually grounded responses. 

Once your container is running and you execute:
```bash
streamlit run rag_app.py
```
you’ll be able to open your browser (typically at `http://localhost:8501`) to:
- Upload documents (.pdf or .txt),
- **Process** them to create embeddings,
- **Ask questions** in the chat interface,
- And receive answers derived from the specific content of those documents.

