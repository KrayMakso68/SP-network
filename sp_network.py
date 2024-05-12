# input_x: int = int(input('Введите входное число в битовом формате: ').strip(), 2)
# key: int = int(input('Введите ключ в битовом формате: ').strip(), 2)
# s_box: [int] = list(map(int, input('Введите s-блок через пробел: ').split()))


def number_to_byte_str(num, fill=9) -> str:
    return "{0:b}".format(num).zfill(fill)


def byte_str_to_number(string):
    return int(string, 2)


def byte_concat_to_int(byte_arr) -> int:
    return int(''.join(map(str, byte_arr)), 2)


# __________________________________________________

def sum_key(input_num: int, key: int) -> int:
    return input_num ^ key


def s_box_step(input_num: int, s_block: [int]) -> int:
    array = list(map(int, number_to_byte_str(input_num, fill=9)))
    pos = 0
    while pos < len(array):
        input_s_block = byte_concat_to_int(array[pos:pos + 3])
        out_block = number_to_byte_str(s_block[input_s_block], fill=3)
        for el in out_block:
            array[pos] = int(el)
            pos += 1
    return byte_concat_to_int(array)


def byte_arr_swap(input_num: int) -> int:
    array = list(map(int, number_to_byte_str(input_num, fill=9)))
    array[1], array[3] = array[3], array[1]
    array[2], array[6] = array[6], array[2]
    array[5], array[7] = array[7], array[5]
    return byte_concat_to_int(array)


def inv_s_box(input_s_box):
    out = [0] * 8
    for i in range(len(input_s_box)):
        out[input_s_box[i]] = i
    return out


def encode(input_num: int, key: int, input_s_box: [int]) -> int:
    full_round_count = 2
    out = input_num
    for _ in range(full_round_count):
        out = byte_arr_swap(s_box_step(sum_key(out, key), input_s_box))
    out = sum_key(s_box_step(sum_key(out, key), input_s_box), key)
    return out


def decode(input_num: int, key: int, inv_s_box: [int]) -> int:
    full_round_count = 2
    out = sum_key(s_box_step(sum_key(input_num, key), inv_s_box), key)
    for i in range(full_round_count):
        out = sum_key(s_box_step(byte_arr_swap(out), inv_s_box), key)
    return out


# __________________________________________________

# out1 = encode(input_x, key, s_box)
# print('Encoded number: ', number_to_byte_str(out1))
#
# out2 = decode(out1, key, inv_s_box(s_box))
# print('Decoded number: ', number_to_byte_str(out2))