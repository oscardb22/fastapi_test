import pandas as pd
import tiktoken

df = pd.read_csv('embedding_people2m.csv')
print(df)
enc = tiktoken.encoding_for_model("text-embedding-3-small")
total_tokens = sum([len(enc.encode(word)) for word in list(df['first_name'])])
print(f"total of tokens: {total_tokens}")
cost_per_token = 0.02 / 1_000_000
estimated_cost = total_tokens * cost_per_token
print(f"Estimated cost in USD: {estimated_cost:.10f}")
