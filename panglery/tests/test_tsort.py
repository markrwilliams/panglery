import unittest
from panglery.tsort import tsort

class TestTSort(unittest.TestCase):
    def test_proper_ordering(self):
        # taken from tsort(1) info page
        acyclic = [{'file_lines': ['dump_remainder'],
                 'main': ['parse_options', 'tail_file', 'tail_forever'],
                 'recheck': ['pretty_name'],
                 'tail': ['tail_lines', 'tail_bytes'],
                 'tail_bytes': ['xlseek', 'start_bytes', 'dump_remainder', 'pipe_bytes'],
                 'tail_file': ['pretty_name', 'write_header', 'tail'],
                 'tail_forever': ['recheck', 'pretty_name', 'write_header', 'dump_remainder'],
                 'tail_lines': ['start_lines', 'dump_remainder', 'file_lines', 'pipe_lines']},
                  # taken from the topological sort wikipedia page
                  {7: [11, 8],
                   5: [11],
                   3: [8, 10],
                   11: [2, 9, 10],
                   8: [9]}]

        for graph in acyclic:
            result = tsort(graph)
            for i, n in enumerate(result):
                for to in graph.get(n, ()):
                    self.assert_(to in result)
                    self.assert_(result.index(to) > i)

    def test_fail_on_no_root_nodes(self):
        top_level_cyclic = {'a': ['b', 'c'], 'b': ['d'], 'c': ['a']}
        self.assertRaises(ValueError, tsort, top_level_cyclic)

    def test_succeed_on_lower_cycles(self):
        lower_level_cyclic = {'a': ['b'], 'b': ['c'], 'c': ['b']}
        self.assert_(tsort(lower_level_cyclic) == ['a', 'b', 'c'])
