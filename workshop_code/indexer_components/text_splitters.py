import re
from typing import List

class SimpleCharacterTextSplitter:
  def __init__(self, chunk_size: int, overlap_size: int):
    self.chunk_size = chunk_size
    self.overlap_size = overlap_size
    
  def split_text(self, text: str) -> List[str]:
    # split_text[n] has chunk_size + (overlap_size * n) words
    # [250 words, 275 words, 300 words, 325 words, etc.]
    text_length = len(text.split())
    word_list = text.split()
    result = []
    for x in range(0, text_length, self.chunk_size):
      if x != 0:
        group = word_list[x-self.overlap_size:x + self.chunk_size]
        result.append(' '.join(group))
      else:
        group = word_list[x:x+self.chunk_size]
        result.append(' '.join(group))
    return result
    # raise NotImplementedError("Implement this method and delete this exception.")