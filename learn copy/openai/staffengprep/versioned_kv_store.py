"""
Implement a KV store with the following methods:

class KeyValueStore(ABC):
    @abstractmethod
    def put(self, key: str, value: str) -> int:
        # Inserts a new value for the given key and returns the version number.
        pass

    @abstractmethod
    def get(self, key: str, version: Optional[int] = -1) -> Optional[str]:
        #Retrieves the value associated with the key at the given version.
        # If version is -1, return the latest value.
        pass
Part A: Implement put and get methods for a versioned KV store.

Part B: Make the KV store thread-safe. Multiple threads could update the same key in parallel, we need to ensure we pass different version numbers for each one of them. Also, get should also be multi-threaded and return a value if key and version number was once accepted by put.

Part C: Imagine the version number we return from put fn is a timestamp of the record when key was added. How to handle the scenario where get receives a version number (or timestamp) in future. What if the timestamp is 100 years in future?
"""