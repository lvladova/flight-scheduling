# Merge sort algorithm for sorting objects based on a given attribute
def merge_sort(objects, attribute):
    if len(objects) > 1:
        mid = len(objects) // 2
        left_half = objects[:mid]
        right_half = objects[mid:]

        # Recursively split the lists
        merge_sort(left_half, attribute)
        merge_sort(right_half, attribute)

        # Merge process
        i = j = k = 0

        # Merge the split lists into result
        while i < len(left_half) and j < len(right_half):
            if left_half[i][int(attribute)] < right_half[j][int(attribute)]:
                objects[k] = left_half[i]
                i += 1
            else:
                objects[k] = right_half[j]
                j += 1
            k += 1

        # Checking if any element was left
        while i < len(left_half):
            objects[k] = left_half[i]
            i += 1
            k += 1

        while j < len(right_half):
            objects[k] = right_half[j]
            j += 1
            k += 1

    return objects


# Bucket sort algorithm for sorting objects based on a given attribute
def bucket_sort(objects, attribute, bucket_size=5):
    if len(objects) == 0:
        return []

    # Determine minimum and maximum values
    min_value = getattr(objects[0], attribute)
    max_value = min_value
    for obj in objects:
        value = getattr(obj, attribute)
        if value < min_value:
            min_value = value
        elif value > max_value:
            max_value = value

    # Initialize buckets
    bucket_count = (max_value - min_value) // bucket_size + 1
    buckets = []
    for _ in range(int(bucket_count)):
        buckets.append([])

    # Distribute input array values into buckets
    for obj in objects:
        bucket_index = (getattr(obj, attribute) - min_value) // bucket_size
        buckets[bucket_index].append(obj)

    # Sort buckets and concatenate results
    sorted_objects = []
    for bucket in buckets:
        sorted_objects.extend(insertion_sort(bucket, attribute))

    return sorted_objects


# Insertion sort algorithm for sorting objects based on a given attribute
def insertion_sort(objects, attribute):
    for i in range(1, len(objects)):
        key_item = objects[i]
        j = i - 1
        # Compare the current object with the ones before it
        while j >= 0 and getattr(objects[j], attribute) > getattr(key_item, attribute):
            objects[j + 1] = objects[j]
            j -= 1
        # Place the key_item in its correct position
        objects[j + 1] = key_item
    return objects


# Quick sort algorithm for sorting objects based on a given attribute
def quick_sort(arr, key=lambda x: x):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if key(x) < key(pivot)]
    middle = [x for x in arr if key(x) == key(pivot)]
    right = [x for x in arr if key(x) > key(pivot)]
    return quick_sort(left, key) + middle + quick_sort(right, key)


# Counting sort algorithm for sorting objects based on a given attribute
def counting_sort(objects, get_attribute, position):
    output = [None] * len(objects)
    count = [0] * 256

    # Store the count of each character
    for obj in objects:
        char = get_attribute(obj)[position] if position < len(get_attribute(obj)) else chr(0)
        count[ord(char)] += 1

    # Change count[i] so that count[i] now contains the actual
    # position of this character in the output array
    for i in range(1, 256):
        count[i] += count[i-1]

    # Build the output array
    for obj in reversed(objects):
        char = get_attribute(obj)[position] if position < len(get_attribute(obj)) else chr(0)
        output[count[ord(char)] - 1] = obj
        count[ord(char)] -= 1

    return output


# Radix sort algorithm for sorting objects based on a given attribute
def radix_sort(objects, get_attribute):
    if not objects:
        return objects

    # Find the maximum length string
    max_len = max(len(get_attribute(obj)) for obj in objects)

    # Do counting sort for every character position
    for pos in range(max_len - 1, -1, -1):
        objects = counting_sort(objects, get_attribute, pos)

    return objects