"""
Level 1: Basic Chat Message Storage

The chat application should store messages exchanged between users. Each user has a message history, where each message has a unique messageId. Messages are stored as field-value pairs, where the field is the message ID, and the value is the message content.

Operations:

SEND_MESSAGE <userId> <messageId> <message>
Stores a message for a user.
If the message ID already exists, the message content is updated.
Returns an empty string.
GET_MESSAGE <userId> <messageId>
Retrieves a message for a given user.
Returns the message content if it exists, or an empty string otherwise.
DELETE_MESSAGE <userId> <messageId>
Deletes a specific message from a user’s history.
Returns "true" if the message was deleted, "false" if it doesn’t exist.
Example Queries:

queries = [
["SEND_MESSAGE", "Alice", "msg1", "Hello Bob!"],
["SEND_MESSAGE", "Alice", "msg2", "How are you?"],
["GET_MESSAGE", "Alice", "msg1"],
["GET_MESSAGE", "Alice", "msg3"],
["DELETE_MESSAGE", "Alice", "msg1"],
["DELETE_MESSAGE", "Alice", "msg3"]
]

Output:
""   # Message stored
""   # Message stored
"Hello Bob!"
""   # Message does not exist
"true"   # Message deleted
"false"  # Message does not exist
Level 2: Message Filtering

Messages should be retrievable based on filtering criteria.

Operations:

LIST_MESSAGES <userId>
Returns all messages for a user in the format:"msg1(Hello Bob!), msg2(How are you?), ..."
Messages are sorted lexicographically by their IDs.
Returns an empty string if the user has no messages.
LIST_MESSAGES_BY_PREFIX <userId> <prefix>
Returns messages where the message ID starts with <prefix>.
Messages are sorted lexicographically.
Example Queries:

queries = [
["SEND_MESSAGE", "Alice", "msg10", "Meeting at 5"],
["SEND_MESSAGE", "Alice", "msg20", "See you soon"],
["SEND_MESSAGE", "Alice", "note1", "Buy groceries"],
["LIST_MESSAGES_BY_PREFIX", "Alice", "msg"],
["LIST_MESSAGES", "Alice"],
["LIST_MESSAGES_BY_PREFIX", "Bob", ""]
]

Output
"msg10(Meeting at 5), msg20(See you soon)"
"msg10(Meeting at 5), msg20(See you soon), note1(Buy groceries)"
""   # Bob has no messages

Level 3: Expiring Messages (Instead of TTL)

Messages now have an expiration time, after which they should be removed.

Operations:

SEND_MESSAGE_AT <userId> <messageId> <message> <timestamp>
Stores a message with a specific timestamp.
SEND_MESSAGE_WITH_EXPIRY <userId> <messageId> <message> <timestamp> <expiry>
Stores a message that will expire <expiry> units after <timestamp>.
The message is only available until (timestamp + expiry).
DELETE_MESSAGE_AT <userId> <messageId> <timestamp>
Deletes a message at a given timestamp.
GET_MESSAGE_AT <userId> <messageId> <timestamp>
Retrieves a message if it hasn’t expired.
LIST_MESSAGES_AT <userId> <timestamp>
Returns all messages for a user at a specific timestamp, filtering out expired messages.
LIST_MESSAGES_BY_PREFIX_AT <userId> <prefix> <timestamp>
Same as LIST_MESSAGES_BY_PREFIX, but considers message expiration.
Example Queries:

queries = [
["SEND_MESSAGE_WITH_EXPIRY", "Alice", "msg1", "See you soon", "11", "10"],
["SEND_MESSAGE_AT", "Alice", "msg2", "Good morning!", "4"],
["DELETE_MESSAGE_AT", "Alice", "msg1", "8"],
["GET_MESSAGE_AT", "Alice", "msg1", "12"],
["LIST_MESSAGES_AT", "Alice", "13"],
["LIST_MESSAGES_AT", "Alice", "20"]
]

Output:
""   # Message stored with expiry
""   # Message stored
"true"  # Message deleted before expiry
""   # Message expired, not retrievable
"msg2(Good morning!)"
""   # All messages expired
Level 4: Message Backup and Restoration

The chat application should allow backing up and restoring messages, keeping track of expiration.

Operations:

ZIP_MESSAGES <timestamp>
Saves the current state of messages.
Returns the number of non-expired messages.
UNZIP_MESSAGES <restoreTimestamp> <backupTimestamp>
Restores the messages from the latest backup taken at or before <backupTimestamp>.
Expiration times are recalculated based on <restoreTimestamp>.
Example Queries:

queries = [
["SEND_MESSAGE_WITH_EXPIRY", "Bob", "msg1", "Meeting at 5", "60", "30"],
["ZIP_MESSAGES", "70"],
["SEND_MESSAGE_WITH_EXPIRY", "Bob", "msg2", "Dinner at 8", "75", "20"],
["UNZIP_MESSAGES", "100", "70"],
["LIST_MESSAGES_AT", "Bob", "100"]
]

Output:

"1"  # One active message at backup
""   # New message stored
""   # Database restored from backup
"msg1(Meeting at 5)"  # Only msg1 is restored, msg2 was not in backup
"""