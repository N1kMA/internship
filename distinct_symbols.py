def distinct_symbols(s):
    result = []
    now_list = []
    last_index = len(s) - 1
    for i in range(len(s)):
        if s[i] not in now_list:
            now_list.append(s[i])
            if i == last_index:
                result.append(len(now_list))
        else:
            result.append(len(now_list))
            now_list.clear()
            now_list.append(s[i])
            if i == last_index:
                result.append(len(now_list))
    result.sort()
    return result[len(result) - 1]

if __name__ == '__main__':
    e1 = distinct_symbols('abcabcbq')
    e2 = distinct_symbols('bbbbb')
    e3 = distinct_symbols('pwwkewee')