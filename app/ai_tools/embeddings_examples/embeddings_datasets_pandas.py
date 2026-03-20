import pandas as pd
from google import genai

from app.core.config import settings


def get_embedding(text, model="gemini-embedding-001"):
    client = genai.Client(api_key=settings.GOOGLE_API_KEY)
    # https://ai.google.dev/gemini-api/docs/migrate#embed-content
    embeddings = client.models.embed_content(
        model=model,
        contents=text,
    )
    return embeddings.embeddings[0].values

if __name__ == "__main__":
    df = pd.read_csv("people2m.csv")
    df = df[['First Name']].head(5).copy()
    df.rename(columns={'First Name': 'first_name'}, inplace=True)
    df = df.sample(frac=1)
    print(df)
    df['embedding'] = df['first_name'].apply(lambda x: get_embedding(x))
    print(df)
    df.to_csv("embedding_people2m.csv", index=False)
