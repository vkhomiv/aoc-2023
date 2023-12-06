import re
import datetime


class MapEntry:
    source: range
    destination: range

    def __init__(self, str_value):
        str_destination, str_source, str_length = str_value.split()
        length = int(str_length)
        destination = int(str_destination)
        source = int(str_source)
        self.source = range(source, source + length)
        self.destination = range(destination, destination + length)

    def map_destination_range(self, input_range: range) -> (range, range, range):
        prefix_range = None
        postfix_range = None

        if input_range.stop < self.source.start or input_range.start > self.source.stop:
            return None, None, input_range

        overlapped_start = max(input_range.start, self.source.start)
        overlapped_stop = min(input_range.stop, self.source.stop)
        if input_range.start < overlapped_start:
            prefix_range = range(input_range.start, overlapped_start)

        if input_range.stop > overlapped_stop:
            postfix_range = range(overlapped_stop, input_range.stop)

        mapped_range = range(self.destination.start + (overlapped_start - self.source.start),
                             self.destination.start + (overlapped_stop - self.source.start))

        return prefix_range, mapped_range, postfix_range

    def __repr__(self):
        return f"source:{self.source} dest:{self.destination}"


def setup():
    file = open("maps_input.txt", "r")
    data = file.read()
    file.close()
    return data


def get_destination_ranges(input_ranges: list[range], mappings: list[MapEntry]):
    remained_ranges = []
    mapped_ranges = []
    for input_range in input_ranges:
        current_range = input_range
        postfix_range = None
        mapping_iter = iter(mappings)
        while mapping := next(mapping_iter, None):
            prefix_range, mapped, postfix_range = mapping.map_destination_range(current_range)
            if prefix_range:
                remained_ranges.append(prefix_range)
            if mapped:
                mapped_ranges.append(mapped)
                if postfix_range:
                    current_range = postfix_range
                else:
                    break
        if postfix_range:
            remained_ranges.append(current_range)
    return sorted(remained_ranges + mapped_ranges, key=lambda x: x.start)


def parse_mapping(pattern, raw_input) -> list[MapEntry]:
    part = re.search(pattern, raw_input, re.S).group(1)
    mappings = [MapEntry(str_value) for str_value in part.splitlines() if str_value != ""]
    return sorted(mappings, key=lambda x: x.source.start)


def get_extended_seeds(seeds_config: list[int]):
    pool = []
    seeds_iter = iter(seeds_config)
    for seed in seeds_iter:
        range_length = next(seeds_iter)
        pool.append(range(seed, seed + range_length))
    return pool


if __name__ == '__main__':
    start = datetime.datetime.now()

    map_input = setup()
    seeds_strings = re.search(r"seeds:(.*)\n", map_input).group(1).split()

    seed_to_soil = parse_mapping(r"seed-to-soil map:(.*)soil", map_input)
    soil_to_fertilizer = parse_mapping(r"soil-to-fertilizer map:(.*)fertilizer", map_input)
    fertilizer_to_water = parse_mapping(r"fertilizer-to-water map:(.*)water", map_input)
    water_to_light = parse_mapping(r"water-to-light map:(.*)light", map_input)
    light_to_temperature = parse_mapping(r"light-to-temperature map:(.*)temperature", map_input)
    temperature_to_humidity = parse_mapping(r"temperature-to-humidity map:(.*)humidity", map_input)
    humidity_to_location = parse_mapping(r"humidity-to-location map:(.*)$", map_input)

    seeds = [int(seed) for seed in seeds_strings]
    extended_seeds = get_extended_seeds(seeds)
    min_location = None

    for seed_range in extended_seeds:
        soil_ranges = get_destination_ranges([seed_range], seed_to_soil)
        fertilizer_ranges = get_destination_ranges(soil_ranges, soil_to_fertilizer)
        water_ranges = get_destination_ranges(fertilizer_ranges, fertilizer_to_water)
        light_ranges = get_destination_ranges(water_ranges, water_to_light)
        temperature_ranges = get_destination_ranges(light_ranges, light_to_temperature)
        humidity_ranges = get_destination_ranges(temperature_ranges, temperature_to_humidity)
        location_ranges = get_destination_ranges(humidity_ranges, humidity_to_location)
        current_min_location = location_ranges[0].start
        if not min_location or current_min_location < min_location:
            min_location = current_min_location
    end = datetime.datetime.now()

    print(min_location, end - start)
