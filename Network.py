import copy
import math


class Network:
    '''
    A class for a network of nodes
    '''
    def __init__(self, nodes={}):
        '''
        The graph is stored as a dictionary of nodes with an ID as the key
        and a dictionary for the nodes connections {connectedNodeID:weight}
        '''
        self.nodes = nodes

    def checkEulerianPath(self):
        '''
        Function to check if a connected network has a Eulerian path or cycle.
        Returns 2 if there is a Eulerian cycle, 1 if there is only an
        Eulerian path and 0 if neither exists.
        '''
        oddVertices = []
        for key, value in self.nodes.items():
            if len(value) % 2 != 0:
                oddVertices.append(key)
        if len(oddVertices) == 2:
            return 1
        elif len(oddVertices) == 0:
            return 2
        else:
            return 0

    def isConnected(self):
        '''
        Function to walk through a network and test if all nodes are connected
        '''
        # set to store nodes that have been checked
        connectedNodes = set()
        # list to store unchecked nodes
        nodesToBeChecked = [next(iter(self.nodes))]

        while len(nodesToBeChecked) != 0:
            # active node to check connections for
            activeNodeID = nodesToBeChecked.pop(0)
            # for every node connected to the active node add to
            # nodesToBeChecked if it has not already been checked
            for node in iter(self.nodes[activeNodeID]):
                if node not in connectedNodes:
                    nodesToBeChecked.extend(node)
            # add the checked node to the set of checked nodes
            connectedNodes.add(activeNodeID)
        # if there are as many checked nodes as nodes in the network then the
        # network is connected (nodes can only be checked if they're connected)
        if len(connectedNodes) == len(self.nodes):
            return True
        else:
            return False

    def findEulerianPath(self):
        '''
        Function to find a Eulerian Path or cycle through a network of nodes
        should one exist. Returns the path as a list of node ID's
        '''
        if self.checkEulerianPath() == 0:
            print('There is no Eulerian Path')
            return
        else:
            firstNodeID = ''
            eulerianPathList = []
            if self.checkEulerianPath() == 1:
                # find a node with odd number of vertices to start from
                for nodeID, connections in self.nodes.items():
                    if len(connections) % 2 != 0:
                        firstNodeID = nodeID
                        break
            else:
                firstNodeID = next(iter(self.nodes))

            pathNotFound = True
            # failedPaths requires a default tuple to iterate over later
            failedPaths = [(0, 0, 0)]
            while pathNotFound:
                # make a copy to preserve the original network
                tempNetwork = copy.deepcopy(self.nodes)
                loopNumber = 0
                activeNodeID = firstNodeID
                checkpointNode = ()
                while len(tempNetwork[activeNodeID]) != 0:
                    loopNumber += 1
                    # add the current node to the list
                    eulerianPathList.append(activeNodeID)
                    # find a node connected to the current node to travel to
                    connectionIter = iter(tempNetwork[activeNodeID])
                    nextNodeID = next(connectionIter)
                    # if the node has more than 2 connections create
                    # a checkpoint stored as a tuple
                    if len(tempNetwork[activeNodeID]) > 2:
                        checkpointNode = (activeNodeID, nextNodeID, loopNumber)
                    # check if the decided path leads to a failed path
                    # if so try a different path
                    while True:
                        for fail in failedPaths:
                            if (activeNodeID, nextNodeID, loopNumber) == fail:
                                nextNodeID = next(connectionIter)
                        break
                    # delete the pathways from both nodes to prevent the same
                    # path being used twice
                    del tempNetwork[activeNodeID][nextNodeID]
                    del tempNetwork[nextNodeID][activeNodeID]
                    # change the active node to the one travelled to
                    activeNodeID = nextNodeID
                # loop to detect if any paths still remain
                failed = False
                for connections in tempNetwork.values():
                    if len(connections) != 0:
                        failed = True
                        break
                if failed:
                    # if the path created has not travelled all edges, the path
                    # has gone wrong and the last created checkpoint is
                    # recorded in failedPaths
                    failedPaths.append(checkpointNode)
                    # clearing variables before resetting the loop
                    eulerianPathList.clear()
                    loopNumber = 0
                    del tempNetwork
                else:
                    pathNotFound = False
                    # adding on the end point of the loop
                    eulerianPathList.append(activeNodeID)
            return eulerianPathList

    def findDijkstraPath(self, start, end='ALLNODES'):
        '''
        Function to use Dijkstra's algorithm to find the shortest path through
        a network. If no end node is given return a dictionary with the
        shortest path to all nodes
        '''
        def findNextNode(SPT, distance):
            distanceTemp = copy.copy(distance)
            while True:
                for k, v in distance.items():
                    if v == min(distanceTemp.values()) and k not in SPT:
                        return k
                    elif v == min(distanceTemp.values()) and k in SPT:
                        del distanceTemp[k]
                        break
                    else:
                        pass

        if start not in self.nodes.keys():
            print('The start node cannot be found in the network.')
            return
        elif end not in self.nodes.keys():
            print('The end node cannot be found in the network.')
            return
        SPT = set()
        # create a dictionary to store the distance from the source and the
        # path required to get there
        distance = {x: [math.inf, []] for x in self.nodes.keys()}
        # reduce the distance to the start node to 0
        distance[start][0] = 0
        distance[start][1].append(start)
        # loop until all vertices have been added to SPT
        while SPT != set(self.nodes.keys()):
            # find the node with the minimum distance not in SPT
            currentNode = findNextNode(SPT, distance)
            SPT.add(currentNode)
            # change the distance values of adjecent nodes
            for k, v in self.nodes[currentNode].items():
                # check to see if the path is shorter
                if distance[k][0] > distance[currentNode][0] + v:
                    # change the distance value
                    distance[k][0] = distance[currentNode][0] + v
                    # change the list to that of the path taken
                    distance[k][1].clear()
                    distance[k][1].extend(distance[currentNode][1])
                    distance[k][1].append(k)
        # return the whole distance dictionary or the value for the end node
        if end == 'ALLNODES':
            return distance
        else:
            return distance[end]


