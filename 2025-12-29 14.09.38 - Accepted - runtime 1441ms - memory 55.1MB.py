class Solution:
    def minDeletions(self, s: str, queries: List[List[int]]) -> List[int]:
        s = list(s)
        n = len(s)
        
        # same[i] = 1 if s[i] == s[i+1], else 0
        # Answer for [l, r] = sum of same[l..r-1]
        # Use BIT (Fenwick tree) for range sum with point updates
        
        # BIT for 1-indexed
        bit = [0] * (n + 1)
        
        def update(i, delta):
            i += 1  # Convert to 1-indexed
            while i <= n:
                bit[i] += delta
                i += i & (-i)
        
        def query_sum(i):  # Sum of same[0..i-1]
            i += 1  # Convert to 1-indexed
            total = 0
            while i > 0:
                total += bit[i]
                i -= i & (-i)
            return total
        
        def range_sum(l, r):  # Sum of same[l..r-1]
            if l > r - 1:
                return 0
            return query_sum(r - 1) - (query_sum(l - 1) if l > 0 else 0)
        
        # Initialize BIT with same values
        for i in range(n - 1):
            if s[i] == s[i + 1]:
                update(i, 1)
        
        result = []
        
        for q in queries:
            if q[0] == 1:
                j = q[1]
                # Before flip, check adjacent pairs
                # s[j-1] == s[j] and s[j] == s[j+1]
                old_left = (j > 0 and s[j-1] == s[j])
                old_right = (j < n-1 and s[j] == s[j+1])
                
                # Flip
                s[j] = 'B' if s[j] == 'A' else 'A'
                
                # After flip, check adjacent pairs
                new_left = (j > 0 and s[j-1] == s[j])
                new_right = (j < n-1 and s[j] == s[j+1])
                
                # Update BIT
                if j > 0:
                    if old_left and not new_left:
                        update(j-1, -1)
                    elif not old_left and new_left:
                        update(j-1, 1)
                if j < n - 1:
                    if old_right and not new_right:
                        update(j, -1)
                    elif not old_right and new_right:
                        update(j, 1)
            else:
                l, r = q[1], q[2]
                # Count same pairs in [l, r-1]
                result.append(range_sum(l, r))
        
        return result