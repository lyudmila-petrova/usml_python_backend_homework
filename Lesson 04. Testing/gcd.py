def gcd(m: int, n: int) -> int:
    """
    Реализация бинарного алгоритма вычисления наибольшего общего делителя

    :param m:
    :param n:
    :return:
    """

    if not isinstance(m, int) or not isinstance(n, int):
        raise ValueError("GCD defined only for integer values")

    if m == 0 and n == 0:
        raise ValueError("GCD is not defined for N=M=0")

    m = abs(m)
    n = abs(n)

    if m == 0 and n != 0:
        return n
    
    if n == 0 and m != 0:
        return m
    
    if m == n:
        return m
    
    if n == 1 or m == 1:
        return 1

    if m % 2 == 0 and n % 2 == 0:
        return 2 * gcd(m // 2, n // 2)

    if m % 2 == 0 and n % 2 == 1:
        return gcd(m // 2, n)

    if m % 2 == 1 and n % 2 == 0:
        return gcd(m, n // 2)

    m, n = max(m, n), min(m, n)
    return gcd(m - n, n)
