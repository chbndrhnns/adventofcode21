from pathlib import Path


def find_naive_increases_count(data):
    items_processed = 0
    increases_count = 0
    for idx, item in enumerate(data):
        items_processed += 1
        next_idx = idx + 1
        try:
            next_item = data[next_idx]
            if next_item > item:
                increases_count += 1
        except IndexError:
            pass
    print(f"Items processed: {items_processed}")
    return increases_count


if __name__ == "__main__":
    with open(Path(__file__).parent / "data.txt", "r") as f:
        data = [num for num in f.readlines()]
        print(find_naive_increases_count([int(item.strip()) for item in data]))
