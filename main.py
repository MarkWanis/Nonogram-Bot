'''
Outline:

drawRowData:
1. For loop through every row in the data
2. For loop through every piece of data in the row
3. Finds x and y positions
  x = offset + (dataLength - len(row) + dataIndex) * cellSize
  y = (dataLength + rowIndex) * cellSize
  
drawColData:
1. For loop through every col in the data
2. For loop through every piece of data in the col
3. Finds x and y positions
  x = offset + (dataLength + colIndex) * cellSize
  y = (dataLength - len(col) + dataIndex) * cellSize
  
evaluateLine(index, lineType):
1. Finds values of the line and the data of the line
2. Finds every empty space creates a binary representation of them, where 0 is 'O' and 1 is 'X'
3. Iterates through every binary combination
  Converts back to letters
  Inserts the letters into a temp line
  Converts line to data format
  Checks to see if data is equal to actual data of the line
  If data matches, append temp line to possible combinations
4. After all combinations have been checked, finds the cells that are filled in every combination and the cells that are never filled
  consistentFilledCells
  consistentEmptyCells
5. Goes through every consistent filled and empty cell and places Os and Xs respectively
'''
#'''
# Imports
import pygame
import time

from pygame import draw

# Initializes pygame
pygame.init()

################################################################
# Screen Variables
################################################################

height = 800 # Height of screen
width = height * 1.6 # Width of screen
offset = (width - height) // 2 # Calculates horizontal offset

clock = pygame.time.Clock()

################################################################
# Nonogram Data
################################################################

# Returns the length of the longest list in the 2D list
def maxListLength(list):
  max = 1
  for line in list:
    if len(line) > max:
      max = len(line)
  return max
