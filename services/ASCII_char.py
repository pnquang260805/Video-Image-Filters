def get_level(level_number: int = 10) -> str:
    """
    define the two grayscale levels used to convert brightness values to ASCII characters as global values. 
    """
    if level_number == 10:
        return "@%#*+=-:. "
    elif level_number == 70:
        return r"$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~i!lI;:,\"^`. "
    elif level_number == 5:
        return r"o0@#."
    else:
        raise RuntimeError("Invalid level") 