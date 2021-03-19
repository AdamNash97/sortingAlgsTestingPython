# sortingAlgsTestingPython

This code is written to allow one to implement various types of sorting algorithms and then carry out time testing (wall-clock) on them for a given data input. The data input 
and number of repetitions of sorting can be altered by the user. I followed instructions and code from  this site for the most part:
https://realpython.com/sorting-algorithms-python/ , whilst making various alterations to the code along the way.

I tested 10 different sorting algorithms in total using the same data input, and the following sites are where you can find the source of said algorithms, as well as the 
site mentioned above.

https://stackabuse.com/bucket-sort-in-python/
https://www.geeksforgeeks.org/radix-sort/
https://www.geeksforgeeks.org/heap-sort/

Following the time testing implementation, I went on to write code that would allow the user to create a database using SQLite that stores the name of the algorithm
being tested alongside the minimum execution time that is observed (in seconds). The database is then ordered to provide an ascending time efficiency ranking. The
final database is saved to the user's current directory under a file name of their choosing that is entered upon being prompted by the program.
