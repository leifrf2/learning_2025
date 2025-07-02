"""
It is required to implement cd(current_dir, new dir) and return the final path, for example:
cd(/foo/bar, baz) = /foo/bar/baz
cd(/foo/../, /baz) = /baz
cd(/, foo/bar/../../baz) = /baz
cd(/, ..) = Null

After completion, the difficulty increases. 
The third parameter is a soft link dictionary, 
for example: 
        cd(/foo/bar, baz, {'/foo/bar': '/abc'}) = /abc/baz 
        cd(/foo/bar, baz, {'/foo/bar': '/abc', '/abc': '/bcd', '/bcd/baz': '/xyz'}) = /xyz 
There may be short matches and long matches in the dictionary. The long one (more specific) should be matched first, 
for example: cd(/foo/bar, baz, {'/foo/bar': '/abc', '/foo/bar/baz': '/xyz'}) = /xyz
To determine whether there is a loop in the dictionary
"""

from typing import Dict, List

UPWARD_PATH = ".."

def compose_path(path_elements: List[str]) -> str:
     if len(path_elements) > 0:
        return '/' + '/'.join(path_elements)
     else:
        return str()

def cd_pathstack(path_elements: List[str], path_update: str) -> List[str]:
    for path_segment in [p for p in path_update.split('/') if p != '']:
            if path_segment == UPWARD_PATH:
                if len(path_elements) > 0:
                    path_elements.pop(0)
            else:
                path_elements.append(path_segment)
    
    return path_elements


def cd(current_dir: str, new_dir: str) -> str:
    path_segments_current_dir = cd_pathstack(list(), current_dir)
    final_path_segments = cd_pathstack(path_segments_current_dir, new_dir)
    if len(final_path_segments) == 0:
         return None
    else:
        return compose_path(final_path_segments)

"""
cd(/foo/bar, baz, {'/foo/bar': '/abc', '/foo/bar/baz': '/xyz'}) = /xyz
"""
def cd_2(current_dir: str, new_dir: str, soft_links: Dict) -> str:
    path_segments_current_dir = cd_pathstack(list(), current_dir)
    final_path_segments = cd_pathstack(path_segments_current_dir, new_dir)

    left = final_path_segments
    initial_full_path = compose_path(left)
    right = list()

    # start with looking for the full new path in the soft links
    # if it's found, return
    # if not found, drop the outermost path segment
    # repeat
    while len(left) > 0:
         path = compose_path(left)
         if path in soft_links.keys():
              return soft_links[path] + compose_path(right)
         else:
            right = [left[-1]] + right
            left = left[:-1]

    return initial_full_path

     ## Handle cycles
