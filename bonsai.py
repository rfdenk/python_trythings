import unittest

def can_merge(list1, list2):
    for n1 in range(0, len(list1)):
        for n2 in range(0, len(list2)):
            if list2[n2] == list1[n1]:
                return True
    return False


def do_merge(list1, list2):
    new_list = list1[:]
    for nt in range(0, len(list2)):
        if list2[nt] not in new_list:
            new_list.append(list2[nt])
    return new_list


def build_lol(list1, list2):
    new_list = [list1]
    for n2 in range(0, len(list2)):
        new_list.append(list2[n2])
    return new_list


def merge2(list_of_lists):
    new_head = list_of_lists[0]
    tail = list_of_lists[1:]
    new_tail = []
    for nt in range(0, len(tail)):
        if can_merge(new_head, tail[nt]):
            new_head = do_merge(new_head, tail[nt])
        else:
            new_tail.append(tail[nt])
    new_list = build_lol(new_head, new_tail)
    return new_list


def merge(list_of_lists):
    if len(list_of_lists) == 0:
        return []

    if len(list_of_lists) == 1:
        return [list_of_lists[0]]

    lol = list_of_lists[:]
    keep_merging = True
    while keep_merging:
        original_len = len(lol)
        lol = merge2(lol)
        if len(lol) == original_len:
            keep_merging = False        # no merges occurred

    new_tail = merge(lol[1:])
    return build_lol(lol[0], new_tail)


class TestBonsai(unittest.TestCase):

    def testCanMerge(self):
        cm1 = can_merge(['a', 'b', 'c'], ['a', 'h'])
        self.assertTrue(cm1)
        cm2 = can_merge(['a', 'b', 'c'], ['d', 'e'])
        self.assertFalse(cm2)

    def testDoMerge(self):
        m1 = do_merge(['a', 'b', 'c'], ['a', 'h'])
        self.assertEqual(m1,['a', 'b', 'c', 'h'])

    def testBuildLOL(self):
        cat1 = build_lol(['a', 'b', 'c'], [['d', 'e', 'f']])
        self.assertEqual(cat1,[['a', 'b', 'c'], ['d','e','f']])

    merge_tests =[
        {"test":[['a', 'b', 'c'], ['d', 'e'], ['a', 'h']],"expected":[['a','b','c','h'],['d','e']]},
        {"test":[['a', 'b', 'c'], ['d', 'e'], ['a', 'd']],"expected":[['a','b','c','d','e']]},
        {"test":[['a', 'b', 'c'], ['d', 'e'], ['f', 'g']],"expected":[['a', 'b', 'c'], ['d', 'e'], ['f', 'g']]},
        {"test":[['d', 'e'], ['a', 'h'], ['a', 'b', 'c'], ],"expected":[['d','e'],['a','h','b','c']]},
        {"test":[['a', 'd'], ['a', 'b', 'c'], ['d', 'e'], ],"expected":[['a','d','b','c','e']]},
    ]

    def testMerges(self):
        for nM in range(0, len(TestBonsai.merge_tests)):
            lol = TestBonsai.merge_tests[nM]["test"]
            lolM = merge(lol)
            print(lol, "-->", lolM, flush=True)
            self.assertEqual(lolM, TestBonsai.merge_tests[nM]["expected"])


if __name__ == "__main__":
    unittest.main()
