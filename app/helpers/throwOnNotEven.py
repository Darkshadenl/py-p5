def throwOnNotEven(number, name):
    if (number % 2 != 0):
        raise ValueError(name + " should be even.")