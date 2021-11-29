# Name: Miles Kesser
# OSU Email: kesserm@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 7 HashMap
# Due Date: 3 December 2021
# Description:
# Import pre-written DynamicArray and LinkedList classes
from a7_include import *


def hash_function_1(key: str) -> int:
    """
    Sample Hash function #1 to be used with A5 HashMap implementation
    DO NOT CHANGE THIS FUNCTION IN ANY WAY
    """
    hash = 0
    for letter in key:
        hash += ord(letter)
    return hash


def hash_function_2(key: str) -> int:
    """
    Sample Hash function #2 to be used with A5 HashMap implementation
    DO NOT CHANGE THIS FUNCTION IN ANY WAY
    """
    hash, index = 0, 0
    index = 0
    for letter in key:
        hash += (index + 1) * ord(letter)
        index += 1
    return hash


class HashMap:
    def __init__(self, capacity: int, function) -> None:
        """
        Init new HashMap based on DA with SLL for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.buckets = DynamicArray()
        for _ in range(capacity):
            self.buckets.append(LinkedList())
        self.capacity = capacity
        self.hash_function = function
        self.size = 0

    def __str__(self) -> str:
        """
        Return content of hash map t in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = ''
        for i in range(self.buckets.length()):
            list = self.buckets.get_at_index(i)
            out += str(i) + ': ' + str(list) + '\n'
        return out

    def get_hash_capacity(self):
        """
        Returns capacity of HashMap
        """
        # Returns current capacity
        return self.capacity

    def set_hash_capacity(self, new_cap):
        """
        Sets new capacity
        """
        # Sets capacity to new_cap
        self.capacity = new_cap

    def get_hash_size(self):
        """
        Returns size of HashMap
        """
        # Returns size of hash table
        return self.size

    def increase_hash_size(self):
        """
        Increases size by 1
        """
        # Increases hash table size by one
        self.size += 1

    def decrease_hash_size(self):
        """
        Decreases size by 1
        """
        # Decreases hash table size by one
        self.size -= 1

    def set_hash_size(self, size):
        """
        Sets size of HashMap
        """
        # Sets size of hash table to size
        self.size = size

    def clear(self) -> None:
        """
        Clears the contents of the hash map. It does not change the underlying hash table capacity
        """
        # Set each buckets contents to None
        for index in range(0, self.get_hash_capacity()):
            self.buckets.set_at_index(index, LinkedList())
        # Set new size to zero
        self.set_hash_size(0)

    def get(self, key: str) -> object:
        """
        Returns the value associated with the given key. If the key is not in the hash map, the method returns None
        """
        # If hash table is empty
        if self.buckets.length() == 0:
            return None
        # If key not in hash table
        elif not self.contains_key(key):
            return None
        # If hash table contains key
        elif self.contains_key(key):
            # Get bucket index
            hash = self.hash_function(key)
            index = hash % self.get_hash_capacity()
            # get linked list in bucket
            linked_list = self.buckets.get_at_index(index)
            # Get value in linked list
            value = linked_list.contains(key)
            if value is None:
                return None
            else:
                return value.value

    def put(self, key: str, value: object) -> None:
        """
        Updates the key / value pair in the hash map. If a given key already exists in the hash map, its associated value must be replaced with the new value. If a given key is not in the hash map, a key / value pair must be added.
        """
        # Get bucket index
        hash = self.hash_function(key)
        index = hash % self.get_hash_capacity()
        # Get linked list in bucket
        linked_list = self.buckets.get_at_index(index)
        # If inked list is empty, insert value
        if linked_list.length() == 0:
            linked_list.insert(key, value)
            # Increase hash size
            self.increase_hash_size()
        # If key is in hash table
        elif linked_list.contains(key) is not None:
            # Remove value
            linked_list.remove(key)
            # Decrease size
            self.decrease_hash_size()
            # Insert new value
            linked_list.insert(key, value)
            # Increase size
            self.increase_hash_size()
        else:
            # If linked list is not empty and key is not found, insert key/value
            linked_list.insert(key, value)
            # Increase size
            self.increase_hash_size()

    def remove(self, key: str) -> None:
        """
        Removes the given key and its associated value from the hash map
        """
        # Get bucket index
        hash = self.hash_function(key)
        index = hash % self.get_hash_capacity()
        # Get linked list in bucket
        linked_list = self.buckets.get_at_index(index)
        # Get value in linked list
        value = linked_list.contains(key)
        # If value is found, remove key/value
        if value is not None:
            linked_list.remove(key)
            # Decrease size
            self.decrease_hash_size()

    def contains_key(self, key: str) -> bool:
        """
        Returns True if the given key is in the hash map, otherwise it returns False. An empty hash map does not contain any keys
        """
        # Get bucket index
        hash = self.hash_function(key)
        index = hash % self.get_hash_capacity()
        # If hash table is empty, return False
        if self.buckets.length() == 0:
            return False
        # If key/value is found in array, return True
        elif self.buckets.get_at_index(index).contains(key):
            return True
        else:
            return False

    def empty_buckets(self) -> int:
        """
        Returns the number of empty buckets in the hash table
        """
        # Set counter to zero
        count = 0
        # Iterate through hash table
        for index in range(0, self.get_hash_capacity()):
            # Increase count for each empty spot found
            if self.buckets.get_at_index(index).length() == 0:
                count += 1
        return count

    def table_load(self) -> float:
        """
        Returns the current hash table load factor as float
        """
        # If hash table is empty
        if self.get_hash_size() == 0:
            return 0.0
        # return float of (size / capacity)
        return float(self.get_hash_size()) / float(self.get_hash_capacity())

    def resize_table(self, new_capacity: int) -> None:
        """
        Changes the capacity of the internal hash table. All existing key / value pairs must remain in the new hash map and all hash table links must be rehashed
        """
        # If new capacity is less than one, nothing happens
        if new_capacity < 1:
            return
        # Initialize new dynamic array
        new_array = DynamicArray()
        # Add empty linked list to each index of new capacity in dynamic array
        for index in range(0, new_capacity):
            new_array.append(LinkedList())
        # Initialize new empty linked list
        new_linked_list = LinkedList()
        # Get linked lists from each bucket
        for index in range(0, self.get_hash_capacity()):
            linked_list = self.buckets.get_at_index(index)
            # If linked list is not empty
            if linked_list.length() != 0:
                # Get nodes from linked list
                for node in linked_list:
                    # Rehash each node
                    hash = self.hash_function(node.key)
                    index = hash % new_capacity
                    # Add newly hashed nodes to new linked list
                    new_linked_list.insert(node.key, node.value)
        # Set new hash capacity to new_capacity
        self.set_hash_capacity(new_capacity)
        # Set current buckets to new_array
        self.buckets = new_array
        # Set size to zero
        self.size = 0
        # Add nodes from linked list to new array, resetting size and stored values
        for node in new_linked_list:
            self.put(node.key, node.value)

    def get_keys(self) -> DynamicArray:
        """
        Returns a DynamicArray that contains all keys stored in your hash map
        """
        # Create empty dynamic array
        new_array = DynamicArray()
        # For every linked list in each bucket
        for linked_list in range(0, self.buckets.length()):
            # Fro every node in each linked list
            for node in self.buckets.get_at_index(linked_list):
                # Add key to dynamic array
                new_array.append(node.key)
        return new_array


