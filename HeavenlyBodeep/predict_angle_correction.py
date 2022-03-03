"""Use astronaut angle detection trained model to predict the camera correction"""

def compute_angle_correction(game_image):
    """Return the astronaut angle in radiant considering an image of the game [-pi;+pi]"""
    return 10/180*3.14 # TODO write the real function