def print_star_pyramid(num_lines: int) -> None:
    for i in range(1, num_lines):
        print(("*" * i + " " * num_lines + "*" * (num_lines - i)) * 10)


if __name__ == '__main__':
    print_star_pyramid(10)
