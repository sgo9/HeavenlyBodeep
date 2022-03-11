# HeavenlyBodeep

HeavenlyBodeep is a program developped to allow to play the game [Heavenly Bodies](https://heavenlybodiesgame.com/) via webcam instead of keyboard or joystick.
- 

## Getting started
You will need:
- The Heavenly Bodies game (compatibility with Windows only)
- vJoy and x360 (see [link](https://u.pcloud.link/publink/show?code=kZYDtXVZLL74XzxE9SfoSurJi4PnbJDv2bf7))
- Python installed on Windows (to access the camera)
- The HeavenlyBodeep package

Settings for x360:
setup the buttons exactly as shown below.
![](images_readme/xcontroller_config.JPG)


To lauch the game with HeavenlyBodeep:
1. Start x360
2. Start the game (up to starting a level)
3. Run the "main_with_mode.py" file

## The different gaming modes
In the "main_with_mode.py" file, you will find the option to choose between 3 modes:
1. No camera correction
2. Camera correction in game (X control)
3. Camera correction with angle prediction model

This package was made in particular for mode 3: a CNN model was developped to correct the angles of the arms when the astronaut isn't facing upwards.

## Pose detection controls

Pose detection is made using the [Mediapipe Holistic model](https://google.github.io/mediapipe/solutions/holistic.html). The output of this model is sent to x360 via vjoy using the pyvjoy package.

The controls are the following:
- Move the arms up and down to independently control the arms of the astronaut
- Raise one (left or right) knee to fold both the legs of the astronaut
- Grab the hands to grab objects in the game
- Join the hands together (namaste) to press A
- Tilt the body to realign the camera with the astronaut

![](images_readme/ezgif.com-gif-maker.gif)


## Astrobot



