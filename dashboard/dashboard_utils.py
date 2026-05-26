from collections import Counter


def count_items(df, column):

    counter = Counter()

    for values in df[column]:

        if not values:
            continue

        for item in values:
            counter[item] += 1

    return counter