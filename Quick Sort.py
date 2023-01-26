import numpy as np

DATA_SIZE = [10, 25, 50, 75, 100, 250, 500, 750, 1000, 2500]

def ParsePivotArgument(pivot, start, end):
    return { 'start': start, 'middle': (start + end) // 2, 'end': end }.get(pivot, -1)

def QuickSort(data, start, end, pivot='start', count=0):
    if end - start <= 0:
        return count
    
    pivotIndex  = ParsePivotArgument(pivot, start, end)
    searchIndex = start + 1
    
    data[start], data[pivotIndex] = data[pivotIndex], data[start]
    
    for index in range(start + 1, end + 1):
        count += 1
        
        if data[index] < data[start]:
            data[index], data[searchIndex]  = data[searchIndex], data[index]
            searchIndex                    += 1
    
    data[start], data[searchIndex - 1] = data[searchIndex - 1], data[start]
    
    count = QuickSort(data, start, searchIndex - 2, pivot, count + 1)
    count = QuickSort(data, searchIndex, end, pivot, count + 1)
    
    return count

if __name__ == '__main__':
    for index in range(len(DATA_SIZE)):
        print('Count for Forward Data Number {}:\t{}'.format(DATA_SIZE[index], QuickSort(np.arange(0, DATA_SIZE[index], 1), 0, DATA_SIZE[index] - 1, pivot='start')))
        print('Count for Reverse Data Number {}:\t{}'.format(DATA_SIZE[index], QuickSort(np.arange(DATA_SIZE[index], 0, -1), 0, DATA_SIZE[index] - 1, pivot='start')))
        print('Count for Random Data Number {}:\t{}'.format(DATA_SIZE[index], QuickSort(np.random.randint(DATA_SIZE[index], size=DATA_SIZE[index]), 0, DATA_SIZE[index] - 1, pivot='start')))