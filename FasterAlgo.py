
"""
Liam Heasman
LKH981
11283893

Longest Cubic Subsequence
Based on Wang and Zhu (2023), Sections 3.1 and 3.2.
"""

import sys


def ceil_div(a, b):
    # Calculates ceiling division, including for negative values.
    return -((-a) // b)


def lcs3_bounded(A, B, C, D):

    # Gets the string lengths.
    m, n1, n2 = len(A), len(B), len(C)

    # Limits the number of deletions to the length of A.
    D = min(D, m)

    # prev[c][x] stores the largest position p < x where C[p] == c.
    prev = {}

    # Precalculate previous occurrences in C.
    for ch in set(A):

        row, last = [-1] * (n2 + 1), -1

        for x in range(n2 + 1):

            row[x] = last

            if x < n2 and C[x] == ch:
                last = x

        prev[ch] = row

    # Represents an impossible DP state.
    NEG = -1

    # Creates the DP table.
    L = [None] * (m + 1)

    # Base case: an empty suffix of A requires zero deletions.
    L[m] = [
        [n2 if d == 0 else NEG for d in range(D + 1)]
        for _ in range(n1 + 1)
    ]

    # Processes A backwards.
    for i in range(m - 1, -1, -1):

        # Number of characters remaining in A.
        rem = m - i

        # Maximum possible deletions for this state.
        dmax = min(D, rem)

        # Stores the current DP layer.
        Li = [None] * (n1 + 1)
        Lnext = L[i + 1]

        # Current character and its previous-occurrence table.
        a = A[i]
        pa = prev[a]

        # Processes B backwards.
        for j in range(n1, -1, -1):

            row = [NEG] * (D + 1)

            # State after advancing in A.
            nj = Lnext[j]

            for d in range(dmax + 1):

                # If all remaining characters in A are deleted,
                # an empty common subsequence is always possible.
                if d == rem:
                    row[d] = n2
                    continue

                # Option 1: Skip the current character in A.
                best = nj[d - 1] if d >= 1 else NEG

                if j < n1:

                    # Option 2: Skip the current character in B.
                    v = Li[j + 1][d]

                    if v > best:
                        best = v

                    # Option 3: Match the current characters in A and B.
                    if a == B[j]:

                        v = Lnext[j + 1][d]

                        if v >= 0:

                            # Find the previous matching position in C.
                            p = pa[v]

                            if p > best:
                                best = p

                row[d] = best

            Li[j] = row

        L[i] = Li

    # Find the smallest number of deletions that produces a valid LCS.
    d = next(
        (d for d in range(D + 1) if L[0][0][d] >= 0),
        None
    )

    if d is None:
        return None

    # Number of characters in the common subsequence.
    remaining = m - d

    # Reconstruct the common subsequence.
    res = []
    i = 0
    j = 0

    while remaining > 0:

        v = L[i][j][d]

        # Check whether the current character in A was skipped.
        if d >= 1 and L[i + 1][j][d - 1] == v:
            i += 1
            d -= 1

        # Check whether the current character in B was skipped.
        elif j < n1 and L[i][j + 1][d] == v:
            j += 1

        # Otherwise, the current characters are matched.
        else:
            res.append(A[i])
            i += 1
            j += 1
            remaining -= 1

    return "".join(res)


def _prefix_counts(S):

    # Stores prefix character frequencies.
    pref = {}

    for c in set(S):

        arr = [0] * (len(S) + 1)
        count = 0

        for i, ch in enumerate(S):

            if ch == c:
                count += 1

            arr[i + 1] = count

        pref[c] = arr

    return pref


def longest_cubic_subsequence(S):

    n = len(S)

    if n < 3:
        return ""

    # Check whether the entire input is already a cube.
    if n % 3 == 0:

        top = n // 3

        if S[:top] == S[top:2 * top] == S[2 * top:]:
            return S[:top]

    # Precalculate character frequencies.
    pref = _prefix_counts(S)
    letters = list(pref)

    # Start with a deletion budget of zero.
    K = 0

    while True:

        candidates = []

        # Restrict the first cutting position.
        # Derived from Lemma 1.
        s1_min = max(1, ceil_div(n - 3 * K, 3))
        s1_max = min(n - 2, (n + 3 * K) // 3)

        # Restrict the second cutting position.
        # Derived from the length restriction on the third partition.
        e_min = max(2, ceil_div(2 * n - 3 * K, 3))
        e_max = min(n - 1, (2 * n + 3 * K) // 3)

        # Examine only the permitted cutting positions.
        for s1 in range(s1_min, s1_max + 1):

            for e in range(max(s1 + 1, e_min), e_max + 1):

                # Calculate a frequency-based upper bound.
                total = 0

                for c in letters:

                    pc = pref[c]

                    total += min(
                        pc[s1],
                        pc[e] - pc[s1],
                        pc[n] - pc[e]
                    )

                # The shortest partition is another upper bound.
                upper = min(
                    total,
                    s1,
                    e - s1,
                    n - e
                )

                if upper > 0:
                    candidates.append((upper, s1, e))

        # Examine the most promising partitions first.
        candidates.sort(reverse=True)

        best = ""

        # Minimum common subsequence length needed to use
        # at most K deletions from the original sequence.
        target_len = ceil_div(n - K, 3)

        for upper, s1, e in candidates:

            # Remaining partitions cannot improve the answer.
            if upper <= len(best):
                break

            # Create the three partitions, shortest first.
            A, B, C = sorted(
                [S[:s1], S[s1:e], S[e:]],
                key=len
            )

            # Calculate the maximum deletions permitted in A.
            # This is NOT the total deletion budget K.
            D = len(A) - target_len

            # This partition is too short to produce
            # a common subsequence of the required length.
            if D < 0:
                continue

            # Run the bounded three-string LCS algorithm.
            X = lcs3_bounded(A, B, C, D)

            # Update the best solution.
            if X is not None and len(X) > len(best):
                best = X

        # Calculate the actual number of deletions.
        deleted = n - 3 * len(best)

        # If the solution fits within the budget,
        # all potentially better partitions have been examined.
        if deleted <= K:
            return best

        # Increase the deletion budget geometrically.
        if K == 0:
            K = 1
        else:
            K = min(2 * K, n)


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
