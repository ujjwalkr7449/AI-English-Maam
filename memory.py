# memory.py

import chromadb

# ⚡ Create client once
client = chromadb.Client()

# ⚡ No embedding model = no download = faster
collection = client.get_or_create_collection(
    name="user_memory",
    embedding_function=None
)

def save_memory(text):
    try:
        collection.add(
            documents=[text],
            ids=[str(abs(hash(text)))]
        )
    except:
        pass   # avoid crash if duplicate

def get_memories():
    data = collection.get()
    if data and data["documents"]:
        return " ".join(data["documents"])
    return ""