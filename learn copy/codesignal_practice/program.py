# start: 8am
# break 8:09-8:22

"""

- **FILE_UPLOAD(file_name, size)**
  - Upload the file to the remote storage server.
  - If a file with the same name already exists on the server, it throws a runtime exception.
- **FILE_GET(file_name)**
  - Returns the size of the file, or nothing if the file doesn’t exist.
- **FILE_COPY(source, dest)**
  - Copy the source file to a new location.
  - If the source file doesn’t exist, it throws a runtime exception.
  - If the destination file already exists, it overwrites the existing file.

[server34] - 24000 Bytes Limit
    Size
    +- file-1.zip 4321 Bytes
    +- dir-a
    |   +- dir-c
    |   |   +- file-2.txt 1100 Bytes
    |   |   +- file-3.csv 2122 Bytes
    +- dir-b
    |   +- file-4.mdx 3378 Bytes  

  """


from dataclasses import dataclass
from datetime import datetime, time, timedelta
from typing import Dict, List, Optional
from pathlib import Path

@dataclass
class FileServerFile:
    size: int
    # never cleaning these up means that we have file bloat
    expiration: Optional[datetime]

    def is_expired(self, timestamp: datetime) -> bool:
        return self.expiration == None or self.expiration > timestamp


class FileServer:

# we have to simluate a file structure, not actual files
# could do absolute paths
# but that makes it hard to resolve nesting
# so maybe a nested dictionary instead?
# until we know we need to implement that complexity, let's keep it simple

    def __init__(self):
        self.file_directory: Dict[str, FileServerFile] = dict()

    # Upload the file to the remote storage server.
    # If a file with the same name already exists on the server, it throws a runtime exception.
    def file_upload(self, file_name: str, size: int, ttl: Optional[int] = None) -> None:
        if file_name in self.file_directory.keys():
            raise RuntimeError(f"File already exists: {file_name}")
        else:
            self.file_directory[file_name] = FileServerFile(size=size, expiration=datetime.now() + timedelta(seconds=5))

    # Returns the size of the file, or nothing if the file doesn’t exist.
    def file_get(self, timestamp: datetime, file_name: str) -> Optional[int]:
        serverfile = self.file_directory.get(file_name, None)
        
        if not serverfile.is_expired(timestamp):
            return serverfile.size
        else:
            return None

   # Copy the source file to a new location.
   # If the source file doesn’t exist, it throws a runtime exception.
   # If the destination file already exists, it overwrites the existing file.
    def file_copy(self, timestamp: datetime, source: str, dest: str) -> None:
        if source in self.file_directory.keys() and not self.file_directory[source].is_expired():
            self.file_directory[dest] = self.file_directory[source]
            del self.file_directory[source]
        else:
            raise RuntimeError(f"source file does not exist: {source}")
        
    # Find top 10 files starting with the provided prefix.
    # Order results by their size in descending order, and in case of a tie by file name.
    def file_search(self, timestamp: datetime, prefix: str) -> List[str]:
        # TODO: come back to optimize
        # right now it requires sorting the keys NLogN
        # and prefix checking N keys N
        return [x for x,y in 
                sorted((a for a in self.file_directory.items()
                        if a[0].startswith(prefix) and not a[1].is_expired(timestamp)), key=lambda x: -x[1])
                ][:10]
    
    def rollback(timestamp: datetime) -> None:
        # since timestamp is always passed in above
        # and we're never deleting files
        # then there's nothing to do here?
        pass