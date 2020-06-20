def fizzbuzz(n: int) -> str:
    """
    Outputs 'fizz', if the input is dividable by 5.
    Outputs 'buzz', if the input is dividable by 7.
    Outputs 'fizzbuzz', if the input is dividable by 5 and 7.

    Example:
        >>> fizzbuzz(35)
        'fizzbuzz'
        >>> fizzbuzz(36)
        ''

    :param n: Positive integer
    :return: String 'fizz', 'buzz', 'fizzbuzz' oder empty string
    """
    if type(n) != int:
        raise TypeError(f'int expected as input, got {type(n)}')
    if n < 0:
        raise ValueError(f'Positive input expected')
    return f"{'fizz' if n % 5 == 0 else ''}{'buzz' if n % 7 == 0 else ''}"
