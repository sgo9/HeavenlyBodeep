"""Standard functions"""

def mode_selection():
    """Start deep controller"""
    print('\nWelcome to deep controller.\n')

    mode_details = """
    Select camera correction mode:
    1 - no camera correction
    2 - camera correction in game (X control)
    3 - camera correction with angle prediction model

    """

    mode_selection = 0
    while mode_selection not in [1,2,3]:
        mode_selection = int(input(mode_details))

    return mode_selection

def distance(x1, x2, y1, y2):
    """Return distance between two points in 2D dimension"""
    return ((x2-x1)**2 + (y2-y1)**2)**0.5