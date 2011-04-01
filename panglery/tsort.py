"""Basic topological sort implementation
"""

def tsort(graph):
    """Basic depth-first topological sort.
    
       * `graph` is a dictionary representing a DAG the direction of
         whose edges indicate reverse dependencies."""
    level = set(graph) - set(node for bunch in graph.itervalues()
                                 for node in bunch)
    stack = [(False, False)]     
    visited = set()
    edges = []

    while level:
        for node in level:
            if node not in visited:
                visited.add(node)
                if graph.get(node):
                    stack.append((level, node))
                    level = graph[node]
                    break
                edges.append(node)
        else:
            level, parent = stack.pop()
            edges.append(parent)

    edges.pop()                 # clean up our False parent
    edges.reverse()
    return edges

