#Used to generate random numbers in test array.
from random import randint
#Used to time execution of sorting algorithm.
from timeit import repeat
#Used to create and save database with results.
import sqlite3

#PLEASE SEE THE README FILE ASSOCIATED WITH THIS REPO FOR DETAILS OF THE SITES I USED AND THE GENERAL PURPOSE OF THIS CODE.
#Initially had in separate files/ scripts, but decided to just collate in one main.py file for easy adaptability e.g. adding in and removing algorithms to test.
#Might be ideal to run the final calls to test the algorithms (see line 420 onwards) to a separate testing.py to easily run from command line.

#List to contain the minimum execution time for each algorithm tested.
global min_time
min_time = []

####################################AUTOMATED RUNNING/ TIMING OF SORTING ALGORITHMS#############################################################

def run_sorting_algorithm(algorithm, array):
    # Set up the context and prepare the call to the specified
    # algorithm using the supplied array. Only import the
    # algorithm function if it's not the built-in `sorted()`.
    setup_code = f"from __main__ import {algorithm}" \
        if algorithm != "sorted" else ""
    
    #Preparing call to algorithm passing in supplied array. This statement will be executed and timed using timeit module.
    stmt = f"{algorithm}({array})"

    # Execute the code ten different times and return the time
    # in seconds that each execution took
    times = repeat(setup=setup_code, stmt=stmt, repeat=3, number=10)

    #Calculate minimum time from 10 runs
    min_time.append(min(times))
    
    #USEFUL POINT:
    #A common misconception is that you should find the average time of each 
    #run of the algorithm instead of selecting the single shortest time. 
    #Time measurements are noisy because the system runs other processes concurrently. 
    #The shortest time is always the least noisy, making it the best representation of 
    #the algorithm’s true runtime. (https://realpython.com/sorting-algorithms-python/)

    # Finally, display the name of the algorithm and the
    # minimum time it took to run
    print(f"Algorithm: {algorithm}. Minimum execution time: {min(times)}")

#############################################BUBBLE SORT ALGORITHM##############################################################################

def bubble_sort(array):
    n = len(array)

    for i in range(n):
        # Create a flag that will allow the function to
        # terminate early if there's nothing left to sort
        already_sorted = True

        # Start looking at each item of the list one by one,
        # comparing it with its adjacent value. With each
        # iteration, the portion of the array that you look at
        # shrinks because the remaining items have already been
        # sorted.
        for j in range(n - i - 1):
            if array[j] > array[j + 1]:
                # If the item you're looking at is greater than its
                # adjacent value, then swap them
                array[j], array[j + 1] = array[j + 1], array[j]

                # Since you had to swap two elements,
                # set the `already_sorted` flag to `False` so the
                # algorithm doesn't finish prematurely
                already_sorted = False

        # If there were no swaps during the last iteration,
        # the array is already sorted, and you can terminate
        if already_sorted:
            break

    return array

#############################################INSERTION SORT ALGORITHM#####################################################################

def insertion_sort(array):
    # Loop from the second element of the array until
    # the last element
    for i in range(1, len(array)):
        # This is the element we want to position in its
        # correct place
        key_item = array[i]

        # Initialize the variable that will be used to
        # find the correct position of the element referenced
        # by `key_item`
        j = i - 1

        # Run through the list of items (the left
        # portion of the array) and find the correct position
        # of the element referenced by `key_item`. Do this only
        # if `key_item` is smaller than its adjacent values.
        while j >= 0 and array[j] > key_item:
            # Shift the value one position to the left
            # and reposition j to point to the next element
            # (from right to left)
            array[j + 1] = array[j]
            j -= 1

        # When you finish shifting the elements, you can position
        # `key_item` in its correct location
        array[j + 1] = key_item

    return array

#############################################MERGE SORT ALGORITHM#####################################################################

