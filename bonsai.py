
def can_merge(list1,list2):
    for n1 in range(0,len(list1)):
        for n2 in range(0,len(list2)):
            if list2[n2] == list1[n1]:
                return True
    return False


def do_merge(list1,list2):
    new_list = list1[:]
    for nt in range(0,len(list2)):
        if(list2[nt] not in new_list):
            new_list.append(list2[nt])
    return new_list


def merge2(list):
    new_head = list[0]
    tail = list[1:]
    new_tail = []
    for nt in range(0,len(tail)):
        if can_merge(new_head,tail[nt]):
            new_head = do_merge(new_head, tail[nt])
        else:
            new_tail.append(tail[nt])
    new_list = [new_head]
    new_list = new_list + new_tail
    return new_list


def merge(list_of_lists):
    if len(list_of_lists) == 0:
        return []

    if len(list_of_lists) == 1:
        return list_of_lists[0]

    lists = list_of_lists[:]
    keep_merging = True
    while keep_merging:
        original_len = len(lists)
        lists = merge2(lists)
        if(len(lists) == original_len):
            keep_merging = False        # no merges occurred

    new_list = [lists[0]]
    new_list.append(merge(lists[1:]))
    return lists



if __name__ == "__main__":
    cm1 = can_merge(['a','b','c'],['a','h'])
    cm2 = can_merge(['a','b','c'],['d','e'])

    m1 = do_merge(['a','b','c'],['a','h'])

    lol = [['a','b','c'],['d','e'],['a','h']]
    lol_merged = merge(lol)
    print(lol_merged)

    lol2 = [['a','b','c'],['d','e'],['a','d']]
    lol2_merged = merge(lol2)
    print(lol2_merged)

    lol3 = [['a','b','c'],['d','e'],['f','g']]
    lol3_merged = merge(lol3)
    print(lol3_merged)
