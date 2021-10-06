import time
import pandas as pd


def count_connections2(list1: list, list2: list) -> int:
    df1 = pd.DataFrame(list1)[0].value_counts()
    df2 = pd.DataFrame(list2)[0].value_counts()
    df3 = pd.concat([df1, df2], axis=1, join='inner')
    df3.columns = [1, 2]
    df3['sum'] = df3[1] * df3[2]
    count = int(df3['sum'].sum())

    return count


def count_connections1(list1: list, list2: list) -> int:
    count = 0

    for i in list1:
        for j in list2:
            if i == j:
                count += 1

    return count


if __name__ == '__main__':
    list1 = [i for i in range(5000, 25000)]
    # for i in range(5000, 15000):
    #     list1.append(i)
    list2 = [i for i in range(4000, 20000)]
    # for i in range(5000, 14000):
    #     list2.append(i)
    print('Lists was created')
    start_time = time.time()
    q = count_connections1(list1, list2)
    print(f'execution time for 1 is {time.time() - start_time} seconds')
    print(f'value is {q}')
    start_time = time.time()
    q = count_connections2(list1, list2)
    print(f'execution time for 2 is {time.time() - start_time} seconds')
    print(f'value is {q}')