if __name__ == '__main__':
    point1 = {'1': {'0': 1, '2': 1}}
    point2 = {'2': {'0': 1, '1': 1}}
    point0 = {'0': {'1': 1, '2': 1, '3': 1}}
    point3 = {'3': {'0': 1, '4': 1}}
    point4 = {'4': {'3': 1}}
    eulerNetwork = Network({**point1, **point2, **point0, **point3, **point4})
    if eulerNetwork.checkEulerianPath() == 2:
        print('The network has an eulerian cycle.')
    elif eulerNetwork.checkEulerianPath() == 1:
        print('The network has an eulerian path.')
    else:
        print('The network does not have a eulerian path.')
    if eulerNetwork.isConnected():
        print('The network is connected')
    else:
        print('The network is not connected')
    eulerianList = eulerNetwork.findEulerianPath()
    print(eulerianList)
    point0 = {'0': {'1': 4, '7': 8}}
    point1 = {'1': {'0': 4, '2': 8, '7': 11}}
    point2 = {'2': {'1': 8, '3': 7, '8': 2, '5': 4}}
    point3 = {'3': {'2': 7, '4': 9, '5': 14}}
    point4 = {'4': {'3': 9, '5': 10}}
    point5 = {'5': {'4': 10, '3': 14, '2': 4, '6': 2}}
    point6 = {'6': {'5': 2, '8': 6, '7': 1}}
    point7 = {'7': {'0': 8, '1': 11, '8': 7, '6': 1}}
    point8 = {'8': {'2': 2, '6': 6, '7': 7}}
    dijNetwork = Network({**point0, **point1, **point2, **point3, **point4,
                         **point5, **point6, **point7, **point8})
    result = dijNetwork.findDijkstraPath('0', '4')
    print(result)
