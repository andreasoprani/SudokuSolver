from utility import *


class Cell:
    """
    A class representing a Sudoku cell.

    Attributes:
        xPos: the x position of the cell (from 1 to 9).
        yPos: the y position of the cell (from 1 to 9).
        value: the value assigned to the cell. None if no value is assigned yet.
        domain: a list containing all the possible assignment to the cell.
            Only values between 1 and 9 are allowed.
            If a value is assigned to the cell it must contain only that value.
    """
    xPos = None
    yPos = None
    value = None
    domain = None
    cellsInArcs = None

    def __init__(self, xPos, yPos):
        """
        Initializes an empty cell in a given position.
        :param xPos: the x position of the cell (from 1 to 9).
        :param yPos: the y position of the cell (from 1 to 9).
        """

        if xPos not in getValidValueList():
            raise InvalidPosition("xPos", xPos)
        if yPos not in getValidValueList():
            raise InvalidPosition("yPos", yPos)

        self.xPos = xPos
        self.yPos = yPos
        self.domain = getValidValueList()
        self.cellsInArcs = []

    def __str__(self):
        """
        String representation of the cell.
        :return: the value as a string. If the value is None returns a whitespace.
        """
        if self.value is None:
            return " "
        return str(self.value)

    def SetValue(self, value):
        """
        Sets the value of the cell to a given value.
        The setting is performed only if the previous value is None and the domain includes the value.
        It sets the domain to only contain the given value.
        It also removes the value from other cells domains if there's an arc between this cell and the other one.
        :param value: the value to set.
        """
        if value not in getValidValueList():
            raise InvalidCellValue(value)

        if self.value is None and value in self.domain :
            self.value = value
            self.domain = [value]
            for cell in self.cellsInArcs:
                cell.RemoveFromDomain(value)

    def RemoveFromDomain(self, value):
        """
        Removes a value from the domain.
        :param value: the value to remove.
        """
        if value in self.domain:
            self.domain.remove(value)

    def AutoFill(self):
        """
        Fills automatically the cell if the domain contains only one value.
        """
        if self.value is None and len(self.domain) == 1:
            self.SetValue(self.domain[0])
            return True
        else:
            return False

    def SetCellsInArcs(self, cells):
        """
        Sets the cellsInArcs variable to the given list.
        :param cells: the list of cells that are in constraints alongside with this cell.
        """
        self.cellsInArcs = cells

    def GetUnassignedVariablesConstraints(self):
        return sum(1 for c in self.cellsInArcs if c.value is None)
