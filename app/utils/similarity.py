"""
Utilidades para cálculo de similaridade entre embeddings
"""
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity


def calculate_cosine_similarity(embedding1: list, embedding2: list) -> float:
    """
    Calcula a similaridade de cosseno entre dois embeddings
    
    Args:
        embedding1: Primeiro vetor de embedding
        embedding2: Segundo vetor de embedding
        
    Returns:
        Similaridade de cosseno (valor entre -1 e 1)
    """
    emb1 = np.array(embedding1).reshape(1, -1)
    emb2 = np.array(embedding2).reshape(1, -1)
    
    similarity = cosine_similarity(emb1, emb2)[0][0]
    
    return float(similarity)


def normalize_embedding(embedding: list) -> list:
    """
    Normaliza um embedding para ter norma unitária
    
    Args:
        embedding: Vetor de embedding
        
    Returns:
        Embedding normalizado
    """
    emb = np.array(embedding)
    norm = np.linalg.norm(emb)
    
    if norm > 0:
        emb = emb / norm
    
    return emb.tolist()
