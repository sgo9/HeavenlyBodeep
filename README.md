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


# Startup the project

The initial setup.

Create virtualenv and install the project:
```bash
sudo apt-get install virtualenv python-pip python-dev
deactivate; virtualenv ~/venv ; source ~/venv/bin/activate ;\
    pip install pip -U; pip install -r requirements.txt
```

Unittest test:
```bash
make clean install test
```

Check for HeavenlyBodeep in gitlab.com/{group}.
If your project is not set please add it:

- Create a new project on `gitlab.com/{group}/HeavenlyBodeep`
- Then populate it:

```bash
##   e.g. if group is "{group}" and project_name is "HeavenlyBodeep"
git remote add origin git@github.com:{group}/HeavenlyBodeep.git
git push -u origin master
git push -u origin --tags
```

Functionnal test with a script:

```bash
cd
mkdir tmp
cd tmp
HeavenlyBodeep-run
```

# Install

Go to `https://github.com/{group}/HeavenlyBodeep` to see the project, manage issues,
setup you ssh public key, ...

Create a python3 virtualenv and activate it:

```bash
sudo apt-get install virtualenv python-pip python-dev
deactivate; virtualenv -ppython3 ~/venv ; source ~/venv/bin/activate
```

Clone the project and install it:

```bash
git clone git@github.com:{group}/HeavenlyBodeep.git
cd HeavenlyBodeep
pip install -r requirements.txt
make clean install test                # install and test
```
Functionnal test with a script:

```bash
cd
mkdir tmp
cd tmp
HeavenlyBodeep-run
```
