# Top-K
# Limits the model to only consider the K most probable next tokens.
#
# top_k=1 → always picks the single most likely token (deterministic)
# top_k=50 → picks randomly among the top 50 candidates
# Higher K = more creative/random, Lower K = more focused

# Top-P (nucleus sampling)
# Instead of a fixed number of tokens, it picks from the smallest set of tokens whose cumulative probability adds up to P.
#
# top_p=0.9 → considers tokens until their combined probability reaches 90%
# If a few tokens dominate, it considers fewer. If probabilities are spread out, it considers more.
# More adaptive than Top-K

# 🌡️ Temperature
# Controls randomness of outputs. Ranges from 0 to 1 (sometimes 2).
#
# 0 → deterministic, always picks the most likely token
# 1 → more creative and varied
# Use low for factual tasks, high for creative ones

# 🔍 RAG (Retrieval-Augmented Generation)
# A technique to give LLMs access to external knowledge at inference time, without retraining.
# The flow is:
# User query
#    → retrieve relevant docs from a vector DB
#       → inject them into the prompt as context
#          → LLM generates answer grounded in those docs
# Solves two big LLM problems:
#
# Hallucination — the model answers from real retrieved sources
# Knowledge cutoff — you can feed it up-to-date information
#
# It's the backbone of most production AI assistants today.
