import numpy as np
import random as rd
from copy import copy
def getInitialMatrix(rows: int, columns: int) -> np.ndarray:
    return np.random.randint(0,2,(rows, columns),dtype=np.uint8)

def _getNeighbors(matrix: np.ndarray, i: int, j: int) -> np.ndarray:
    """
    Args:
        matrix (np):source matrix
        i (int): row number
        j (int): column number
    Returns:
        np: matrix of neighbors
    """ 
    i_min = max(i - 1, 0)
    i_max = min(i + 2, matrix.shape[0])
    j_min = max(j - 1, 0)
    j_max = min(j + 2, matrix.shape[1])
    return matrix[i_min:i_max, j_min:j_max] 

def getNextMatrix(matrix: np.ndarray) -> np.ndarray:
    """ gets new life game matrix based on algorithm described in
        https://playgameoflife.com/info
    Args:
        matrix (np): current matrix

    Returns:
        np: new matrix
    """
    res: np.ndarray = np.zeros((matrix.shape[0], matrix.shape[1]), dtype=np.uint8)
    for i in range(matrix.shape[0]):
        for j in range(matrix.shape[1]):
            res[i][j] = _getNewValue(matrix, i, j)
    return res

def _getNewValue(matrix: np.ndarray, i: int, j: int) -> int:
    """based on matrix[i][j] returns new value in accordance with 
       https://playgameoflife.com/info

    Args:
        matrix (np): current matrix
        i (int): row number
        j (int): column number

    Returns:
        int: new matrix value
    """ 
    neighbors: np.ndarray = _getNeighbors(matrix, i, j)
    numberOfNeighbors = _getNumberOfNeghbors(matrix, i, j, neighbors)
    return _newValue(matrix[i][j], numberOfNeighbors) 

def _getNumberOfNeghbors(matrix:np, i: int, j: int, neighbors:np)->int:
    """subtracts current value matrix[i][j] from sum of neighbors matrix 

    Args:
        matrix (np): current matrix
        i (int): number of row
        j (int): number of column
        neighbors (np): matrix of naighbors

    Returns:
        int: new matrix value
    """    
    return np.sum(neighbors) - matrix[i][j] 

def _newValue(cur: int, nNeighbors: int)->int:
    """defines new value based on the current one and number of neighbors

    Args:
        cur (int): current life matrix value
        nNeighbors (int): number of neighbors in the current life matrix

    Returns:
        int: new value
    """  
    return int(_remainsAlive(nNeighbors) if cur else _becomesAlive(nNeighbors))  
    
def _remainsAlive(nNeighbors: int)-> bool :
    """
    Args:
        nNeighbors (int): number of neighbors

    Returns:
        bool: true or false according to number of neighbors for the alive
    """       
    return 1 < nNeighbors < 4    

def _becomesAlive(nNeighbors: int)-> bool :
    """
    Args:
        nNeighbors (int): number of neighbors

    Returns:
        bool: true or false according to number of neighbors for the dead
    """       
    return nNeighbors == 3       
