from openai import OpenAI
import os
from typing import List

# This is temporary, remove later
OPENAI_CLIENT = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
EMBEDDING_MODEL = "text-embedding-3-small"

class Vectorizer:

    # This is for contents/texts, hence why need text splits
    # Looks similar with vectorize_query, only difference is that one is for query only
    # no text splits
    def vectorize_text_splits(self, text_splits: List[str]) -> List[List[float]]:
        
        # model can be anything available
        model = 'text-embedding-3-small'
        response = OPENAI_CLIENT.embeddings.create(input=text_splits, model=model)
        
        embeddings = []
        
        # Each text split is an item hence why we have to loop this
        for i in range(0, len(response.data)):
            embeddings.append(response.data[i].embedding)
        return embeddings
    
    def vectorize_query(self, query: str) -> List[float]:
        
        model = 'text-embedding-3-small'
        response = OPENAI_CLIENT.embeddings.create(input=query, model=model)
        query_vector = response.data[0].embedding
        return query_vector