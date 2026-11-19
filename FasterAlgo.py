"""
Liam Heasman
LKH981
11283893
"""

import sys

def lcs3_bounded(A, B, C, D):

    #gets the string lengths
    m, n1, n2 = len(A), len(B), len(C)

    #uses shortest string as a reference
    D = min(D, m)

    # prev[c][x] = largest position p < x with C[p] == c, else -1
    prev = {}

    #iterates through every character in A removing any characters that are duplicates
    for i in set(A):

        #creates a list that initializes everything to be -1 to track matching characters
        row, last = [-1] * (n2 + 1), -1

        #loops through every character in i
        for x in range(n2 + 1):

            #stores most recent position of character i before position x
            row[x] = last

            #checks if x is a valid character positon in i
            if x < n2 and C[x] == i:
                last = x

        #stores the completed position table inside the dictionary
        prev[i] = row

    #represent an impossible state for dynamic programming table
    NEG = -1

    #creates list that will store DP table
    L = [None] * (m + 1)

    #initialized base case of the DP table
    L[m] = [[n2 if d == 0 else NEG for d in range(D + 1)] for _ in range(n1 + 1)]


    #iterates backwards through string A
    for i in range(m - 1, -1, -1):

        #calculates how many characters are remaining in A starting from position i
        rem = m - i

        #determines maximum number of characters that can be skipped from remaining portion of A
        dmax = min(D, rem)

        #stores the results  for the current position A
        Li, Lnext = [None] * (n1 + 1), L[i + 1]

        #stores the current character from A
        a, pa = A[i], prev[A[i]]

        #iterates backwards throiugh the positions in B
        for j in range(n1, -1, -1):

            #creates a new row for the current position in B
            row = [NEG] * (D + 1)

            #retrieves the preivously calculated row for th next position in A
            nj = Lnext[j]

            #iterates through every valid number of skipped characters
            for d in range(dmax + 1):

                #checks whteher the number of skipped characters equals the number of characters remaining in A
                if d == rem:                      # nothing left to match
                    
                    #marks state as valid
                    row[d] = n2
                    continue

                #if at least one skip is allowed, it looks at the state for the next position in A with one fewer remaining skip
                #if d is zero, skipping is not allowed and the result is marked invalid
                best = nj[d - 1] if d >= 1 else NEG      # skip A[i]

                #checks whether there are still characters remaining in B
                if j < n1:

                    #retrieves the result from the next position in B
                    v = Li[j + 1][d]                     # skip B[j]

                    #checks whether skipping the character in B produces a better result than the current best position
                    if v > best:
                        best = v

                    #checks whether the current character in A matches the current character in B
                    #if they do not match then this particular matching option cannnot be used
                    if a == B[j]:     

                        #looks at state after advancing one position in both A and B
                        v = Lnext[j + 1][d]
                        
                        #checks if resulting state is valid
                        if v >= 0:
                            #uses previous occurance table to find the last ocurance of character a before positoon v in C
                            p = pa[v]

                            #checks to see if it produces a better result
                            if p > best:
                                best = p
                #stores the best result for the current dyanmic programming state
                row[d] = best
            #stores the completed row for the current position B
            Li[j] = row
        #stores the completed dynamic programming table for the current position in A
        L[i] = Li

    #searches through all possible skip counts starting from zero
    d = next((d for d in range(D + 1) if L[0][0][d] >= 0), None)
    if d is None:
        return None

    #calculates the length of the common subsequence
    k = m - d

    #list to store the resulting subsequence and initialize i and j to 0
    res, i, j = [], 0, 0

    #reconsutructs the subsequence until all k matched characters have been recovered
    while k > 0:

        #retrieves the current dnyamic programming result
        v = L[i][j][d]

        #checks whether the current character in A was skipped when calculating the state
        if d >= 1 and L[i + 1][j][d - 1] == v:
            i += 1
            d -= 1

        #if character in A was not skipped checks whether the current character in B was skipped
        elif j < n1 and L[i][j + 1][d] == v:
            j += 1

        #if neither are skipped, the current characters must be apart of the common subsequence. 
        else:
            res.append(A[i])
            i += 1
            j += 1
            k -= 1

    #combines all the characters into one string
    return "".join(res)