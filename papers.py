import csv
from typing import List, Dict
from tm_trees import TMTree

# Filename for the dataset
DATA_FILE = 'cs1_papers.csv'


class PaperTree(TMTree):
    """A tree representation of Computer Science Education research paper data.

    === Private Attributes ===

    These should store information about this paper's <authors> and <doi>.

    === Inherited Attributes ===
    rect:
        The pygame rectangle representing this node in the treemap
        visualization.
    data_size:
        The size of the data represented by this tree.
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
    - All TMTree RIs are inherited.
    """

    authors: str
    doi: str
    citations: int

    def __init__(self, name: str, subtrees: List[TMTree], authors: str = '',
                 doi: str = '', citations: int = 0, by_year: bool = True,
                 all_papers: bool = False) -> None:
        """Initialize a new PaperTree with the given <name> and <subtrees>,
        <authors> and <doi>, and with <citations> as the size of the data.

        If <all_papers> is True, then this tree is to be the root of the paper
        tree. In that case, load data about papers from DATA_FILE to build the
        tree.

        If <all_papers> is False, Do NOT load new data.

        <by_year> indicates whether or not the first level of subtrees should be
        the years, followed by each category, subcategory, and so on. If
        <by_year> is False, then the year in the dataset is simply ignored.
        """

        TMTree.__init__(self, name, [], 0)
        self._parent_tree = None
        if all_papers:
            self._expanded = True
            self._load_papers_to_dict(by_year)
        else:
            self._expanded = False
            self.authors = authors
            self.doi = doi
            self.citations = citations


    def _load_papers_to_dict(self, by_year: bool = True) -> None:
        """Return a nested dictionary of the data read from the papers
         dataset file.

        If <by_year>, then use years as the roots of the subtrees of the root of
        the whole tree. Otherwise, ignore years and use categories only.
        """
        with open(DATA_FILE, mode='r') as csv_file:
            csv_reader = csv.DictReader(csv_file)

            for row in csv_reader:
                self._build_tree_from_dict(row, by_year)


    def get_separator(self) -> str:
        """Return the file separator for this OS.
        """
        return ":"

    def get_suffix(self) -> str:
        """Return the final descriptor of this tree.
        """
        if len(self._subtrees) == 0:
            return ' (Article)'
        else:
            return ' (Category)'

    def _build_tree_from_dict(self, row: Dict, by_year: bool) -> None:
        """Return a list of trees from the nested dictionary <nested_dict>.
        """
        category = row["Category"]
        categories = category.split(':')
        title = row["Title"]
        url = row["Url"]
        citation = int(row["Citations"])
        author = row["Author"]
        year = row["Year"]

        parent = self
        parent.data_size += citation
        if by_year:
            sub_node = self._build_sub_node([parent], year, citation)
            parent = sub_node[0]

        for item in categories:
            sub_node = self._build_sub_node([parent], item, citation)
            parent = sub_node[0]
        leaf = PaperTree(title, [], author, url, citation, False, False)
        leaf._parent_tree = parent
        leaf.data_size = citation
        parent._hacky([leaf])

    def _hacky(self, leaf: List) -> List:
        """
        This is one of 3 hacky type methods that builds leaves
        :param leaf: the leaf
        :return: a list of leaves
        """
        self._append_subnode(leaf[0])

    def _build_sub_node(self, parent2: List, name: str, citation: int) -> List:
        """
        This is for building the sub nodes of the trees
        :param parent2: a list of parents
        :param name: the name of the category
        :param citation: the citation
        :return: A list of PaperTrees
        """
        parent = parent2[0]
        sub_node2 = parent._hacky2(name)
        self._expanded = self._expanded
        if len(sub_node2) == 0:
            sub_node = None
        else:
            sub_node = sub_node2[0]

        if sub_node is None:
            sub_node = PaperTree(name, [], "", "", 0, False, False)
            sub_node._parent_tree = parent
            parent._hacky3([sub_node])
        sub_node.data_size += citation
        return [sub_node]

    def _hacky2(self, name: str) -> List:
        """
        This is the second of three methods that builds the tree
        :param name: This is the name of the category
        :return: A list of leaves
        """
        lst = []
        abc = self._get_subnode_by_name(name)
        lst.append(abc)
        return lst

    def _hacky3(self, sub_node: List) -> None:
        """
        This is the third of 3 methods that build the tree
        :param sub_node: a subnode that will be appended
        :return: Nothing
        """
        self._append_subnode(sub_node[0])



if __name__ == '__main__':
