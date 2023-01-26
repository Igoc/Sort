import numpy as np

DATA_SIZE = [10, 25, 50, 75, 100, 250, 500, 750, 1000, 2500]

def SelectionSort(data):
    count = 0
    
    for index in range(0, len(data) - 1):
        minimumIndex = index
        
        for searchIndex in range(index + 1, len(data)):
            count += 1
            
            if data[searchIndex] < data[minimumIndex]:
                minimumIndex = searchIndex
        
        data[index], data[minimumIndex] = data[minimumIndex], data[index]
    
    return count

if __name__ == '__main__':
    for index in range(len(DATA_SIZE)):
        print('Count for Forward Data Number {}:\t{}'.format(DATA_SIZE[index], SelectionSort(np.arange(0, DATA_SIZE[index], 1))))
        print('Count for Reverse Data Number {}:\t{}'.format(DATA_SIZE[index], SelectionSort(np.arange(DATA_SIZE[index], 0, -1))))
        print('Count for Random Data Number {}:\t{}'.format(DATA_SIZE[index], SelectionSort(np.random.randint(DATA_SIZE[index], size=DATA_SIZE[index]))))