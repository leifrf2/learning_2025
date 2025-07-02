"""
Implement cd command which given a pwd (present working directory) and an input_path outputs the path operating system switches to. There are multiple parts to this question: 

Part A: Implement cd command to account for ./ ../ and /root paths in the input paths. 

Part B: Imagine you are given symbolic link mapping that maps symLinks to actual paths, extend the solution to account for symlinks with cd command. We need to check for symlink at every step of traversing the path. 

Part C: How to handle cases where symLink→Path→AnotherPath (multi-level indirections) with symLink paths. Also, how to make sure we do not end up in a cycle and loop forever.
"""