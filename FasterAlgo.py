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


def longest_cubic_subsequence(S):

    n = len(S)
    top = n // 3

    if top == 0:
        return ""

    # Check whether the input already contains three identical blocks.
    if n % 3 == 0 and S[:top] == S[top:2 * top] == S[2 * top:]:
        return S[:top]

    # Precalculate character frequencies.
    pref = _prefix_counts(S)
    letters = list(pref)

    # Store divisions and their maximum possible common subsequence lengths.
    candidates = []

    # Try every possible pair of cut positions.
    for s1 in range(1, n - 1):

        for e in range(s1 + 1, n):

            # Calculate the maximum possible common subsequence length.
            total = 0

            for c in letters:
                pc = pref[c]

                total += min(
                    pc[s1],
                    pc[e] - pc[s1],
                    pc[n] - pc[e]
                )

            # The shortest section is another upper bound.
            upper = min(total, s1, e - s1, n - e)

            # Store the division only if it might improve the answer.
            if upper > 0:
                candidates.append((upper, s1, e))

    # Examine divisions with the greatest potential first.
    candidates.sort(reverse=True)

    best = ""

    for upper, s1, e in candidates:

        # No remaining division can improve the current answer.
        if upper <= len(best):
            break

        # Create the three sections, shortest first.
        A, B, C = sorted(
            [S[:s1], S[s1:e], S[e:]],
            key=len
        )

        # Allow the full LCS search.
        X = lcs3_bounded(A, B, C, len(A))

        # Update the best answer.
        if len(X) > len(best):
            best = X

    return best



def main():
    if len(sys.argv) > 1:
        with open(sys.argv[1], "r") as f:
            S = f.read().strip()
    else:
        S = sys.stdin.read().strip()
    X = longest_cubic_subsequence(S)
    print("Input sequence:", S)
    print("Repeated block X:", X)
    print("Longest cubic subsequence:", X * 3)
    print("Length:", 3 * len(X))



if __name__ == "__main__":
    main()