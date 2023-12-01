digits_map = {
    "one": "1", "two": "2", "three": "3", "four": "4", "five": "5", "six": "6", "seven": "7", "eight": "8", "nine": "9"
}


def get_spelled_digit(calibration_value):
    for spelled_digit in digits_map.keys():
        if calibration_value.startswith(spelled_digit):
            return digits_map[spelled_digit]
    return None


def get_that_digit(calibration_value):
    if len(calibration_value) < 1:
        return None
    first_element = calibration_value[0]
    return first_element if first_element.isdigit() else get_spelled_digit(calibration_value)


def fix_calibration_values():
    file = open('day1/calibration_values.txt', 'r')
    calibration_values = file.readlines()

    accumulator = []
    for calibration_value in calibration_values:
        first_num_str = None
        last_num_str = None

        for idx in range(len(calibration_value)):
            probably_digit = get_that_digit(calibration_value[idx:])
            if probably_digit:
                last_num_str = probably_digit
                if not first_num_str:
                    first_num_str = probably_digit

        accumulator.append(int(first_num_str + last_num_str))
        print(calibration_value, first_num_str, last_num_str)

    print(sum(accumulator))


if __name__ == '__main__':
    fix_calibration_values()
