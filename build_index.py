import os
import json
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer

def build_vector_database():
    model = SentenceTransformer('all-MiniLM-L6-v2')
    database_dir = "database"
    output_dir = "rag_data"
    os.makedirs(output_dir, exist_ok=True)
    
    all_chunks = []
    metadata = []
    
    if os.path.exists(database_dir):
        for folder in os.listdir(database_dir):
            folder_path = os.path.join(database_dir, folder)
            if os.path.isdir(folder_path):
                for file in os.listdir(folder_path):
                    if file.endswith(".txt"):
                        file_path = os.path.join(folder_path, file)
                        with open(file_path, "r", encoding="utf-8") as f:
                            content = f.read().strip()
                            if content:
                                paragraphs = content.split("\n\n")
                                for p in paragraphs:
                                    p_clean = p.strip()
                                    if len(p_clean) > 20:
                                        all_chunks.append(p_clean)
                                        metadata.append({"folder": folder, "file": file})
                                        
    if all_chunks:
        embeddings = model.encode(all_chunks, show_progress_bar=True)
        embeddings = np.array(embeddings).astype("float32")
        
        dimension = embeddings.shape[1]
        index = faiss.IndexFlatL2(dimension)
        index.add(embeddings)
        
        faiss.write_index(index, os.path.join(output_dir, "faiss.index"))
        with open(os.path.join(output_dir, "metadata.json"), "w", encoding="utf-8") as f:
            json.dump(metadata, f, ensure_ascii=False, indent=2)
        with open(os.path.join(output_dir, "chunks.json"), "w", encoding="utf-8") as f:
            json.dump(all_chunks, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    build_vector_database()