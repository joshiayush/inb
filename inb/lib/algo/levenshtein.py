# MIT License
#
# Copyright (c) 2019 Creative Commons
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
# OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

from ..utils import _type


def levenshtein(string1: str, string2: str) -> int:
    """Function levenshtein() returns the edit distance between the two given strings.

    :Args:
        - string1: {str} first string.
        - string2: {str} second string.

    :Returns:
        - {int} edit distance.
    """
    if not isinstance(string1, str):
        raise TypeError("levenshtein: %(type)s type object is a invalid argument, requires string!" % {
                        "type": _type(string1)})
    if not isinstance(string2, str):
        raise TypeError("levenshtein: %(type)s type object is a invalid argument, requires string!" % {
                        "type": _type(string2)})

    # Our optimal solution matrix that will hold the optimal solution
    # of converting one string into another
    optimal_solution_matrix: list = [
        [-1 for i in range(len(string2))] for j in range(len(string1))]

    def levenshteinDistanceTopDown(string1Index: int, string2Index: int) -> int:
        """Function levenshteiDistanceTopDown() is the actual reccursive program to find the edit
        distance between two strings.

        :Args:
            - string1Index: {int} first string index for this reccursive level.
            - string2Index: {int} second string index for this reccursive level.

        :Returns:
            - {int} edit distance.
        """
        # Using the parent function string1 variable
        nonlocal string1
        # Using the parent function string2 variable
        nonlocal string2
        # Using the parent function optimal_solution_matrix variable
        nonlocal optimal_solution_matrix

        if string1Index < 0:
            # If string1 is NULL, it is all insertion to get string1 to string2
            return string2Index + 1

        if string2Index < 0:
            # If string2 is NULL, it is all insertion to get string2 to string1
            return string1Index + 1

        if not optimal_solution_matrix[string1Index][string2Index] == -1:
            # Return the globally optimized solution if we already have one
            return optimal_solution_matrix[string1Index][string2Index]

        if string1[string1Index] == string2[string2Index]:
            # Character match; no repair needs to take place no addition to distance
            optimal_solution_matrix[string1Index][string2Index] = levenshteinDistanceTopDown(
                string1Index - 1, string2Index - 1)

            # Return the optimized solution
            return optimal_solution_matrix[string1Index][string2Index]

        # We have a character mismatch. Remember we want to transform string1 into
        # string2 and we hold the i'th character of string1 and the j'th character
        # of string2

        # Deletion:
        #   Find levenshtein distance of string1[0...(i - 1)] => string2[0...j] i'th
        #   character of string1 is deleted
        delete_cost: int = levenshteinDistanceTopDown(
            string1Index - 1, string2Index)

        # Insertion:
        #   Find levenshtein distance of string1[0...j] => string2[0...(j - 1)] we then
        #   insert string2[j] into string2 to refain string2[0...j]
        insert_cost: int = levenshteinDistanceTopDown(
            string1Index, string2Index - 1)

        # Replace:
        #   Find levenshtein distance of string1[0...(i -1)] => string2[0...(j - 1)] we
        #   then insert string2[j] as i'th character of string1 effectively substituting
        #   it
        replace_cost: int = levenshteinDistanceTopDown(
            string1Index - 1, string2Index - 1)

        # We want to take the minimum of these three costs to fix the problem (we add 1
        # to the minimum to symbolize performing the action)
        optimal_solution_matrix[string1Index][string2Index] = min(
            delete_cost, min(insert_cost, replace_cost)) + 1

        # Return the optimized solution
        return optimal_solution_matrix[string1Index][string2Index]

    # Commence the recurrence to ascertain the globally optimized solution to convert
    # string1 into string2
    return levenshteinDistanceTopDown(len(string1) - 1, len(string2) - 1)
