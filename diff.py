from sys import argv
import numpy as np


def createPath(a, b, dist):
    i = len(a)
    j = len(b)
    path = [(i, j)]
    while i > 0 or j > 0:
        if i == 0:
            path.append((i, j - 1))
            j = j - 1
        elif j == 0:
            path.append((i - 1, j))
            i = i - 1
        else:
            nextPoint = min(dist[i][j-1] + 1, dist[i-1][j] + 1, dist[i-1][j-1] + (a[i-1] != b[j-1]))
            if nextPoint == dist[i-1][j-1] + (a[i-1] != b[j-1]):
                path.append((i - 1, j - 1))
                i = i - 1
                j = j - 1
            elif nextPoint == dist[i][j-1] + 1:
                path.append((i, j - 1))
                j = j - 1
            elif nextPoint == dist[i-1][j] + 1:
                path.append((i - 1, j))
                i = i - 1
    return path


def my_dist(a, b):
    dist = np.zeros((len(a) + 1, len(b) + 1))
    for i in range(len(a) + 1):
        for j in range(len(b) + 1):
            if i == 0:
                if j != 0:
                    dist[i][j] = j
            if j == 0:
                if i != 0:
                    dist[i][j] = i

            if i != 0 and j != 0:
                dist[i][j] = min(dist[i][j - 1] + 1, dist[i - 1][j] + 1, dist[i - 1][j - 1] + (a[i - 1] != b[j - 1]))
    return dist

def create_diff_file(fileName, path, a, b):
    f = open(fileName, "w")
    curPoint = path.pop()
    modifyingInProgress = False
    startModifyingInterval = 0
    endModifyingInterval = 0
    changes = []

    while len(path) > 0:
        prevPoint = curPoint
        curPoint = path.pop()

        if curPoint[0] == prevPoint[0] + 1 and curPoint[1] == prevPoint[1] + 1 and a[curPoint[0] - 1] == b[curPoint[1] - 1]:
            if modifyingInProgress:
                f.write('#' + str(startModifyingInterval) + '#' + str(endModifyingInterval) + '#' + str(len(changes)) + "#")
                f.write(''.join(chr(e) for e in changes))
                f.write('$')
                modifyingInProgress = False
                changes = []
        elif curPoint[0] == prevPoint[0] + 1 and curPoint[1] == prevPoint[1] + 1 and a[curPoint[0] - 1] != b[curPoint[1] - 1]:
            if not modifyingInProgress:
                modifyingInProgress = True
                startModifyingInterval = curPoint[0] - 1

            endModifyingInterval = curPoint[0]
            changes.append(b[curPoint[1] - 1])
        elif curPoint[0] == prevPoint[0] + 1:
            if not modifyingInProgress:
                modifyingInProgress = True
                startModifyingInterval = curPoint[0] - 1

            endModifyingInterval = curPoint[0]

        elif curPoint[1] == prevPoint[1] + 1:
            if not modifyingInProgress:
                modifyingInProgress = True
                startModifyingInterval = curPoint[0]
                endModifyingInterval = startModifyingInterval

            changes.append(b[curPoint[1] - 1])

    if modifyingInProgress:
        f.write('#' + str(startModifyingInterval) + '#' + str(endModifyingInterval) + '#' + str(len(changes)) + "#")
        f.write(''.join(chr(e) for e in changes))
        f.write('$')

    f.close()


def main():
    if len(argv) != 4:
        print("Передайте названия старого и нового файлов, а также файл для diff")
        exit(1)
    _, oldFileName, newFileName, diffFileName = argv

    fileOld = open(oldFileName, 'rb')
    fileNew = open(newFileName, 'rb')

    fileOldData = fileOld.read()
    fileNewData = fileNew.read()

    fileOld.close()
    fileNew.close()

    distanceTable = my_dist(fileOldData, fileNewData)
    path = createPath(fileOldData, fileNewData, distanceTable)
    create_diff_file(diffFileName, path, fileOldData, fileNewData)


if __name__ == "__main__":
    main()
