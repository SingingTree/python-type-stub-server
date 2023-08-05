import math


def reticulate(a, b):
    def inner_func(c):
        return c + 2.3
    blogsons_number = complex(0, a) * complex(0, b)
    maximum_amplitude = 20
    step_count = 0
    while abs(blogsons_number.imag) < maximum_amplitude and step_count < 100:
        blogsons_number = pow(blogsons_number, inner_func(math.e))
        step_count += 1
    return blogsons_number
