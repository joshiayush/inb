# Levenshtein Distance Service

This service provides a function that takes in two strings and returns the minimum edit distance between them.

This document has the following section:

- [System Call Interface](#system-call-interface)

## System Call Interface

- **Function levenshtein**

  ```python
  def levenshtein(string1: str, string2: str) -> int:
  ```

  > This function returns the edit distance between two given strings.
  > <br><br>
  > This function initially creates an optimal solution matrix to be used to generate solutions on the basis of sub-problems. This
  > matrix is then used by an internal nested function called `levenshteinDistanceTopDown` to finally generate a globally optimized
  > solution matrix, this nested function is the actual implementation of the reccurence relation that we ascertain in levenshtein
  > distance algorithm.
