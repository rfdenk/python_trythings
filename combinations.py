

def combinations(k, n):
    # create the original list.
    c = []
    for i in range(0, k):
        c.append(i)
    all_combos = []

    while True:
        all_combos.append(list(c))  # gotta duplicate c!

        for i in range(0, k):
            print(str(c[i]), end='', flush=True)
        print("")

        for i in reversed(range(0, k)):
            if c[i] < n-(k-i):              # I can increment this one, and have room for the rest.
                c[i] += 1                   # do so!
                for j in range(i+1, k):
                    c[j] = c[j-1] + 1       # fill in the rest
                break
        else:                               # did not hit the "break", so we must be done.
            return all_combos


def combo_generator(k, n):
    c = []
    for i in range(0, k):
        c.append(i)

    while True:
        yield c
        for i in reversed(range(0, k)):
            if c[i] < n-(k-i):              # I can increment this one, and have room for the rest.
                c[i] += 1                   # do so!
                for j in range(i+1, k):
                    c[j] = c[j-1] + 1       # fill in the rest
                break
        else:                               # did not hit the "break", so we must be done.
            return

def factorial(n):
    acc = 1
    v = n;
    while v > 0:
        acc = acc * v
        v -= 1
    return acc

def count_combinations(k, n):
    return factorial(n) / (factorial(k) * factorial(n-k))


if __name__ == "__main__":
    combos = combinations(5, 7)
    expected = count_combinations(5, 7)
    print("There were " + str(len(combos)) + " combinations, and we expected " + str(int(expected)))

    num_duplicates = 0
    for s in range(0, len(combos)-1):
        for e in range(s+1, len(combos)):
            if combos[s] == combos[e]:
                num_duplicates += 1
                print(str(s) + " and " + str(e) + " are duplicates!")

    print("There are", str(num_duplicates), "duplicates")

    generated_combos = 0
    for c in combo_generator(5,7):
        generated_combos += 1
        print(str(c))

    print("There are " + str(generated_combos) + " generated combos")