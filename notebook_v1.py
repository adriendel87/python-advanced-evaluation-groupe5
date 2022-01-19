#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
an object-oriented version of the notebook toolbox
"""

class CodeCell:
    def __init__(self, ipynb):
        self.id = ipynb['id']
        self.source = ipynb['source']
        self.execution_count = ipynb['execution_count']
    
    """A Cell of Python code in a Jupyter notebook.

    Args:
        ipynb (dict): a dictionary representing the cell in a Jupyter Notebook.

    Attributes:
        id (int): the cell's id.
        source (list): the cell's source code, as a list of str.
        execution_count (int): number of times the cell has been executed.

    Usage:

        >>> code_cell = CodeCell({
        ...     "cell_type": "code",
        ...     "execution_count": 1,
        ...     "id": "b777420a",
        ...     'source': ['print("Hello world!")']
        ... })
        >>> code_cell.id
        'b777420a'
        >>> code_cell.execution_count
        1
        >>> code_cell.source
        ['print("Hello world!")']
    """

    

class MarkdownCell:
    def __init__(self, ipynb):
        self.id = ipynb['id']
        self.source = ipynb['source']

    
    """A Cell of Markdown markup in a Jupyter notebook.

    Args:
        ipynb (dict): a dictionary representing the cell in a Jupyter Notebook.

    Attributes:
        id (int): the cell's id.
        source (list): the cell's source code, as a list of str.

    Usage:

        >>> markdown_cell = MarkdownCell({
        ...    "cell_type": "markdown",
        ...    "id": "a9541506",
        ...    "source": [
        ...        "Hello world!\n",
        ...        "============\n",
        ...        "Print `Hello world!`:"
        ...    ]
        ... })
        >>> markdown_cell.id
        'a9541506'
        >>> markdown_cell.source
        ['Hello world!\n', '============\n', 'Print `Hello world!`:']
    """

    def __init__(self, ipynb):
        pass

class Notebook:
    def __init__(self, ipynb):
        self.version = str(ipynb['nbformat']) + '.' + str(ipynb['nbformat_minor'])
        self.cells = []
        for cell in ipynb['cells']:
            if cell['cell_type'] == 'markdown':
                self.cells.append(MarkdownCell(cell))
            elif cell['cell_type'] == 'code':
                self.cells.append(CodeCell(cell))
    
    """A Jupyter Notebook.

    Args:
        ipynb (dict): a dictionary representing a Jupyter Notebook.

    Attributes:
        version (str): the version of the notebook format.
        cells (list): a list of cells (either CodeCell or MarkdownCell).

    Usage:

        - checking the verion number:

            >>> ipynb = toolbox.load_ipynb("samples/minimal.ipynb")
            >>> nb = Notebook(ipynb)
            >>> nb.version
            '4.5'

        - checking the type of the notebook parts:

            >>> ipynb = toolbox.load_ipynb("samples/hello-world.ipynb")
            >>> nb = Notebook(ipynb)
            >>> isinstance(nb.cells, list)
            True
            >>> isinstance(nb.cells[0], Cell)
            True
    """


    @staticmethod
    def from_file(filename):
        from notebook_v0 import load_ipynb
        return Notebook(load_ipynb(filename))
        
        """Loads a notebook from an .ipynb file.

        Usage:

            >>> nb = Notebook.from_file("samples/minimal.ipynb")
            >>> nb.version
            '4.5'
        """
        pass

    def __iter__(self):
        r"""Iterate the cells of the notebook.

        Usage:

            >>> nb = Notebook.from_file("samples/hello-world.ipynb")
            >>> for cell in nb:
            ...     print(cell.id)
            a9541506
            b777420a
            a23ab5ac
        """
        return iter(self.cells)

class PyPercentSerializer:
    r"""Prints a given Notebook in py-percent format.

    Args:
        notebook (Notebook): the notebook to print.

    Usage:
            >>> nb = Notebook.from_file("samples/hello-world.ipynb")
            >>> ppp = PyPercentSerializer(nb)
            >>> print(ppp.to_py_percent()) # doctest: +NORMALIZE_WHITESPACE
            # %% [markdown]
            # Hello world!
            # ============
            # Print `Hello world!`:
            <BLANKLINE>
            # %%
            print("Hello world!")
            <BLANKLINE>
            # %% [markdown]
            # Goodbye! 👋
    """
    def __init__(self, notebook):
        pass

    def to_py_percent(self):
        r"""Converts the notebook to a string in py-percent format.
        """
        pass

    def to_file(self, filename):
        r"""Serializes the notebook to a file

        Args:
            filename (str): the name of the file to write to.

        Usage:

                >>> nb = Notebook.from_file("samples/hello-world.ipynb")
                >>> s = PyPercentSerializer(nb)
                >>> s.to_file("samples/hello-world-serialized-py-percent.py")
        """
        pass
class Serializer:
    def __init__(self, notebook):
        self.notebook = notebook
    
    """Serializes a Jupyter Notebook to a file.

    Args:
        notebook (Notebook): the notebook to print.

    Usage:

        >>> nb = Notebook.from_file("samples/hello-world.ipynb")
        >>> s = Serializer(nb)
        >>> pprint.pprint(s.serialize())  # doctest: +NORMALIZE_WHITESPACE
            {'cells': [{'cell_type': 'markdown',
                'id': 'a9541506',
                'medatada': {},
                'source': ['Hello world!\n',
                           '============\n',
                           'Print `Hello world!`:']},
               {'cell_type': 'code',
                'execution_count': 1,
                'id': 'b777420a',
                'medatada': {},
                'outputs': [],
                'source': ['print("Hello world!")']},
               {'cell_type': 'markdown',
                'id': 'a23ab5ac',
                'medatada': {},
                'source': ['Goodbye! 👋']}],
            'metadata': {},
            'nbformat': 4,
            'nbformat_minor': 5}
        >>> s.to_file("samples/hello-world-serialized.ipynb")
    """

    def serialize(self):
        nb = self.notebook
        dic = {}
        dic['cells'] = []
        for cell in nb.cells:
            ce = {}
            if isinstance(cell, MarkdownCell):
                ce['cell_type'] = 'markdown'
            elif isinstance(cell, CodeCell):
                ce['cell_type'] = 'code'
                ce['execution_count'] = cell.execution_count
            ce['id'] = cell.id
            ce['metadata'] = {}
            if isinstance(cell, CodeCell):
                ce['outputs'] = []
            ce['source'] = cell.source
            dic['cells'].append(ce)
        dic['metadata'] = {}
        dic['nbformat'] = int(nb.version[0])
        dic['nbformat_minor'] = int(nb.version[2])
        return dic

        """Serializes the notebook to a JSON object

        Returns:
            dict: a dictionary representing the notebook.
        """
        pass

    def to_file(self, filename):
        from notebook_v0 import save_ipynb
        return save.ipynb(self, filename)
        
        """Serializes the notebook to a file

        Args:
            filename (str): the name of the file to write to.

        Usage:

                >>> nb = Notebook.from_file("samples/hello-world.ipynb")
                >>> s = Serializer(nb)
                >>> s.to_file("samples/hello-world-serialized.ipynb")
                >>> nb = Notebook.from_file("samples/hello-world-serialized.ipynb")
                >>> for cell in nb:
                ...     print(cell.id)
                a9541506
                b777420a
                a23ab5ac
        """
        pass

class Outliner:
    r"""Quickly outlines the strucure of the notebook in a readable format.

    Args:
        notebook (Notebook): the notebook to outline.

    Usage:

            >>> nb = Notebook.from_file("samples/hello-world.ipynb")
            >>> o = Outliner(nb)
            >>> print(o.outline()) # doctest: +NORMALIZE_WHITESPACE
                Jupyter Notebook v4.5
                └─▶ Markdown cell #a9541506
                    ┌  Hello world!
                    │  ============
                    └  Print `Hello world!`:
                └─▶ Code cell #b777420a (1)
                    | print("Hello world!")
                └─▶ Markdown cell #a23ab5ac
                    | Goodbye! 👋
    """
    def __init__(self, notebook):
        self.notebook = notebook

    def outline(self):
        nb = self.notebook
        title = f"Jupyter Notebook v{nb.version}\n"
        body = ''
        for cell in nb:
            if isinstance(cell, CodeCell):
                ce = f"└─▶ Code cell #{cell.id} ({cell.execution_count})\n"
            elif isinstance(cell, MarkdownCell):
                ce = f"└─▶ Markdown cell #{cell.id}\n"
            if len(cell.source) == 1:
                ce += "    | " + cell.source[0] + '\n'
            else:
                for count, line in enumerate(cell.source):
                    if count == 0:
                        ce += '    ┌  ' + line
                    elif count == len(cell.source) - 1:
                        ce += '    └  ' + line + '\n'
                    else: 
                        ce += '    │  ' + line
            body += ce
        return title + body
        
        """Outlines the notebook in a readable format.

        Returns:
            str: a string representing the outline of the notebook.
        """
        
