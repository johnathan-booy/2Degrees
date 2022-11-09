def divide_list(l: list, n: int) -> list:
    """Divide a long list into multiple lists of a given length"""
    new_list = [l[i:i + n] for i in range(0, len(l), n)]
    return new_list
