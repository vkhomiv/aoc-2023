digits_map = {
    "one": "1", "two": "2", "three": "3", "four": "4", "five": "5", "six": "6", "seven": "7", "eight": "8", "nine": "9"
}


def get_spelled_digit(calibration_value):
    for spelled_digit in digits_map.keys():
        if calibration_value.startswith(spelled_digit):
            return digits_map[spelled_digit]
    return None


def fix_calibration_values():
    file = open('calibration_values.txt', 'r')
    calibration_values = file.readlines()

    accumulator = []
    for calibration_value in calibration_values:
        first_num_str = None
        last_num_str = None

        for idx, element in enumerate(calibration_value):
            if element.isdigit():
                if not first_num_str:
                    first_num_str = element
                last_num_str = element
            elif spelled_digit := get_spelled_digit(calibration_value[idx:]):
                if not first_num_str:
                    first_num_str = spelled_digit
                last_num_str = spelled_digit

        accumulator.append(int(first_num_str + last_num_str))
        print(calibration_value, first_num_str, last_num_str)

    print(sum(accumulator))


if __name__ == '__main__':
    fix_calibration_values()
