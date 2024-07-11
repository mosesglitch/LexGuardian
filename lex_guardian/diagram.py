from diagrams import Diagram, Cluster
from diagrams.programming.language import Python
from diagrams.onprem.client import User
from diagrams.onprem.database import PostgreSQL
from diagrams.aws.storage import S3
from diagrams.azure.ml import CognitiveServices

with Diagram("LexGuardian Architecture", show=False, direction="TB"):
    user = User("User")

    with Cluster("Streamlit Web Interface"):
        streamlit = Python("Streamlit App")
        session = Python("Session State")

    with Cluster("RAG System"):
        with Cluster("Setup"):
            env_setup = Python("Environment Setup")
            doc_process = Python("Document Processing")
            vectorstore_setup = Python("Vector Store Setup")
            llm_setup = Python("LLM Setup")
            retriever_setup = Python("Retriever Setup")
            rag_chain_setup = Python("RAG Chain Setup")

        with Cluster("Components"):
            vectorstore = PostgreSQL("Qdrant Vector Store")
            llm = CognitiveServices("HuggingFace LLM")
            pdf_storage = S3("PDF Storage")

    user >> streamlit
    streamlit >> session
    streamlit >> rag_chain_setup

    env_setup >> doc_process >> vectorstore_setup >> retriever_setup >> rag_chain_setup
    llm_setup >> rag_chain_setup
    vectorstore_setup >> vectorstore
    llm_setup >> llm
    doc_process >> pdf_storage

    rag_chain_setup >> llm
    rag_chain_setup >> vectorstore
