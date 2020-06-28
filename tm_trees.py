from __future__ import annotations
import os
import math
from random import randint
from typing import List, Tuple, Optional


class TMTree:
    """A TreeMappableTree: a tree that is compatible with the treemap
    visualiser.

    This is an abstract class that should not be instantiated directly.

    You may NOT add any attributes, public or private, to this class.
    However, part of this assignment will involve you implementing new public
    *methods* for this interface.
    You should not add any new public methods other than those required by
    the client code.
    You can, however, freely add private methods as needed.

    === Public Attributes ===
    rect:
        The pygame rectangle representing this node in the treemap
        visualization.
    data_size:
        The size of the data represented by this tree.

    === Private Attributes ===
    _colour:
        The RGB colour value of the root of this tree.
    _name:
        The root value of this tree, or None if this tree is empty.
    _subtrees:
        The subtrees of this tree.
    _parent_tree:
        The parent tree of this tree; i.e., the tree that contains this tree
        as a subtree, or None if this tree is not part of a larger tree.
    _expanded:
        Whether or not this tree is considered expanded for visualization.

    === Representation Invariants ===
    - data_size >= 0
    - If _subtrees is not empty, then data_size is equal to the sum of the
      data_size of each subtree.

    - _colour's elements are each in the range 0-255.

    - If _name is None, then _subtrees is empty, _parent_tree is None, and
      data_size is 0.
      This setting of attributes represents an empty tree.

    - if _parent_tree is not None, then self is in _parent_tree._subtrees

    - if _expanded is True, then _parent_tree._expanded is True
    - if _expanded is False, then _expanded is False for every tree
      in _subtrees
    - if _subtrees is empty, then _expanded is False
    """

    rect: Tuple[int, int, int, int]
    data_size: int
    _colour: Tuple[int, int, int]
    _name: str
    _subtrees: List[TMTree]
    _parent_tree: Optional[TMTree]
    _expanded: bool

    def __init__(self, name: str, subtrees: List[TMTree],
                 data_size: int = 0) -> None:
        """Initialize a new TMTree with a random colour and the provided <name>.

        If <subtrees> is empty, use <data_size> to initialize this tree's
        data_size.

        If <subtrees> is not empty, ignore the parameter <data_size>,
        and calculate this tree's data_size instead.

        Set this tree as the parent for each of its subtrees.

        Precondition: if <name> is None, then <subtrees> is empty.
        """
        self._name = name
        self._subtrees = subtrees
        self.data_size = data_size
        self.rect = (0, 0, 0, 0)
        self._colour = (randint(0, 255), randint(0, 255), randint(0, 255))


    def is_empty(self) -> bool:
        """Return True iff this tree is empty.
        """
        return self._name is None

    def update_rectangles(self, rect: Tuple[int, int, int, int]) -> None:
        """Update the rectangles in this tree and its descendents using the
        treemap algorithm to fill the area defined by pygame rectangle <rect>.
        """
        # Read the handout carefully to help get started identifying base cases,
        # then write the outline of a recursive step.
        #
        # Programming tip: use "tuple unpacking assignment" to easily extract
        # elements of a rectangle, as follows.
        x, y, width, height = rect
        self.rect = (x, y, width, height)
        if self._subtrees == [] or self.data_size == 0:
            return
        delta = 0

        for i in range(0, len(self._subtrees)):
            if width >= height:
                if i == 0:
                    x2 = x
                else:
                    x2 = self._subtrees[i-1].rect[0] + \
                         self._subtrees[i-1].rect[2]

                flot = (self._subtrees[i].data_size/self.data_size)*width
                if abs(x2 + flot + delta - (x + width)) < 0.001:
                    width2 = x + width - x2
                    delta = 0
                else:
                    width2 = int(flot)
                    delta += flot - width2
                height2 = height
                y2 = y

            else:
                if i == 0:
                    y2 = y
                else:
                    y2 = self._subtrees[i-1].rect[1] +\
                         self._subtrees[i-1].rect[3]
                flot = (self._subtrees[i].data_size/self.data_size)*height
                if abs(y2 + flot + delta - (y + height)) < 0.001:
                    height2 = y + height - y2
                    delta = 0
                else:
                    height2 = int(flot)
                    delta += flot - height2

                x2 = x
                width2 = width

            # consider cases for when its rightmost or bottommost
            self._subtrees[i].update_rectangles((x2, y2, width2, height2))

    def get_rectangles(self) -> List[Tuple[Tuple[int, int, int, int],
                                           Tuple[int, int, int]]]:
        """Return a list with tuples for every leaf in the displayed-tree
        rooted at this tree. Each tuple consists of a tuple that defines the
        appropriate pygame rectangle to display for a leaf, and the colour
        to fill it with.
        """
        if self._subtrees == []:
            if self._expanded:
                return [(self.rect, self._colour)]
            else:
                return []
        lst = []
        for subtree in self._subtrees:
            lst.extend(subtree.get_rectangles())
        if lst == [] and self._expanded:
            lst.extend([(self.rect, self._colour)])
        return lst

    def _get_subtrees(self) -> List[TMTree]:
        lst = []
        for subtree in self._subtrees:
            if subtree._subtrees == []:
                lst.append(subtree)
            else:
                lst.extend(subtree._get_subtrees())
        return lst

    def get_tree_at_position(self, pos: Tuple[int, int]) -> Optional[TMTree]:
        """Return the leaf in the displayed-tree rooted at this tree whose
        rectangle contains position <pos>, or None if <pos> is outside of this
        tree's rectangle.

        If <pos> is on the shared edge between two rectangles, return the
        tree represented by the rectangle that is closer to the origin.

        the docstring states to break ties by choosing the rectangle
        “closer to the origin”. This is inaccurate, and more complicated than
        what we intended. Instead, ties should be broken by choosing the
        rectangle on the left for a vertical boundary, or the rectangle above
        for a horizontal boundary.
        """
        x, y, width, height = self.rect
        if not ((x <= pos[0] <= x + width) and (y) <= pos[1] <= y + height) or \
                not self._expanded:
            return None
        lst = []
        if self._subtrees == []:
            lst.append(self)
        for subtree in self._subtrees:
            lst.extend([subtree.get_tree_at_position(pos)])

        lst2 = lst.copy()
        for item in lst:
            if item is None:
                lst2.remove(item)
        lst = lst2

        if len(lst) == 1:
            return lst[0]
        elif len(lst) > 1:
            return _the_one(lst)
        if len(self.get_rectangles()) == 1:
            return self
        return None

    def update_data_sizes(self) -> int:
        """Update the data_size for this tree and its subtrees, based on the
        size of their leaves, and return the new size.

        If this tree is a leaf, return its size unchanged.
        """
        if self._subtrees == []:
            return self.data_size

        size = 0
        for subtree in self._subtrees:
            size += subtree.update_data_sizes()
        self.data_size = size
        return size

    def move(self, destination: TMTree) -> None:
        """If this tree is a leaf, and <destination> is not a leaf, move this
        tree to be the last subtree of <destination>. Otherwise, do nothing.
        """
        if self._subtrees == [] and destination._subtrees != []:
            self._parent_tree.data_size -= self.data_size
            destination._subtrees.append(self)
            destination.data_size += self.data_size
            self._parent_tree._subtrees.remove(self)
            self._parent_tree = destination
            self._expanded = False

    def change_size(self, factor: float) -> None:
        """Change the value of this tree's data_size attribute by <factor>.

        Always round up the amount to change, so that it's an int, and
        some change is made.

        Do nothing if this tree is not a leaf.
        """
        is_neg = factor < 0
        if is_neg:
            factor = abs(factor)
        if self._subtrees == []:
            the_factor = math.ceil(self.data_size*factor)
            if is_neg:
                the_factor = -(the_factor)
            self.data_size += the_factor

    def _get_top(self) -> TMTree:
        """Return the root of a tree"""
        if self._parent_tree is None:
            return self
        return self._parent_tree._get_top()

    def expand(self) -> None:
        """Update attribute _expanded of internal node to True"""
        self._expanded = True
        for subtree in self._subtrees:
            subtree._expanded = True

    def expand_all(self) -> None:
        """Update the entire displayed-tree rooted such that it is entirely
        expanded."""
        self._expanded = True
        # self.expand()
        for subtree in self._subtrees:
            subtree.expand_all()

    def collapse(self) -> None:
        """Update attribute _expanded to False"""
        if self._parent_tree is None:
            return
        self._parent_tree._unexpand()
        self._parent_tree._expanded = True

    def _unexpand(self) -> None:
        self._expanded = False
        for subtree in self._subtrees:
            subtree._unexpand()

    def collapse_all(self) -> None:
        """Update every attribute _expanded in displayed-tree rooted to False
        so that its collapsed up and to the root"""
        if self._parent_tree is None:
            return

        node = self._get_top()
        node._subtrees[0].collapse()

    # Methods for the string representation
    def get_path_string(self, final_node: bool = True) -> str:
        """Return a string representing the path containing this tree
        and its ancestors, using the separator for this tree between each
        tree's name. If <final_node>, then add the suffix for the tree.
        """
        if self._parent_tree is None:
            path_str = self._name
            if final_node:
                path_str += self.get_suffix()
            return path_str
        else:
            path_str = (self._parent_tree.get_path_string(False) +
                        self.get_separator() + self._name)
            if final_node or len(self._subtrees) == 0:
                path_str += self.get_suffix()
            return path_str

    def get_separator(self) -> str:
        """Return the string used to separate names in the string
        representation of a path from the tree root to this tree.
        """
        raise NotImplementedError

    def get_suffix(self) -> str:
        """Return the string used at the end of the string representation of
        a path from the tree root to this tree.
        """
        raise NotImplementedError

    def _get_subnode_by_name(self, name: str) -> TMTree:
        for subtree in self._subtrees:
            if subtree._name == name:
                return subtree
        return None

    def _append_subnode(self, node: TMTree) -> None:
        self._subtrees.extend([node])


