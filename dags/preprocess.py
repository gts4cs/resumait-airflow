from langchain_community.document_loaders.csv_loader import CSVLoader
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS


def csv_to_vectorDB(data_path):
    """
    Convert to CSV data into VectorDB
    Parameters :
        datapath: destination of CSV data
    """
    # Load CSV data
    loader = CSVLoader(file_path=data_path)
    docs = loader.load()

    # Model define by using OpenSource Model
    modelPath = "distiluse-base-multilingual-cased-v1"
    model_kwargs = {"device": "cpu"}
    encode_kwargs = {"normalize_embeddings": False}
    embeddings = HuggingFaceEmbeddings(
        model_name=modelPath, model_kwargs=model_kwargs, encode_kwargs=encode_kwargs
    )
    # Convert CSV into VectorDB
    db = FAISS.from_documents(docs, embedding=embeddings)
    db.save_local("./data/FaissVectorDB")
