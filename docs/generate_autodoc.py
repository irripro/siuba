import ast
from ast import NodeVisitor

HEADER_TEMPLATE = """
.. THIS DOCUMENT IS AUTOGENERATED

{module}
-------------------------------------------------------------------------------
"""

FUNC_TEMPLATE = """
{func_name}
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. autofunction:: {module}.{func_name}
"""

class GimmeThoseHeaders(NodeVisitor):
    def __init__(self):
        self.out = []
        
    def visit_FunctionDef(self, node):
        if node.name.startswith("_"):
            return
        
        self.out.append(node.name)


if __name__ == "__main__":
    import sys
    from pathlib import Path
    lib_path, in_file = sys.argv[1:3]

    pyfile = open(Path(lib_path) / in_file, 'r').read()

    gth = GimmeThoseHeaders()
    gth.visit(ast.parse(pyfile))

    module = in_file.replace('/', '.').replace('.py', '')
    
    sections = []
    for name in gth.out:
        section = FUNC_TEMPLATE.format(func_name = name, module = module)
        sections.append(section)

    page = HEADER_TEMPLATE.format(module = module) + "\n\n".join(sections)
    print(page)
    
