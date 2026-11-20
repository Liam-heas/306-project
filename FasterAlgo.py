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

#calculates the number of occurences of each character throughout the input string
def _prefix_counts(S):
    
    pref = {}

    #loops through every unique character in the input string
    for c in set(S):

        arr= [0] * (len(S) + 1)

        #count for number of times current character has appeared
        t = 0

        #iterate through every character in S where i = index, ch =character at index i
        for i, ch in enumerate(S):

            #checks to see if current character is the same as character being counted
            if ch == c:
                t += 1

            #stores current occurence count in prefix array
            arr[i + 1] = t

        #saves completed prefix count array in dictionary
        pref[c] = arr

    #returns dictionary containing the prefix counts for evry unique character
    return pref


#
def feasible(S, p, pref=None):

    #stores length of input string
    n = len(S)

    #checks minimum block length
    if p <= 0:
        return ""

    #calculate show many characters can be deleted from string while still allowing three copies
    k = n - 3 * p

    #checks to see if input is too short
    if k < 0:
        return None

    #calculates prefix count
    if pref is None:
        pref = _prefix_counts(S)

    #list of unique characters
    letters = list(pref)

    #tests possible positons for first cut in string
    for s1 in range(p, min(p + k, n - 2 * p) + 1):

        #tests possible lengths for second piece
        for s2 in range(p, min(p + k, n - s1 - p) + 1):

            #calculates end of second piece
            e = s1 + s2

            #counter for maximum length of common subsequence
            tot = 0

            #iterates through every unique character
            for c in letters:
                
                #calclulates how many times current character appears in each of the three pieces and adds
                #smalles count
                pc = pref[c]
                tot += min(pc[s1], pc[e] - pc[s1], pc[n] - pc[e])

            #checks to see if total number of matching characters is smaller than required block length
            if tot < p:
                continue

            #creates three pieces of the original string with A being shortest and C longest
            A, B, C = sorted([S[:s1], S[s1:e], S[e:]], key=len)

            #calls the LCS algorithm
            X = lcs3_bounded(A, B, C, len(A) - p)

            #checks to see if it found a valid subsequence
            if X is not None and len(X) >= p:
                return X
            
    #returns none if it didnt find a valid subsequence
    return None




def longest_cubic_subsequence(S):

    #length of input string
    n = len(S)

    #max length of X
    top = n // 3

    #if fewer then 3 char return empty string
    if top == 0:
        return ""
    
    #checks to see if string is made up of three identical blocks
    if n % 3 == 0 and S[:top] == S[top:2 * top] == S[2 * top:]:
        return S[:top]

    #gets prefic counts for every unique character in string
    pref = _prefix_counts(S)

    #checks maximum possible block length
    X = feasible(S, top, pref)

    #ifit finds a valid block nothing else needs to be considered
    if X is not None:
        return X

    
    # F1: doubling to find a feasible p, then binary search the gap
    fail_p, step = top, 1

    #goes until a feasable length is found
    while True:

        #calculates the next block length to test
        p = max(0, top - step)

        #tests to see if block is possible
        X = feasible(S, p, pref)

        #checks whether valid block has been found
        if X is not None:
            good_p = len(X)
            break

        #If the feasibility test fails will record the current block length as an unsuccessful value
        fail_p = p
        step *= 2

    #stores best block 
    best = X

    #Continues searching while there is at least one integer block length between the successful and unsuccessful boundaries.
    while fail_p - good_p > 1:

        #calculates midpoint between successful and unsuccessful boundaries
        mid = (fail_p + good_p) // 2

        #tests whether it can be consutrctued 
        X = feasible(S, mid, pref)

        #checks to see if it can be done
        if X is not None:
            best, good_p = X, len(X)
        else:
            fail_p = mid

    #resturns longest cubic block
    return best

