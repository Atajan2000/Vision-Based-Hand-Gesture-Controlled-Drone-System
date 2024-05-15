import configargparse
import cv2 as cv
from gestures.gesture_recognition import GestureRecognition, GestureBuffer
from utils.cvfpscalc import CvFpsCalc
from gestures.gesture_controller import GestureController

def get_args():
    parser = configargparse.ArgParser(default_config_files=['config.txt'])
    parser.add('-c', '--my-config', required=False, is_config_file=True, help='config file path')
    parser.add("--device", type=int, default=0)
    parser.add("--width", help='cap width', type=int, default=960)
    parser.add("--height", help='cap height', type=int, default=540)
    parser.add('--use_static_image_mode', action='store_true', help='True if running on photos')
    parser.add("--min_detection_confidence", help='min_detection_confidence', type=float, default=0.7)
    parser.add("--min_tracking_confidence", help='min_tracking_confidence', type=float, default=0.7)
    parser.add("--buffer_len", help='Length of gesture buffer', type=int, default=5)
    parser.add("--connection_string", help="Connection string for connecting to the drone", type=str, default="tcp:192.168.10.7:6000")
    args = parser.parse_args()
    return args

def main():
    # Argument parsing
    args = get_args()

    # Camera preparation
    cap = cv.VideoCapture(args.device)
    cap.set(cv.CAP_PROP_FRAME_WIDTH, args.width)
    cap.set(cv.CAP_PROP_FRAME_HEIGHT, args.height)

    # Initialize the GestureController with the connection string
    gesture_controller = GestureController(args.connection_string)

    # Initialize Gesture Recognition and Buffer
    gesture_detector = GestureRecognition(args.use_static_image_mode, args.min_detection_confidence, args.min_tracking_confidence, history_length=16)
    gesture_buffer = GestureBuffer(buffer_len=args.buffer_len)

    # FPS Measurement
    cv_fps_calc = CvFpsCalc(buffer_len=10)

    while True:
        fps = cv_fps_calc.get()

        # Camera capture
        ret, image = cap.read()
        if not ret:
            print("Ignoring empty camera frame.")
            continue

        debug_image, gesture_id = gesture_detector.recognize(image)
        gesture_buffer.add_gesture(gesture_id)

        # Gesture control
        gesture = gesture_buffer.get_gesture()
        if gesture is not None:
            gesture_controller.gesture_control(gesture)

        # Display the resulting frame
        debug_image = gesture_detector.draw_info(debug_image, fps, mode=1, number=0)
        cv.imshow('Gesture Recognition', debug_image)
        if cv.waitKey(5) & 0xFF == 27:  # ESC key to exit
            break

    # Clean up
    gesture_controller.close()
    cap.release()
    cv.destroyAllWindows()

if __name__ == '__main__':
    main()
