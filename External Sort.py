import argparse
import os
import time

class ExternalSort:
    class FilesArray:
        def __init__(self, files):
            self.__files        = files
            self.__emptySet     = set()
            self.__buffers      = {index: None for index in range(len(files))}
            self.__bufferNumber = len(files)
        
        def Refresh(self):
            for index in range(self.__bufferNumber):
                if self.__buffers[index] == None and index not in self.__emptySet:
                    self.__buffers[index] = self.__files[index].readline()
                    
                    if self.__buffers[index] == '':
                        self.__emptySet.add(index)
            
            if len(self.__emptySet) == self.__bufferNumber:
                return False
            
            return True
        
        def Unshift(self, index):
            value                 = self.__buffers[index]
            self.__buffers[index] = None
            
            return value
        
        def GetDictionary(self):
            return {index: self.__buffers[index] for index in range(self.__bufferNumber) if index not in self.__emptySet}
    
    class FileSplitter:
        BLOCK_FILE_FORMAT = 'Block {}.dat'
        
        def __init__(self, path):
            self.__path            = path
            self.__blockFilePathes = list()
        
        def Split(self, blockSize):
            with open(self.__path, 'r') as file:
                blockIndex = 0
                
                while True:
                    lines = file.readlines(blockSize)
                    
                    if lines == list():
                        break
                    
                    lines.sort()
                    
                    self.__WriteBlock(''.join(lines), blockIndex)
                    blockIndex += 1
        
        def CleanBlockFiles(self):
            for blockFilePath in self.__blockFilePathes:
                os.remove(blockFilePath)
        
        def GetBlockFilePathes(self):
            return self.__blockFilePathes
        
        def __WriteBlock(self, data, blockIndex):
            with open(self.BLOCK_FILE_FORMAT.format(blockIndex), 'w') as block:
                block.write(data)
                self.__blockFilePathes.append(self.BLOCK_FILE_FORMAT.format(blockIndex))
    
    class FileMerger:
        def __init__(self, mergeStrategy):
            self.__mergeStrategy = mergeStrategy
        
        def Merge(self, pathes, outputPath, bufferSize):
            with open(outputPath, 'w', bufferSize) as output:
                buffers = ExternalSort.FilesArray(self.__CreateFileHandles(pathes, bufferSize))
                
                while buffers.Refresh():
                    minIndex = self.__mergeStrategy.Select(buffers.GetDictionary())
                    output.write(buffers.Unshift(minIndex))
        
        def __CreateFileHandles(self, pathes, bufferSize):
            files = dict()
            
            for index in range(len(pathes)):
                files[index] = open(pathes[index], 'r', bufferSize)
            
            return files
    
    class NWayMerge:
        def Select(self, dictionary):
            minIndex = -1
            
            for key in dictionary:
                minIndex = key
                break
            
            for index in dictionary:
                if dictionary[index] < dictionary[minIndex]:
                    minIndex = index
            
            return minIndex
    
    def __init__(self, blockSize):
        self.__blockSize = blockSize
    
    def Sort(self, path):
        blockNumber = self.__CalculateBlockNumber(path, self.__blockSize)
        
        fileSplitter = self.FileSplitter(path)
        fileSplitter.Split(self.__blockSize)
        
        fileMerger = self.FileMerger(self.NWayMerge())
        bufferSize = int(self.__blockSize / (blockNumber + 1))
        fileMerger.Merge(fileSplitter.GetBlockFilePathes(), path.split('.')[0] + '.out', bufferSize)
        
        fileSplitter.CleanBlockFiles()
    
    def __CalculateBlockNumber(self, path, blockSize):
        return os.stat(path).st_size / blockSize + 1

def ParseFileSize(fileSize):
    if fileSize[-1].upper() == 'K':
        return int(fileSize[:-1]) * 1024
    elif fileSize[-1].upper() == 'M':
        return int(fileSize[:-1]) * 1024 * 1024
    elif fileSize[-1].upper() == 'G':
        return int(fileSize[:-1]) * 1024 * 1024 * 1024
    
    return int(fileSize)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('file', metavar='<file path>', nargs=1, help='Path of file to sort')
    parser.add_argument('--block_size', metavar='<block size>', help='Size of block to use for sorting', default='100M')
    
    arguments    = parser.parse_args()
    externalSort = ExternalSort(ParseFileSize(arguments.block_size))
    
    startTime = time.process_time()
    externalSort.Sort(arguments.file[0])
    endTime   = time.process_time()
    
    print('[INFO] Elapsed Time = {} seconds'.format(endTime - startTime))