# BASIC TESTING
if __name__ == "__main__":
    print("\nPDF - empty_buckets example 1")
    print("-----------------------------")
    m = HashMap(100, hash_function_1)
    print(m.empty_buckets(), m.size, m.capacity)
    m.put('key1', 10)
    print(m.empty_buckets(), m.size, m.capacity)
    m.put('key2', 20)
    print(m.empty_buckets(), m.size, m.capacity)
    m.put('key1', 30)
    print(m.empty_buckets(), m.size, m.capacity)
    m.put('key4', 40)
    print(m.empty_buckets(), m.size, m.capacity)
    print("\nPDF - empty_buckets example 2")
    print("-----------------------------")
    m = HashMap(50, hash_function_1)
    for i in range(150):
        m.put('key' + str(i), i * 100)
        if i % 30 == 0:
            print(m.empty_buckets(), m.size, m.capacity)
    print("\nPDF - table_load example 1")
    print("--------------------------")
    m = HashMap(100, hash_function_1)
    print(m.table_load())
    m.put('key1', 10)
    print(m.table_load())
    m.put('key2', 20)
    print(m.table_load())
    m.put('key1', 30)
    print(m.table_load())
    print("\nPDF - table_load example 2")
    print("--------------------------")
    m = HashMap(50, hash_function_1)
    for i in range(50):
        m.put('key' + str(i), i * 100)
        if i % 10 == 0:
            print(m.table_load(), m.size, m.capacity)
    print("\nPDF - clear example 1")
    print("---------------------")
    m = HashMap(100, hash_function_1)
    print(m.size, m.capacity)
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key1', 30)
    print(m.size, m.capacity)
    m.clear()
    print(m.size, m.capacity)
    print("\nPDF - clear example 2")
    print("---------------------")
    m = HashMap(50, hash_function_1)
    print(m.size, m.capacity)
    m.put('key1', 10)
    print(m.size, m.capacity)
    m.put('key2', 20)
    print(m.size, m.capacity)
    m.resize_table(100)
    print(m.size, m.capacity)
    m.clear()
    print(m.size, m.capacity)
    print("\nPDF - put example 1")
    print("-------------------")
    m = HashMap(50, hash_function_1)
    for i in range(150):
        m.put('str' + str(i), i * 100)
        if i % 25 == 24:
            print(m.empty_buckets(), m.table_load(), m.size, m.capacity)
    print("\nPDF - put example 2")
    print("-------------------")
    m = HashMap(40, hash_function_2)
    for i in range(50):
        m.put('str' + str(i // 3), i * 100)
        if i % 10 == 9:
            print(m.empty_buckets(), m.table_load(), m.size, m.capacity)
    print("\nPDF - contains_key example 1")
    print("----------------------------")
    m = HashMap(10, hash_function_1)
    print(m.contains_key('key1'))
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key3', 30)
    print(m.contains_key('key1'))
    print(m.contains_key('key4'))
    print(m.contains_key('key2'))
    print(m.contains_key('key3'))
    m.remove('key3')
    print(m.contains_key('key3'))
    print("\nPDF - contains_key example 2")
    print("----------------------------")
    m = HashMap(75, hash_function_2)
    keys = [i for i in range(1, 1000, 20)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.size, m.capacity)
    result = True
    for key in keys:
        # all inserted keys must be present
        result &= m.contains_key(str(key))
        # NOT inserted keys must be absent
        result &= not m.contains_key(str(key + 1))
    print(result)
    print("\nPDF - get example 1")
    print("-------------------")
    m = HashMap(30, hash_function_1)
    print(m.get('key'))
    m.put('key1', 10)
    print(m.get('key1'))
    print("\nPDF - get example 2")
    print("-------------------")
    m = HashMap(150, hash_function_2)
    for i in range(200, 300, 7):
        m.put(str(i), i * 10)
    print(m.size, m.capacity)
    for i in range(200, 300, 21):
        print(i, m.get(str(i)), m.get(str(i)) == i * 10)
        print(i + 1, m.get(str(i + 1)), m.get(str(i + 1)) == (i + 1) * 10)
    print("\nPDF - remove example 1")
    print("----------------------")
    m = HashMap(50, hash_function_1)
    print(m.get('key1'))
    m.put('key1', 10)
    print(m.get('key1'))
    m.remove('key1')
    print(m.get('key1'))
    m.remove('key4')
    print("\nPDF - resize example 1")
    print("----------------------")
    m = HashMap(20, hash_function_1)
    m.put('key1', 10)
    print(m.size, m.capacity, m.get('key1'), m.contains_key('key1'))
    m.resize_table(30)
    print(m.size, m.capacity, m.get('key1'), m.contains_key('key1'))
    print("\nPDF - resize example 2")
    print("----------------------")
    m = HashMap(75, hash_function_2)
    keys = [i for i in range(1, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.size, m.capacity)
    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)
        m.put('some key', 'some value')
        result = m.contains_key('some key')
        m.remove('some key')
        for key in keys:
            result &= m.contains_key(str(key))
            result &= not m.contains_key(str(key + 1))
        print(capacity, result, m.size, m.capacity, round(m.table_load(), 2))
    print("\nPDF - get_keys example 1")
    print("------------------------")
    m = HashMap(10, hash_function_2)
    for i in range(100, 200, 10):
        m.put(str(i), str(i * 10))
    print(m.get_keys())
    m.resize_table(1)
    print(m.get_keys())
    m.put('200', '2000')
    m.remove('100')
    m.resize_table(2)
    print(m.get_keys())