'''
rowData = [
  [1],          
  [1],    
  [3],    
  [1, 1],    
  [2, 2],      
  [0],    
  [8, 8],       
  [7, 7],         
  [7, 2, 7],         
  [4, 4, 4],          
  [5, 3, 5],          
  [21],          
  [2, 13, 2],          
  [1, 2, 7, 2, 1],          
  [2, 7, 2],  
  [9],
  [1, 11, 1],
  [1, 1, 5, 1, 1],
  [2, 7, 2],
  [1, 7, 1],
  [2, 4, 4, 2],
  [1, 4, 4, 1],
  [2, 4, 4, 2],
  [1, 4, 4, 1],
  [5, 4, 4, 5]
]
colData = [
  [1],          
  [1, 3],    
  [2, 3, 3, 1],       
  [3, 2, 3, 1],   
  [6, 3, 1], 
  [6], 
  [9, 1],       
  [9, 2, 3],       
  [2, 3, 2, 5],       
  [1, 6, 7],       
  [1, 1, 1, 13],       
  [3, 14],       
  [3, 12],         
  [3, 13],       
  [1, 1, 13],           
  [1, 6, 7],
  [2, 3, 2, 5],
  [9, 2, 3],
  [9, 1],
  [6],
  [6, 3, 1],
  [3, 2, 3, 1],
  [2, 3, 3, 1],
  [1, 3],
  [1],
]
'''
#'''
rowData = [
  [2],
  [2, 1],
  [2, 4],
  [2, 1, 2, 2],
  [8, 2, 1],
  [2, 4, 4],
  [2, 4, 1, 2],
  [2, 8, 1],
  [9, 2, 1],
  [4, 3, 6],
  [8, 4, 1],
  [14],
  [4, 4],
  [6],
  [4]
]
colData = [
  [3],
  [2, 6],
  [10],
  [1, 2, 4],
  [2, 3, 2],
  [2, 10],
  [15],
  [1, 13],
  [2, 2, 2, 4],
  [2, 3, 2],
  [2, 7],
  [10],
  [1, 2, 4],
  [2, 3, 2],
  [3]
]
#'''
dataLength = max([maxListLength(rowData), maxListLength(colData)])
cellsPerRow = len(rowData) # Number of cells per row
cellSize = height // (cellsPerRow + dataLength) # Pixel size of each cell
'''
nonogramBoard = [
  ['E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E'],
  ['E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E'],
  ['E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E'],
  ['E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E'],
  ['E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E'],
  ['E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E'],
  ['E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E'],
  ['E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E'],
  ['E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E'],
  ['E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E'],
  ['E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E'],
  ['E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E'],
  ['E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E'],
  ['E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E'],
  ['E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E'],
  ['E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E'],
  ['E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E'],
  ['E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E'],
  ['E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E'],
  ['E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E'],
  ['E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E'],
  ['E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E'],
  ['E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E'],
  ['E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E'],
  ['E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E'],
]
'''
nonogramBoard = [
  ['E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E'],
  ['E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'X', 'E', 'E', 'E', 'E'],
  ['E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'X', 'E'],
  ['E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E'],
  ['E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E'],
  ['E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E'],
  ['E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E'],
  ['E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E'],
  ['E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E'],
  ['E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E'],
  ['E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E'],
  ['E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E'],
  ['E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E'],
  ['E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E'],
  ['E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E']
]
'''
nonogramBoard = [
  ['E', 'E', 'E', 'E', 'E'],
  ['E', 'E', 'E', 'E', 'E'],
  ['E', 'E', 'E', 'E', 'E'],
  ['E', 'E', 'E', 'E', 'E'],
  ['E', 'E', 'E', 'E', 'E']
]
'''
################################################################
# Functions
################################################################

# Draws the row and col data onto the screen
def drawData(screen):

  drawRowData(screen)
  drawColData(screen)

# Draws the row data onto the screen
def drawRowData(screen):

  fontSize = 50
  font = pygame.font.Font(None, fontSize)

  for rowIndex, row in enumerate(rowData):
    for dataIndex, data in enumerate(row):
      x = offset + (dataLength - len(row) + dataIndex) * cellSize
      y = (dataLength + rowIndex) * cellSize

      numberSurface = font.render(str(data), True, 'Black')
      numberRect = numberSurface.get_rect(center=(x + cellSize // 2, y + cellSize // 2))
      screen.blit(numberSurface, numberRect)

# Draws the col data onto the screen
def drawColData(screen):

  fontSize = 50
  font = pygame.font.Font(None, fontSize)

  for colIndex, col in enumerate(colData):
    for dataIndex, data in enumerate(col):
      x = offset + (dataLength + colIndex) * cellSize
      y = (dataLength - len(col) + dataIndex) * cellSize

      numberSurface = font.render(str(data), True, 'Black')
      numberRect = numberSurface.get_rect(center=(x + cellSize // 2, y + cellSize // 2))
      screen.blit(numberSurface, numberRect)

# Draws the nonogram board onto the screen
def drawBoard(screen):

  fontSize = 50
  font = pygame.font.Font(None, fontSize)

  for row in range(cellsPerRow):
    for col in range(cellsPerRow):
      x = offset + (dataLength + col) * cellSize
      y = (dataLength + row) * cellSize

      if nonogramBoard[row][col] == 'E':
        continue

      if nonogramBoard[row][col] == 'X':
        letterSurface = font.render('X', True, 'Black')
        letterRect = letterSurface.get_rect(center=(x + cellSize // 2, y + cellSize // 2))
        screen.blit(letterSurface, letterRect)

      elif nonogramBoard[row][col] == 'O':
        pygame.draw.rect(screen, 'Black', (x, y, cellSize, cellSize))

      else:
        print('Draw Board Error')
    
# Creates a grid of lines
def grid(screen):

  for row in range(cellsPerRow + 1):
      for col in range(cellsPerRow + 1):
          x, y = col * cellSize + offset + dataLength * cellSize, row * cellSize + dataLength * cellSize

          pygame.draw.line(screen, 'Black', (x, 0), (x, height), 3) # Vertical lines
          pygame.draw.line(screen, 'Black', (offset, y), (width - offset, y), 3) # Horizontal lines

# Iterates through every row and col in the board and updates it
def evaluateBoard(screen):

  evaluateRows(screen)
  evaluateCols(screen)

# Iterates through every row in the board and updates it
def evaluateRows(screen):

  for rowIndex in range(cellsPerRow):
    evaluateLine(rowIndex, 'Row')
    redraw(screen)
    

# Iterates through every col in the board and updates it
def evaluateCols(screen):

  for colIndex in range(cellsPerRow):
    evaluateLine(colIndex, 'Col')
    redraw(screen)

# Evaluates the given line and identifies the knowns and unknowns of the line, then updates the board
def evaluateLine(lineIndex, lineType):

  data = grabData(lineIndex, lineType)
  line = grabLine(lineIndex, lineType)

  if 'E' not in line:
    return None
  
  validCombinations = findCombinations(data, line) 

  consistentFilledCells, consistentEmptyCells = findConsistentCells(validCombinations)

  updateBoard(consistentFilledCells, consistentEmptyCells, lineIndex, lineType)

# Updates the board with filled and empty cells
def updateBoard(filledCells, emptyCells, lineIndex, lineType):

  # Updates board with filled cells
  if lineType == 'Row':
    for cell in filledCells: # Ex: [1, 2, 3]
      nonogramBoard[lineIndex][cell] = 'O'
  elif lineType == 'Col':
    for cell in filledCells: # Ex: [1, 2, 3]
      nonogramBoard[cell][lineIndex] = 'O'

  # Updates board with empty cells
  if lineType == 'Row':
    for cell in emptyCells: # Ex: [1, 2, 3]
      nonogramBoard[lineIndex][cell] = 'X'
  elif lineType == 'Col':
    for cell in emptyCells: # Ex: [1, 2, 3]
      nonogramBoard[cell][lineIndex] = 'X'
  else:
    print('Update Board Error')

# Looks through every combination and finds the cells that are consistently filled or empty
def findConsistentCells(combinations):

  consistentFilledCells = findFilledCells(combinations[0]) 
  consistentEmptyCells = findEmptyCells(combinations[0])

  for combination in combinations:

    filledCells = findFilledCells(combination)
    emptyCells = findEmptyCells(combination)

    consistentFilledCells = compareCells(consistentFilledCells, filledCells)
    consistentEmptyCells = compareCells(consistentEmptyCells, emptyCells) 

  return consistentFilledCells, consistentEmptyCells

# Given a line, return the indices of the filled cells
def findFilledCells(line):

  filledCells = []

  for cellIndex, cell in enumerate(line):
    if cell == 'O':
      filledCells.append(cellIndex)

  return filledCells

# Given a line, return the indices of the empty cells
def findEmptyCells(line):

  emptyCells = []

  for cellIndex, cell in enumerate(line):
    if cell == 'X':
      emptyCells.append(cellIndex)

  return emptyCells

# Compares to lists of indices and removes the values that are not in both lists
def compareCells(oldList, newList):

  for cellIndex in oldList:
    if cellIndex not in newList:
      oldList.remove(cellIndex)

  return oldList

# Converts all of the empty spaces to binary bits and checks every combination to see if it's valid
# Iterates through every combination of the blank spaces and returns the valid combinations
def findCombinations(data, line):

  validCombinations = []
  blankCells = findBlankCells(line) 
  totalCombinations = 2 ** len(blankCells)
  filledCells = countFilledCells(line)

  combIndex = 0
  while combIndex < totalCombinations:
  #for index in range(totalCombinations):
    binaryCombination = bin(combIndex)[2:].zfill(len(blankCells)) # Binary representation of blank cells

    bitSum = binaryCombination.count('1')
    if bitSum + filledCells != sum(data): # Continues if filled cells not correct
      combIndex += 1
      continue
    
    combination = binaryToCells(binaryCombination) # Converts the binary to values in a cell
    lineCopy = insertCombinationIntoLine(line.copy(), combination, blankCells)

    if lineToData(lineCopy) == data: # Checks if data of lineCopy is equal to the actual data
      validCombinations.append(lineCopy) # Appends line if it's equal

    combIndex += 1

  return validCombinations

# Counts the number of filled cells in the given line
def countFilledCells(line):

  filledCells = 0

  for cell in line:
    if cell == 'O':
      filledCells += 1

  return filledCells

# Inserts the values in combination at the indices given by blankCells into the given line and returns it
def insertCombinationIntoLine(line, combination, blankCells):

  for cellIndex, cell in enumerate(blankCells): # Enumerates through blankCells
    line[cell] = combination[cellIndex]

  return line

# Converts the given line to a list in the data format, Ex: ['O', 'X', 'O'] >> [1, 1]
def lineToData(line):

  data = [0]

  for cell in line:
    if cell == 'O':
      data[-1] += 1

    elif cell == 'X' and data[-1] != 0:
      data.append(0)

  if data[-1] == 0 and len(data) > 1:
    del data[-1]

  return data

# Converts the given binary number to values in a cell
def binaryToCells(bits): # 01100 >> ['X', 'O', 'O', 'X', 'X']

  return ['O' if bit == '1' else 'X' for bit in bits]
    
# Searches given list of cells and returns a list of the indices of every blank cell
def findBlankCells(line):

  blankCells = []

  for cellIndex, cell in enumerate(line):
    if cell == 'E':
      blankCells.append(cellIndex)

  return blankCells

# Grabs and returns the data at the given index and lineType
def grabData(index, lineType):

  if lineType == 'Row':
    return rowData[index]

  elif lineType == 'Col':
    return colData[index]

  else:
    print('Grab Data Error')

# Grabs and returns the line at the given index and lineType
def grabLine(index, lineType):

  if lineType == 'Row':
    return nonogramBoard[index]

  elif lineType == 'Col':
    return [nonogramBoard[row][index] for row in range(cellsPerRow)]

  else:
    print('Grab Line Error')
    return []

# Redraws the screen
def redraw(screen):

  screen.fill('White')
  grid(screen)
  drawData(screen)
  drawBoard(screen)
  pygame.display.update()

# Main function
def main():

  # Sets screen size
  screen = pygame.display.set_mode((width, height), pygame.FULLSCREEN)
  
  redraw(screen)

  running = True
  
  while running:

    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        exit()
        
    redraw(screen)

    evaluateBoard(screen)
    
    time.sleep(.5)

main()
#'''
