import numpy as np
import pandas as pd

from app.ai_tools.embeddings_examples.embeddings_datasets_pandas import get_embedding


def cosine_similarity(vector_x, vector_y):
    x = np.array(vector_x)
    y = np.array(vector_y)

    if x.ndim != 1 or y.ndim != 1:
        raise ValueError("Both vectors must be one-dimensional")

    if x.shape[0] !=  y.shape[0]:
        raise ValueError("Both vectors must be of the same dimensional")

    dot_product = np.dot(x, y)

    norm_x = np.linalg.norm(x)
    norm_y = np.linalg.norm(y)
    if norm_x == 0 or norm_y == 0:
        return ValueError("One of the vectors is zero.")
    similarity = dot_product / (norm_x*norm_y)
    return similarity


if __name__ == "__main__":
    df = pd.read_csv('embedding_people2m.csv')
    print(df)

    df['embedding'] = df['embedding'].apply(eval).apply(np.array)
    print(df)

    search_term = 'ave'
    search_term_vector = get_embedding(search_term)
    print(search_term_vector)
    df["similarity"] = df["embedding"].apply(lambda x: cosine_similarity(x, search_term_vector))
    df.sort_values(by=['similarity'], ascending=False, inplace=True)
    print(df)
