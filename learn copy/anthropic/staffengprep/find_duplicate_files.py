"""
Implement a system to detect duplicate files within a given file system directory. The solution should efficiently identify files that are identical based on the following comparison methods:

Size Comparison: Initially, identify potential duplicates by comparing file sizes. Files of different sizes cannot be duplicates.
Partial Hash Comparison: For files with the same size, compute a hash of a small portion (e.g., the first few kilobytes) of their content. This helps quickly eliminate non-identical files while minimizing computational overhead.
Full Hash Comparison: If two files pass the partial hash check, compute a full cryptographic hash (e.g., SHA-256) to confirm whether they are exact duplicates.
The implementation should efficiently traverse the file system, handle large files, and minimize unnecessary computations. The output should include a list of groups of duplicate files, where each group contains files that are identical based on the full hash comparison
"""