from pathlib import Path


def find_naive_increases_count(data):
    increases_count = 0
    for idx, item in enumerate(data):
        next_idx = idx + 1
        try:
            next_item = data[next_idx]
            if next_item > item:
                increases_count += 1
        except IndexError:
            pass
    return increases_count


def find_sliding_window_increases_count(data, *, window_size=3):
    def _get_window_at(start: int):
        return data[start:start + window_size]

    if len(data) < window_size:
        return 0

    next_window_starts_at = 0
    current_window_sum = sum(_get_window_at(next_window_starts_at))
    next_window_starts_at += 1

    increases_count = 0
    while next_window := _get_window_at(next_window_starts_at):
        next_window_sum = sum(next_window)
        if next_window_sum > current_window_sum:
            increases_count += 1
        next_window_starts_at += 1
        current_window_sum = next_window_sum
    return increases_count


if __name__ == "__main__":
    with open(Path(__file__).parent / "data.txt", "r") as f:
        data = [num for num in f.readlines()]
        naive = find_naive_increases_count([int(item.strip()) for item in data])
        print(f"naive: {naive}")
        sliding_window = find_sliding_window_increases_count([int(item.strip()) for item in data])
        print(f"sliding window: {sliding_window}")
