import numpy as np

DATA_SIZE = [10, 25, 50, 75, 100, 250, 500, 750, 1000, 2500]

def MergeSort(data, count=0):
    if len(data) <= 1:
        return count
    
    pivot      = len(data) // 2
    leftGroup  = data[:pivot]
    rightGroup = data[pivot:]
    
    count = MergeSort(leftGroup, count + 1)
    count = MergeSort(rightGroup, count + 1)
    
    leftGroupIndex  = 0
    rightGroupIndex = 0
    mergingIndex    = 0
    
    while leftGroupIndex < len(leftGroup) and rightGroupIndex < len(rightGroup):
        if leftGroup[leftGroupIndex] < rightGroup[rightGroupIndex]:
            data[mergingIndex]  = leftGroup[leftGroupIndex]
            leftGroupIndex     += 1
            mergingIndex       += 1
            count              += 1
        else:
            data[mergingIndex]  = rightGroup[rightGroupIndex]
            rightGroupIndex    += 1
            mergingIndex       += 1
            count              += 1
    
    while leftGroupIndex < len(leftGroup):
        data[mergingIndex]  = leftGroup[leftGroupIndex]
        leftGroupIndex     += 1
        mergingIndex       += 1
        count              += 1
    
    while rightGroupIndex < len(rightGroup):
        data[mergingIndex]  = rightGroup[rightGroupIndex]
        rightGroupIndex    += 1
        mergingIndex       += 1
        count              += 1
    
    return count

if __name__ == '__main__':
    for index in range(len(DATA_SIZE)):
        print('Count for Forward Data Number {}:\t{}'.format(DATA_SIZE[index], MergeSort(np.arange(0, DATA_SIZE[index], 1))))
        print('Count for Reverse Data Number {}:\t{}'.format(DATA_SIZE[index], MergeSort(np.arange(DATA_SIZE[index], 0, -1))))
        print('Count for Random Data Number {}:\t{}'.format(DATA_SIZE[index], MergeSort(np.random.randint(DATA_SIZE[index], size=DATA_SIZE[index]))))