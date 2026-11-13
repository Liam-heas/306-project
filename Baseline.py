"""
Liam Heasman
LKH981
11283893
"""
# Longest Common Subsequence (LCS) for Longest Cubic Sequence (LCubS):

import sys


# this finds the longest common subsequence shared by three sequences
def lcs_three(A, B, C):

    #gets the length of each sequence
    a = len(A)
    b = len(B)
    c = len(C)

    # Create a 3D table to store the LCS lengths for different
    # combinations of prefixes from A, B and C.
    dp = [[[0] * (c + 1) for _ in range(b + 1)]
          for _ in range(a + 1)]


    # Fills in the table by comparing characters from each sequence.
    for i in range(1, a + 1):
        for j in range(1, b + 1):
            for k in range(1, c + 1):

                # If all characters match, adds one to the
                # result from the previous positions in all sequences.
                if A[i - 1] == B[j - 1] == C[k - 1]:
                    dp[i][j][k] = 1 + dp[i - 1][j - 1][k - 1]

                # If characters do not match, use largest result
                # by removing one character from any of the three sequences.
                else:
                    dp[i][j][k] = max(
                        dp[i - 1][j][k],
                        dp[i][j - 1][k],
                        dp[i][j][k - 1]
                    )

    # iterate backwards through table to find which characters
    # make up the longest common subsequence.
    result = []

    i = a
    j = b
    k = c

    while i > 0 and j > 0 and k > 0:

        # If current characters match, they are part of the LCS.
        # Move diagonally backwards through the table.
        if A[i - 1] == B[j - 1] == C[k - 1]:
            result.append(A[i - 1])
            i -= 1
            j -= 1
            k -= 1

        # Otherwise, move in the direction of the largest DP value.
        # helps to trace back the choices that produced the LCS.
        elif dp[i - 1][j][k] >= dp[i][j - 1][k] and \
             dp[i - 1][j][k] >= dp[i][j][k - 1]:
            i -= 1


        elif dp[i][j - 1][k] >= dp[i][j][k - 1]:
            j -= 1

        else:
            k -= 1


    # reverse characters to get the subsequence in its original order.
    result.reverse()


    return result



# finds the longest cubic sequence of S
def longest_cubic_subsequence(S):
        
        n = len(S)

        #stores the best repeated block
        best_block = []

        #stores the length of the best repeated block
        best_length = 0

        # Tries every possible pair of dividing positions.
        for p in range(n + 1):
            for q in range(p, n + 1):
        
                # Splits original sequence into three sections.
                A = S[:p]
                B = S[p:q]
                C = S[q:]
        
                # Finds longest subsequence while keeping the original order.
                block = lcs_three(A, B, C)
        
                # Update best block if longer one is found
                if len(block) > best_length:
                    best_length = len(block)
                    best_block = block
        
         # Repeats best block three times to form cubic subsequence
        cubic = best_block * 3
        
        return best_block, cubic


def main():
    return


if __name__ == "__main__":
    main()