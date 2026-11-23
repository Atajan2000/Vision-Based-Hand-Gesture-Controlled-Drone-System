# Vision-Based Hand Gesture Controlled Drone System

A camera-based interface for controlling a drone with eight hand gestures. Developed for my undergraduate thesis at Chongqing University of Posts and Telecommunications in 2024, the project combines MediaPipe hand tracking, a TensorFlow Lite gesture classifier and MAVLink commands through DroneKit.

[Watch the demonstration](https://www.bilibili.com/video/BV1Lm421n7jQ/) | [Read the full thesis](docs/Atajan-Garayev-Gesture-Controlled-Drone-Thesis.pdf) | [Download the thesis](docs/Atajan-Garayev-Gesture-Controlled-Drone-Thesis.pdf?raw=true)

![Eight hand gestures and their command labels](docs/images/thesis-gesture-examples.jpeg)

*The eight gestures used for movement, stopping and landing.*

## Hardware

The drone platform uses a Prometheus 450 (P450) frame, a Pixhawk V6C flight controller, an NVIDIA Jetson NX companion computer and a USB camera. The companion computer processes camera images and sends flight commands to the controller over MAVLink.

## Results

Testing covered the eight predefined gestures with different lighting conditions, backgrounds and users.

| Measurement | Result |
|---|---|
| Gesture recognition and command execution success rate | 98% |
| Average response time from gesture recognition to command execution | Approximately 0.3 seconds |

The full experimental discussion and results are included in Chapter 5 of the [thesis](docs/Atajan-Garayev-Gesture-Controlled-Drone-Thesis.pdf).

## How it works

```text
Camera -> Hand landmarks -> Gesture classification -> Command buffer -> Drone
```

MediaPipe tracks 21 hand landmarks. Their coordinates are normalized relative to the wrist and passed to a neural network as 42 input values. The classifier selects one of eight gestures, and a short voting buffer filters isolated changes before sending the corresponding MAVLink command. The default buffer requires four matching observations.

## Gesture commands

| ID | Gesture | Command |
|---|---|---|
| 0 | Forward | North at 1 m/s |
| 1 | Stop | Zero velocity |
| 2 | Up | Ascend at 1 m/s |
| 3 | Land | Switch to `LAND` mode |
| 4 | Down | Descend at 1 m/s |
| 5 | Back | South at 1 m/s |
| 6 | Left | West at 1 m/s |
| 7 | Right | East at 1 m/s |

Movement uses the local north-east-down coordinate frame (`MAV_FRAME_LOCAL_NED`). Horizontal directions refer to these axes, regardless of the drone's heading. Velocity and landing commands require `GUIDED` mode. Arming and takeoff are handled separately from the gesture loop.

## Getting started

You need a webcam and, for vehicle control, a MAVLink endpoint that supports the controller's `GUIDED` and `LAND` modes. Check the commands in an ArduPilot SITL simulator before connecting flight hardware.

Use a virtual environment compatible with the legacy MediaPipe Solutions, TensorFlow Lite and DroneKit APIs. The original training notebook used Python 3.8.5; `requirements.txt` contains dependency version constraints.

Install dependencies from the repository root:

```bash
python -m pip install -r requirements.txt
```

### Run gesture recognition

```bash
python -m tests.gesture_test --device 0
```

This opens the webcam display without connecting to a vehicle. Press **Esc** to close it.

### Connect to a simulator or drone

Set the connection string for your MAVLink endpoint. For a local SITL instance exposing TCP port 5760:

```bash
python main.py --connection_string tcp:127.0.0.1:5760
```

Camera and recognition settings are available in `config.txt` and through command-line arguments:

```bash
python main.py --device 0 --width 960 --height 540 --buffer_len 5 --connection_string tcp:127.0.0.1:5760
```

Run from the repository root so model and label paths resolve correctly. Establish the vehicle's flight state and mode before issuing commands. Pressing **Esc** closes the application and connection; it does not request landing.

## Model training

`Keypoint_model_training.ipynb` trains an eight-class classifier from hand-landmark coordinates and exports it to TensorFlow Lite. The base network uses dense layers of 32, 32 and 16 ReLU units followed by eight softmax outputs. The notebook uses a 75/25 train/test split and includes hyperparameter experiments.

To train from the repository root, set these notebook paths:

```python
dataset = 'model/keypoint_classifier/keypoint.csv'
model_save_path = 'model/keypoint_classifier/keypoint_classifier.hdf5'
tflite_save_path = 'model/keypoint_classifier/keypoint_classifier.tflite'
```

Install pandas, scikit-learn, matplotlib, seaborn and Jupyter for the training workflow. Keep classifier output IDs aligned with the gesture label CSV and command mapping when retraining.

## Operating notes

- Lighting, occlusion and hand orientation affect recognition. The classifier selects the highest-scoring class without a confidence rejection threshold.
- Losing hand detection does not send an automatic stop command. Configure vehicle failsafes and retain manual control during testing.
- Collision avoidance and geofencing must be provided by the vehicle setup; they are not implemented by the gesture application.

## Repository structure

| Path | Contents |
|---|---|
| `main.py`, `config.txt` | Application loop and configuration |
| `gestures/` | Hand recognition, command buffering and vehicle control |
| `model/` | Classifiers, checkpoints, labels and landmark datasets |
| `Keypoint_model_training.ipynb` | Classifier training and TensorFlow Lite export |
| `tests/` | Interactive camera and connection checks |
| `utils/` | Display utilities |
| `docs/` | Full thesis and gesture illustration |

## Thesis

**Vision Based Gesture Controlled Drone System**  
Garayev Atajan, Computer Science and Technology  
Chongqing University of Posts and Telecommunications, June 2024

[Read or download the full thesis](docs/Atajan-Garayev-Gesture-Controlled-Drone-Thesis.pdf).

## License and acknowledgments

The project uses the [GNU GPL v3 license](LICENSE).

The landmark preprocessing, classifier wrappers and FPS utility include material from [kinivi's MediaPipe hand-gesture recognition sample](https://github.com/kinivi/hand-gesture-recognition-mediapipe), licensed under Apache 2.0. See [third-party notices](THIRD_PARTY_NOTICES.md) and the included [Apache license](LICENSES/Apache-2.0.txt).

Built with [MediaPipe](https://github.com/google-ai-edge/mediapipe), [TensorFlow](https://github.com/tensorflow/tensorflow), [OpenCV](https://opencv.org/), [DroneKit](https://github.com/dronekit/dronekit-python) and [MAVLink](https://mavlink.io/).