def merge(left, right):
    # If the first array is empty, then nothing needs
    # to be merged, and you can return the second array as the result
    if len(left) == 0:
        return right

    # If the second array is empty, then nothing needs
    # to be merged, and you can return the first array as the result
    if len(right) == 0:
        return left

    result = []
    index_left = index_right = 0

    # Now go through both arrays until all the elements
    # make it into the resultant array
    while len(result) < len(left) + len(right):
        # The elements need to be sorted to add them to the
        # resultant array, so you need to decide whether to get
        # the next element from the first or the second array
        if left[index_left] <= right[index_right]:
            result.append(left[index_left])
            index_left += 1
        else:
            result.append(right[index_right])
            index_right += 1

        # If you reach the end of either array, then you can
        # add the remaining elements from the other array to
        # the result and break the loop
        if index_right == len(right):
            result += left[index_left:]
            break

        if index_left == len(left):
            result += right[index_right:]
            break

    return result

def merge_sort(array):
    # If the input array contains fewer than two elements,
    # then return it as the result of the function
    if len(array) < 2:
        return array

    midpoint = len(array) // 2

    # Sort the array by recursively splitting the input
    # into two equal halves, sorting each half and merging them
    # together into the final result
    return merge(
        left=merge_sort(array[:midpoint]),
        right=merge_sort(array[midpoint:]))

#############################################QUICK SORT ALGORITHM#####################################################################

def quick_sort(array):
    # If the input array contains fewer than two elements,
    # then return it as the result of the function
    if len(array) < 2:
        return array

    low, same, high = [], [], []

    # Select your `pivot` element randomly
    pivot = array[randint(0, len(array) - 1)]

    for item in array:
        # Elements that are smaller than the `pivot` go to
        # the `low` list. Elements that are larger than
        # `pivot` go to the `high` list. Elements that are
        # equal to `pivot` go to the `same` list.
        if item < pivot:
            low.append(item)
        elif item == pivot:
            same.append(item)
        elif item > pivot:
            high.append(item)

    # The final result combines the sorted `low` list
    # with the `same` list and the sorted `high` list
    return quick_sort(low) + same + quick_sort(high)

#############################################SELECTION SORT ALGORITHM#####################################################################

def selection_sort(array):
    iterations = 0
    for i in range(len(array)):
        # i is index of first element in unsorted subarray
        index_min = i # find index of minimum element in unsorted part
        # search for the minimum element in the unsorted part
        for j in range(i+1, len(array)):
            iterations += 1
            if array[j] < array[index_min]: # found new minimum in unsorted part
                index_min = j                       # remember index of new minimum
            j +=1
        if index_min != i:
            # swap elements
            temp = array[index_min]
            array[index_min] = array[i]
            array[i] = temp
    #print("iterations: ", iterations)

#############################################HEAP SORT ALGORITHM#####################################################################

# To heapify subtree rooted at index i. 
# n is size of heap 
def heapify(array, n, i): 
    largest = i  # Initialize largest as root 
    l = 2 * i + 1     # left = 2*i + 1 
    r = 2 * i + 2     # right = 2*i + 2 
  
    # See if left child of root exists and is 
    # greater than root 
    if l < n and array[i] < array[l]: 
        largest = l 
  
    # See if right child of root exists and is 
    # greater than root 
    if r < n and array[largest] < array[r]: 
        largest = r 
  
    # Change root, if needed 
    if largest != i: 
        array[i],array[largest] = array[largest],array[i]  # swap 
  
        # Heapify the root. 
        heapify(array, n, largest) 
  
