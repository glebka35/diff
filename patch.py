from sys import argv
import numpy as np


class Chunk(object):
    def __init__(self, data):
        filteredData = list(filter(None, data.split("#")))
        self.startIndex = int(filteredData[0])
        self.endIndex = int(filteredData[1])
        self.count = int(filteredData[2])
        if self.count == 0:
            self.data = None
        else:
            self.data = filteredData[3]

    def __str__(self):
        if self.data != None:
            return "startIndex:" + str(self.startIndex) + '\n' \
               + "endIndex:" + str(self.endIndex) + '\n' \
               + "count:" + str(self.count) + '\n' \
               + "data:" + self.data + '\n'
        else:
            return "startIndex:" + str(self.startIndex) + '\n' \
                   + "endIndex:" + str(self.endIndex) + '\n' \
                   + "count:" + str(self.count) + '\n' \
                   + "data:" + "None" + '\n'


def main():
    if len(argv) != 3:
        print("Передайте названия старого файла и файла, содержащего diff")
        exit(1)
    _, oldFileName, diffFileName = argv

    oldFile = open(oldFileName, 'rb+')
    diffFile = open(diffFileName, 'r')

    oldFileData = oldFile.read()
    oldFile.close()

    diffFileData = list(filter(None, diffFile.read().split('$')))
    diffFile.close()

    chunks = [Chunk(e) for e in diffFileData]

    modifiedData = oldFileData
    offset = 0

    for chunk in chunks:
        startIndex = chunk.startIndex
        endIndex = chunk.endIndex

        if chunk.data is None:
            modifiedData = modifiedData[0:startIndex + offset] + modifiedData[endIndex + offset::]
        else:
            modifiedData = modifiedData[0:startIndex + offset] \
                           + bytes(chunk.data, 'utf-8') \
                           + modifiedData[endIndex + offset::]

        offset = chunk.count - (endIndex - startIndex)


    oldFile = open(oldFileName, 'wb')
    oldFile.write(modifiedData)
    oldFile.close()


if __name__ == "__main__":
    main()