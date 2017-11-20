import unittest


def move_blocks_dir(blocks, direction):
    directions = ["L", "R"]
    if len(blocks) == 0:
        return []
    elif len(blocks) == 1:
        return [blocks[0] + directions[direction]]
    else:
        moves = [] + \
            move_blocks_dir(blocks[1:], 1-direction) + \
            move_blocks_dir(blocks[0:1], direction) + \
            move_blocks_dir(blocks[1:], 1-direction)
        return moves


def move(num_blocks):
    blocks = []
    for n in range(num_blocks, 0, -1):
        blocks.append(str(n))
    return move_blocks_dir(blocks, 0)


def swap_l_and_r(moves):
    swapped = []
    for m in range(0, len(moves)):
        new_move = moves[m].replace('L', '_').replace('R', 'L').replace('_', 'R')
        swapped.append(new_move)
    return swapped


def execute_moves(num_blocks, moves):
    pillars = []
    blocks = []
    for n in range(num_blocks, 0, -1):
        blocks.append(str(n))
    pillars.append(blocks)
    pillars.append([])
    pillars.append([])

    for m in range(0, len(moves)):
        block_to_move = moves[m][0:-1]
        dir_to_move = moves[m][-1]
        for p in range(0, 3):
            if len(pillars[p]) > 0 and pillars[p][-1] == block_to_move:
                pillars[p] = pillars[p][0:-1]
                if dir_to_move == "L":
                    target = p - 1
                    if target < 0:
                        target = 2
                else:
                    target = p + 1
                    if target > 2:
                        target = 0
                pillars[target] += [block_to_move]
                break
    return pillars


class TestHanoi(unittest.TestCase):

    def testSwap(self):
        s = swap_l_and_r(["1L", "2R", "1L"])
        self.assertEqual(s, ["1R", "2L", "1R"])

    def testAll(self):
        for b in range(1, 12):
            moves = move(b)
            print(moves)
            print(len(moves))
            expected = [] + swap_l_and_r(move(b-1)) + [str(b) + "L"] + swap_l_and_r(move(b - 1))
            self.assertEqual(moves, expected)
            self.assertEqual(len(moves), (1 << b) - 1)
            result = execute_moves(b, moves)
            self.assertEqual(len(result[0]), 0)
            self.assertEqual(len(result[1]), 0)
            self.assertEqual(len(result[2]), b)
            print(result)
            for tb in range(0, b):
                self.assertEqual(result[2][tb], str(b-tb))


if __name__ == "__main__":
    unittest.main()
