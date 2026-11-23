# Third-party notices

## MediaPipe hand-gesture sample

The landmark-preprocessing and classifier-wrapper code in this repository corresponds to the approach and implementation in [kinivi/hand-gesture-recognition-mediapipe](https://github.com/kinivi/hand-gesture-recognition-mediapipe). The local `utils/cvfpscalc.py` matches that project's utility after line-ending normalization.

Upstream is distributed under Apache License 2.0. Its full license is included in `LICENSES/Apache-2.0.txt`. Recognition code and the webcam demo have been adapted for this repository's command labels and drone-control integration. The webcam demo now imports its FPS utility explicitly and resolves model paths from the repository root.

The exact provenance of the bundled trained model weights and landmark datasets is not recorded in the original repository. Those artifacts should not be described as independently authored or independently evaluated based only on the files present.

## Dependencies

MediaPipe, TensorFlow, OpenCV, DroneKit, pymavlink and ConfigArgParse are installed separately. Refer to their upstream repositories and package metadata for their licenses. The root `LICENSE` retains this project's existing GPL v3 declaration.
