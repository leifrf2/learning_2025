"""
Level 1:
The inventory management system should support operations to add items, copy items, and get item quantity.

ADD ITEM <name> <quantity> — should add a new item <name> to the inventory with <quantity> units. The operation fails if an item with the same <name> already exists. Returns "true" if the item was added successfully or "false" otherwise.
COPY ITEM <nameFrom> <nameTo> — should copy the item at <nameFrom> to <nameTo>. The operation fails if <nameFrom> does not exist or if an item with the same name <nameTo> already exists. Returns "true" if the item was copied successfully or "false" otherwise.
GET ITEM QUANTITY <name> — should return a string representing the quantity of the item <name> if it exists, or an empty string otherwise.
Examples:
queries = [
["ADD_ITEM", "/warehouse/sectionA/item1", "20"],
["COPY_ITEM", "/not-existing.item", "/warehouse/sectionB/item1"],
["COPY_ITEM", "/warehouse/sectionA/item1", "/warehouse/sectionB/item1"],
["ADD_ITEM", "/warehouse/sectionB/item1", "35"],
["COPY_ITEM", "/warehouse/sectionB/item1", "/warehouse/sectionA/item1"],
["GET_ITEM_QUANTITY", "/warehouse/sectionB/item1"],
["GET_ITEM_QUANTITY", "/not-existing.item"]
]

Returns:

"true"; adds item "/warehouse/sectionA/item1" with 20 units
"false"; item "/not-existing.item" does not exist
"true"; adds item "/warehouse/sectionB/item1" with 20 units
"false"; item "/warehouse/sectionB/item1" already exists
"false"; item "/warehouse/sectionA/item1" already exists
"20"
""; item "/not-existing.item" does not exist
Level 2:
Implement support for retrieving item names by searching sections via prefixes and suffixes.

FIND ITEM <prefix> <suffix> — should search for items with names starting with <prefix> and ending with <suffix>. Returns a string representing all matching items in this format: "<name1>(<quantity1>), <name2> (<quantity2>), ...".
The output should be sorted in descending order of quantity or, in the case of ties, lexicographically.
If no items match the required properties, it should return an empty string.
Examples:
queries = [
["ADD_ITEM", "/warehouse/sectionX/itemA", "50"],
["ADD_ITEM", "/warehouse/itemB", "25"],
["ADD_ITEM", "/warehouse/sectionY/itemC", "30"],
["COPY_ITEM", "/warehouse/sectionY/itemC", "/warehouse/sectionZ/itemC"],
["FIND_ITEM", "/warehouse", "item"],
["FIND_ITEM", "/warehouse", "itemX"],
["FIND_ITEM", "/sectionY", "itemC"]
]

Returns:

"true"
"true"
"true"
"true"
"/warehouse/sectionX/itemA(50), /warehouse/sectionZ/itemC(30), /warehouse/sectionY/itemC(30), /warehouse/itemB(25)"
""; no item with the prefix "/warehouse" and suffix "itemX"
""; no item with the prefix "/sectionY" and suffix "itemC"
Level 3:
Implement support for different users managing inventory. All users share a common inventory system, but each user is assigned an individual stock capacity limit.

ADD USER <userId> <capacity> — should add a new user to the system, with <capacity> as their stock limit (in units). The total quantity of all items owned by <userId> cannot exceed <capacity>. The operation fails if a user with <userId> already exists. Returns "true" if the user is successfully created, or "false" otherwise.
ADD ITEM BY <userId> <name> <quantity> — should behave in the same way as the ADD ITEM from Level 1, but the added item should be owned by <userId>. A new item cannot be added if doing so will exceed the user’s <capacity> limit. Returns a string representing the remaining stock capacity for <userId> if the item is successfully added, or an empty string otherwise.
Note: All queries calling the ADD ITEM operation from Level 1 are run by the user "admin", who has unlimited stock capacity.
The COPY ITEM operation preserves ownership of the original item.
UPDATE CAPACITY <userId> <capacity> — should change the maximum stock capacity for <userId>. If the total quantity of all user’s items exceeds the new <capacity>, the largest items (sorted lexicographically in case of a tie) should be removed from the inventory until the total quantity of all remaining items no longer exceeds <capacity>. Returns a string representing the number of removed items, or an empty string if <userId> does not exist.
Examples:
queries = [
["ADD_USER", "user1", "1500"],
["ADD_USER", "user1", "1200"],
["ADD_USER", "user2", "2500"],
["ADD_ITEM_BY", "user1", "/sectionA/itemBig", "600"],
["ADD_ITEM_BY", "user1", "/itemMed", "400"],
["COPY_ITEM", "/itemMed", "/sectionA/itemMed"],
["ADD_ITEM_BY", "user1", "/itemSmall", "200"],
["ADD_ITEM_BY", "user2", "/itemMed", "500"],
["ADD_ITEM_BY", "user1", "/sectionA/itemTiny", "100"],
["ADD_ITEM_BY", "user2", "/storage/itemHuge", "2500"],
["ADD_ITEM_BY", "user3", "/storage/itemHuge", "2500"],
["UPDATE_CAPACITY", "user1", "4000"],
["UPDATE_CAPACITY", "user1", "1000"],
["UPDATE_CAPACITY", "user2", "5000"]
]

Returns:

"true"; creates user "user1" with 1500 capacity
"false"; "user1" already exists
"true"; creates user "user2" with 2500 capacity
"900"
"500"
""; copying preserves the item owner. After copying, "user1" has 500 capacity left
"300"
""; "user1" does not have enough storage capacity left to perform copying operation
"true"
""; item "/sectionA/itemTiny" already exists
""; "user2" does not have enough storage capacity left to add this item
""; "user3" doesn't exist
"0"; all items owned by "user1" can fit into the new capacity of 4000 units
"2"; items "/sectionA/itemBig" and "/sectionA/itemMed" should be deleted so that the remaining items owned by "user1" fit within the new capacity of 1000 units
""; "user2" doesn't exist
Level 4:
Implement support for handling duplicate items.

ADD_DUPLICATE_ITEMS <userId> <name> — should create a duplicate of the item <name> if it belongs to <userId>. The duplicate item should be named <name>.dupe. The quantity of the newly created duplicate item should be half of the original item’s quantity. The quantity of all items is guaranteed to be even, so there should be no fractional calculations. It is also guaranteed that <name> for this operation never points to a duplicate item—i.e., it never ends with .dupe. Duplicate items should be owned by <userId> — the owner of the original item. Returns a string representing the remaining stock capacity for <userId> if the duplicate was successfully added, or an empty string otherwise.
Note: Because item names can only contain lowercase letters, duplicate items cannot be added via ADD_ITEM_BY.
COPY_ITEM operations must preserve the .dupe suffix.
REMOVE_DUPLICATE_ITEMS <userId> <name> — should remove the duplicate of the item <name>.dupe if it belongs to <userId>. If removing the duplicate would exceed <userId>‘s storage capacity (after restoring the original item quantity), or if a non-duplicate version of the item with the given name already exists, the operation fails. Returns a string representing the remaining stock capacity for <userId> if the duplicate was successfully removed, or an empty string otherwise.
"""