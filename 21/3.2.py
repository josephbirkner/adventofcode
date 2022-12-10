
initial_numbers = []
with open("03.data", 'r') as f:
    for line in f:
        l = line.strip()
        if l:
            assert not initial_numbers or len(initial_numbers[-1]) == len(l)
            initial_numbers.append(l)


def search_value(list_sel_fun, binary_numbers, pos=0) -> str:
    number_lists_per_bit_val = [[], []]
    for num in binary_numbers:
        number_lists_per_bit_val[int(num[pos])].append(num)
    new_binary_number_list = list_sel_fun(number_lists_per_bit_val)
    assert len(new_binary_number_list) == 1 or pos+1 < len(binary_numbers[0])
    if len(new_binary_number_list) == 1:
        return new_binary_number_list[0]
    return search_value(list_sel_fun, new_binary_number_list, pos+1)


def list_sel_max_len(lists, invert=False, fallback=1):
    if len(lists[0]) > len(lists[1]):
        if invert:
            lists.reverse()
        return lists[0]
    elif len(lists[1]) > len(lists[0]):
        if invert:
            lists.reverse()
        return lists[1]
    else:
        return lists[fallback]


oxy = search_value(lambda lists: list_sel_max_len(lists, invert=False, fallback=1), initial_numbers)
co2 = search_value(lambda lists: list_sel_max_len(lists, invert=True, fallback=0), initial_numbers)

print(f"oxy     : {oxy} ({int(oxy, 2)})")
print(f"co2     : {co2} ({int(co2, 2)})")
print(f"product : {int(oxy, 2)*int(co2, 2)}")
