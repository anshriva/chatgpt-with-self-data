import os
import sys
from flask_cors import CORS 
from flask import Flask, request, jsonify
from langchain.chains import ConversationalRetrievalChain
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import DirectoryLoader, TextLoader, JSONLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.indexes import VectorstoreIndexCreator
from langchain.indexes.vectorstore import VectorStoreIndexWrapper
from langchain.llms import OpenAI
from langchain.vectorstores import Chroma

PERSIST = True

query = None

if PERSIST and os.path.exists("persist"):
    print("Reusing index...\n")
    vectorstore = Chroma(persist_directory="persist", embedding_function=OpenAIEmbeddings())
    index = VectorStoreIndexWrapper(vectorstore=vectorstore)
else:
    loader = DirectoryLoader("data/", glob='**/*.json', show_progress=True, loader_cls=TextLoader)

    if PERSIST:
        index = VectorstoreIndexCreator(vectorstore_kwargs={"persist_directory": "persist"}).from_loaders([loader])
    else:
        index = VectorstoreIndexCreator().from_loaders([loader])

chain = ConversationalRetrievalChain.from_llm(
    llm=ChatOpenAI(model="gpt-3.5-turbo"),
    retriever=index.vectorstore.as_retriever(search_kwargs={"k": 1}),
)

chat_history = []

app = Flask(__name__)
CORS(app) 

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    query = data.get('prompt', None)

    if not query:
        return jsonify({"error": "No prompt provided"}), 400

    result = chain({"question": query, "chat_history": chat_history})
    response = {"answer": result['answer']}
    chat_history.append((query, result['answer']))
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=False)