def _the_one(lst: List) -> TMTree:
    """
    This method is used for breaking ties for get_tree_at_position

    :param lst: The list of rectangles that have the same pos(x,y)
    :return: The TMTree that will break the tie
    """
    if lst[0].rect[0] + lst[0].rect[2] == lst[1].rect[0]:
        return lst[0]
    elif lst[0].rect[0] == lst[1].rect[0] + lst[1].rect[2]:
        return lst[1]
    elif lst[0].rect[1] + lst[0].rect[3] == lst[1].rect[1]:
        return lst[0]
    else:
        return lst[1]

class FileSystemTree(TMTree):
    """A tree representation of files and folders in a file system.

    The internal nodes represent folders, and the leaves represent regular
    files (e.g., PDF documents, movie files, Python source code files, etc.).

    The _name attribute stores the *name* of the folder or file, not its full
    path. E.g., store 'assignments', not '/Users/Diane/csc148/assignments'

    The data_size attribute for regular files is simply the size of the file,
    as reported by os.path.getsize.
    """

    def __init__(self, path: str) -> None:
        """Store the file tree structure contained in the given file or folder.

        Precondition: <path> is a valid path for this computer.
        """
        TMTree.__init__(self, os.path.basename(path), [], 0)
        self._name = os.path.basename(path)
        if os.path.isdir(path):
            self._subtrees = self._build_children(path)
            sums = 0
            for subtree in self._subtrees:
                sums += subtree.data_size
            self.data_size = sums
        else:
            self._subtrees = []
            self.data_size = os.path.getsize(path)

        self._parent_tree = None

        if self._parent_tree is None:
            self._expanded = True
        else:
            self._expanded = False

    def _build_children(self, path: str) -> List:
        """
        This methods builds the subtrees and then adds the parent
        :param path: the file path
        :return: a list of TMTrees
        """
        lst = []
        for filename in os.listdir(path):
            subitem = os.path.join(path, filename)
            thing = FileSystemTree(subitem)
            thing._parent_tree = self
            lst.append(thing)
            if thing._parent_tree is None:
                thing._expanded = True
            else:
                thing._expanded = False
        return lst

    def get_separator(self) -> str:
        """Return the file separator for this OS.
        """
        return os.sep

    def get_suffix(self) -> str:
        """Return the final descriptor of this tree.
        """
        if len(self._subtrees) == 0:
            return ' (file)'
        else:
            return ' (folder)'


if __name__ == '__main__':
