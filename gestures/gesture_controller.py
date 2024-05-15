from dronekit import VehicleMode, connect
from pymavlink import mavutil
import time

class GestureController:
    def __init__(self, connection_string):
        print("Connecting to drone on: {}".format(connection_string))
        self.vehicle = connect(connection_string, wait_ready=True)
        print("Connected to drone.")

    def arm_and_takeoff(self, aTargetAltitude):
        """
        Arms vehicle and fly to aTargetAltitude.
        """
        print("Arming motors")
        self.vehicle.mode = VehicleMode("GUIDED")
        self.vehicle.armed = True

        while not self.vehicle.armed:
            print(" Waiting for arming...")
            time.sleep(1)

        print("Taking off!")
        self.vehicle.simple_takeoff(aTargetAltitude)

        while True:
            print(" Altitude: ", self.vehicle.location.global_relative_frame.alt)
            if self.vehicle.location.global_relative_frame.alt >= aTargetAltitude * 0.95:
                print("Reached target altitude")
                break
            time.sleep(1)

    def set_velocity(self, vx, vy, vz, yaw_rate=0):
        """
        Sets the velocity of the drone.
        """
        if self.vehicle.mode.name == "GUIDED":
            msg = self.vehicle.message_factory.set_position_target_local_ned_encode(
                0, 0, 0,
                mavutil.mavlink.MAV_FRAME_LOCAL_NED,
                0b0000111111000111,
                0, 0, 0,
                vx, vy, vz,
                0, 0, 0,
                0, yaw_rate)
            self.vehicle.send_mavlink(msg)
        else:
            print("Vehicle is not in GUIDED mode. Cannot set velocity.")

    def condition_yaw(self, heading, relative=False):
        """
        Changes the yaw of the drone (rotational movement).
        """
        if self.vehicle.mode.name == "GUIDED":
            is_relative = 1 if relative else 0
            msg = self.vehicle.message_factory.command_long_encode(
                0, 0,  # target system, target component
                mavutil.mavlink.MAV_CMD_CONDITION_YAW,  # command
                0,  # confirmation
                heading,  # param 1, yaw in degrees
                0,  # param 2, yaw speed deg/s
                1,  # param 3, direction -1 ccw, 1 cw
                is_relative,  # param 4, relative offset 1, absolute angle 0
                0, 0, 0  # param 5 ~ 7 not used
            )
            self.vehicle.send_mavlink(msg)
        else:
            print("Vehicle is not in GUIDED mode. Cannot condition yaw.")

    def set_roi(self, lat, lon, alt):
        """
        Sets the Region of Interest (ROI) for the camera.
        """
        if self.vehicle.mode.name == "GUIDED":
            msg = self.vehicle.message_factory.command_long_encode(
                0, 0, 0,
                mavutil.mavlink.MAV_CMD_DO_SET_ROI_LOCATION,
                0,  # Confirmation
                0, 0, 0,  # Params 1-3 (not used)
                lat, lon, alt,  # Params 4-6 - ROI location
                0  # Param 7 (not used)
            )
            self.vehicle.send_mavlink(msg)
        else:
            print("Vehicle is not in GUIDED mode. Cannot set ROI.")

    def gesture_control(self, gesture_id):
        """
        Controls the drone based on the gesture ID.
        """
        print("GESTURE", gesture_id)

        # Example gestures for movement
        if gesture_id == 0:  # Forward
            self.set_velocity(1, 0, 0)
        elif gesture_id == 5:  # Backward
            self.set_velocity(-1, 0, 0)
        elif gesture_id == 6:  # Left
            self.set_velocity(0, -1, 0)
        elif gesture_id == 7:  # Right
            self.set_velocity(0, 1, 0)
        elif gesture_id == 4:  # Up
            self.set_velocity(0, 0, 1)
        elif gesture_id == 2:  # Down
            self.set_velocity(0, 0, -1)
        elif gesture_id == 1:  # Stop
            self.stop()
        elif gesture_id == 3:  # Land
            self.land()

    def stop(self):
        """
        Stops the drone's movement and brings it to a hover.
        """
        self.set_velocity(0, 0, 0)

    def land(self):
        """
        Lands the drone.
        """
        if self.vehicle.mode.name == "GUIDED":
            self.vehicle.mode = VehicleMode("LAND")
        else:
            print("Vehicle is not in GUIDED mode. Cannot land.")


