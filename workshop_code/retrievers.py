from workshop_code.common_components.vectorizers import Vectorizer
from workshop_code.common_components.wcs_client_adapter import WcsClientAdapter

class NaiveRetriever:
  
  def __init__(self, vectorizer: Vectorizer):
    self._wcs_client_adapter = WcsClientAdapter()
    self._vectorizer = vectorizer
    
  def retrieve(self, query: str) -> str:
    
    # Vectorize the query we are inputting
    query_vector = self._vectorizer.vectorize_query(query)

    # retrieve here is retrieving data from WCS.
    # Need to understand retrieve better
    retrieved_chunks_list = self._wcs_client_adapter.retrieve(query_vector, k=5)
    formatted_chunks = "\n\n".join(chunk for chunk in retrieved_chunks_list)
    return formatted_chunks