# The main function to sort an array of given size 
def heap_sort(array): 
    n = len(array) 
  
    # Build a maxheap. 
    # Since last parent will be at ((n//2)-1) we can start at that location. 
    for i in range(n // 2 - 1, -1, -1): 
        heapify(array, n, i) 
  
    # One by one extract elements 
    for i in range(n-1, 0, -1): 
        array[i], array[0] = array[0], array[i]   # swap 
        heapify(array, i, 0) 

#############################################RADIX SORT ALGORITHM#####################################################################

def countingSort(array, exp1): 
  
    n = len(array) 
  
    # The output array elements that will have sorted arr 
    output = [0] * (n) 
  
    # initialize count array as 0 
    count = [0] * (10) 
  
    # Store count of occurrences in count[] 
    for i in range(0, n): 
        index = (array[i] / exp1) 
        count[int(index % 10)] += 1
  
    # Change count[i] so that count[i] now contains actual 
    # position of this digit in output array 
    for i in range(1, 10): 
        count[i] += count[i - 1] 
  
    # Build the output array 
    i = n - 1
    while i >= 0: 
        index = (array[i] / exp1) 
        output[count[int(index % 10)] - 1] = array[i] 
        count[int(index % 10)] -= 1
        i -= 1
  
    # Copying the output array to arr[], 
    # so that arr now contains sorted numbers 
    i = 0
    for i in range(0, len(array)): 
        array[i] = output[i] 
  
# Method to do Radix Sort 
def radix_sort(array): 
  
    # Find the maximum number to know number of digits 
    max1 = max(array) 
  
    # Do counting sort for every digit. Note that instead 
    # of passing digit number, exp is passed. exp is 10^i 
    # where i is current digit number 
    exp = 1
    while max1 / exp > 0: 
        countingSort(array, exp) 
        exp *= 10

#############################################BUCKET SORT ALGORITHM#####################################################################

def bucket_sort(array):
    # Find maximum value in the list and use length of the list to determine which value in the list goes into which bucket 
    max_value = max(array)
    size = max_value/len(array)

    # Create n empty buckets where n is equal to the length of the input list
    buckets_list= []
    for x in range(len(array)):
        buckets_list.append([]) 

    # Put list elements into different buckets based on the size
    for i in range(len(array)):
        j = int (array[i] / size)
        if j != len (array):
            buckets_list[j].append(array[i])
        else:
            buckets_list[len(array) - 1].append(array[i])

    # Sort elements within the buckets using Insertion Sort
    for z in range(len(array)):
        insertion_sort(buckets_list[z])
            
    # Concatenate buckets with sorted elements into a single list
    final_output = []
    for x in range(len (array)):
        final_output = final_output + buckets_list[x]
    return final_output

#############################################TIMSORT ALGORITHM#####################################################################

#Timsort: Mixture of merge and sort algorithms (same as built in sorted() in Python)
def insertion_sort_mod(array, left=0, right=None):
    if right is None:
        right = len(array) - 1

    # Loop from the element indicated by
    # `left` until the element indicated by `right`
    for i in range(left + 1, right + 1):
        # This is the element we want to position in its
        # correct place
        key_item = array[i]

        # Initialize the variable that will be used to
        # find the correct position of the element referenced
        # by `key_item`
        j = i - 1

        # Run through the list of items (the left
        # portion of the array) and find the correct position
        # of the element referenced by `key_item`. Do this only
        # if the `key_item` is smaller than its adjacent values.
        while j >= left and array[j] > key_item:
            # Shift the value one position to the left
            # and reposition `j` to point to the next element
            # (from right to left)
            array[j + 1] = array[j]
            j -= 1

        # When you finish shifting the elements, position
        # the `key_item` in its correct location
        array[j + 1] = key_item

    return array

def tim_sort(array):
    min_run = 32
    n = len(array)

    # Start by slicing and sorting small portions of the
    # input array. The size of these slices is defined by
    # your `min_run` size.
    for i in range(0, n, min_run):
        insertion_sort_mod(array, i, min((i + min_run - 1), n - 1))

    # Now you can start merging the sorted slices.
    # Start from `min_run`, doubling the size on
    # each iteration until you surpass the length of
    # the array.
    size = min_run
    while size < n:
        # Determine the arrays that will
        # be merged together
        for start in range(0, n, size * 2):
            # Compute the `midpoint` (where the first array ends
            # and the second starts) and the `endpoint` (where
            # the second array ends)
            midpoint = start + size - 1
            end = min((start + size * 2 - 1), (n-1))

            # Merge the two subarrays.
            # The `left` array should go from `start` to
            # `midpoint + 1`, while the `right` array should
            # go from `midpoint + 1` to `end + 1`.
            merged_array = merge(
                left=array[start:midpoint + 1],
                right=array[midpoint + 1:end + 1])

            # Finally, put the merged array back into
            # your array
            array[start:start + len(merged_array)] = merged_array

        # Each iteration should double the size of your arrays
        size *= 2

    return array

#############################################RUNNING THE EXECUTION TIME TESTS#####################################################################

#Length of array to be sorted/ tested
ARRAY_LENGTH = 1000

if __name__ == "__main__":
    # Generate an array of `ARRAY_LENGTH` items consisting
    # of random integer values between 0 and 999
    array = [randint(0, 1000) for i in range(ARRAY_LENGTH)]
    
    # Call the function using the name of the sorting algorithm
    # and the array you just created
    run_sorting_algorithm(algorithm="sorted", array=array)
    run_sorting_algorithm(algorithm="bubble_sort", array=array)
    run_sorting_algorithm(algorithm="insertion_sort", array=array)
    run_sorting_algorithm(algorithm="merge_sort", array=array)
    run_sorting_algorithm(algorithm="quick_sort", array=array)
    run_sorting_algorithm(algorithm="selection_sort", array=array)
    run_sorting_algorithm(algorithm="heap_sort", array=array)
    run_sorting_algorithm(algorithm="radix_sort", array=array)
    run_sorting_algorithm(algorithm="bucket_sort", array=array)
    run_sorting_algorithm(algorithm="tim_sort", array=array)

#############################################STORE RESULTS IN DATABASE USING SQLITE3#####################################################################

#Ask user for file name to save results in .db file in the project directory
databaseFileName = input("\nWhat would you like to call the database file containing your results? ")

#Create and save a database:
conn = sqlite3.connect(f'{databaseFileName}.db')

#Create a cursor
c = conn.cursor()

#Create a table to put data in, use doc string (triple QMs)
# for multi-line. Real is the datatype needed to hold the floats returned by the timeit module.
c.execute("""CREATE TABLE results (
    algorithm text,
    min_exec_time real
    )""")

#Store results in list. Add to as needed if you want to test more algorithms.
many_results = [
                   ('sorted        ', min_time[0]),
                   ('bubble_sort   ', min_time[1]),
                   ('insertion_sort', min_time[2]),
                   ('merge_sort    ', min_time[3]),
                   ('quick_sort    ', min_time[4]),
                   ('selection_sort', min_time[5]),
                   ('heap_sort     ', min_time[6]),
                   ('radix_sort    ', min_time[7]),
                   ('bucket_sort   ', min_time[8]),
                   ('tim_sort      ', min_time[9]),
                ]

#Add many elements to database at once
c.executemany("INSERT INTO results VALUES (?, ?)", many_results)

#Query the database and display it as list/ tuple. Can also select primary key for each element by typing "SELECT rowid" if you want to display it. Put in ascending order
#using the minimum execution time column.
c.execute("SELECT * FROM results ORDER BY min_exec_time ASC")
items = c.fetchall()

#WARNING: RANKING is not actually listed in database, just there for user convenience on print out. Felt like it would be more convenient for later analysis to leave it out of database for now.
print(f"\nDISPLAYED BELOW IS YOUR DATABASE: {databaseFileName}.db\n")

#Formatting database on print out to terminal
print("RANKING" + "\t\tALGORITHM " + "\t\tMIN_EXECUTION_TIME (s)")
print("-------" + "\t\t--------- " + "\t\t----------------------")
for index, item in enumerate(items):
    #Add in ranking of algorithm execution time. Use index to do this by enumerating (essentially adding an assigned index number each sorting algorithm in min_times array).
    #One less indent needed for double digit rowID values. Will need to change again for 3 digits and so on.
    if((index+1) >= 10):
        print(str(index+1) + "     \t\t" + item[0] + "          " + str(item[1]))
    else:
        print(str(index+1) + "      \t\t" + item[0] + "          " + str(item[1]))

#Commit commands to database. Nothing would be executed with respect to the database without this line!
conn.commit()

#Close connection to database
conn.close()