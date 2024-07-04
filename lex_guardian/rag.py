import os
from dotenv import load_dotenv
from lex_guardian.utils import load_config
from qdrant_client import QdrantClient
from langchain_community.vectorstores import Qdrant
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.llms import HuggingFaceEndpoint
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough


def setup_environment():
    os.chdir("c:\\Users\\Spectra\\LexGuardian")
    config = load_config()
    load_dotenv()
    return config


def process_documents(config):
    loader = PyPDFLoader(config["data"]["data_path"])
    documents = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    return text_splitter.split_documents(documents)


def setup_vectorstore(config, text_chunks):
    url = config["vectorstore"]["url"]
    api_key = os.getenv("QDRANT_API_KEY")
    model_name = "BAAI/bge-base-en-v1.5"
    embeddings = HuggingFaceEmbeddings(model_name=model_name)
    return Qdrant.from_documents(
        text_chunks,
        embeddings,
        url=url,
        prefer_grpc=True,
        api_key=api_key,
        collection_name="constitution",
    )


def instantiate_db(config):
    url = config["vectorstore"]["url"]
    api_key = os.getenv("QDRANT_API_KEY")
    model_name = "BAAI/bge-base-en-v1.5"
    collection_name = "constitution"
    embeddings = HuggingFaceEmbeddings(model_name=model_name)
    client = QdrantClient(url, api_key=api_key)
    return Qdrant(client, collection_name, embeddings)


def setup_retriever(vectorstore):
    return vectorstore.as_retriever(search_kwargs={"k": 5})


def setup_llm():
    repo_id = "mistralai/Mixtral-8x7B-Instruct-v0.1"
    return HuggingFaceEndpoint(repo_id=repo_id, temperature=0.3)


def setup_rag_chain(retriever, llm):
    prompt = """
    You are a knowledgeable and friendly legal assistant with expertise in Kenyan law. Your task is to help the common person understand various aspects of Kenyan law in a simple, clear, and easy-to-understand manner.

    When responding, please follow these guidelines:

    - Simplify Legal Terms: Use simple language and avoid legal jargon. When legal terms must be used, provide clear explanations.
    - Provide Examples: Where possible, use examples or analogies to make complex legal concepts easier to grasp.
    - Be Concise: Keep your responses short and to the point, but ensure they are complete and informative.
    - Be Neutral and Informative: Provide information neutrally without offering personal opinions or legal advice.

    Use the following pieces of retrieved context to answer the question.

    Question: {question}
    Context: {context}
    Answer:
    """
    prompt_template = PromptTemplate.from_template(prompt)

    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)

    return (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt_template
        | llm
        | StrOutputParser()
    )


def stream_response(rag_chain, query):
    for chunk in rag_chain.stream(query):
        print(chunk, end="", flush=True)


def main():
    config = setup_environment()
    vectorstore = instantiate_db(config)
    retriever = setup_retriever(vectorstore)
    llm = setup_llm()
    rag_chain = setup_rag_chain(retriever, llm)

    query = "What are the rights of an arrested person and what section of the constitution guarantees these rights?"
    stream_response(rag_chain, query)


if __name__ == "__main__":
    main()
