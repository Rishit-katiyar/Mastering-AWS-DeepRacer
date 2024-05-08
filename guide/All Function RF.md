# All Functions Found On The Internet And Combined

### break down of this codes working:

1. **PerformanceEvaluator Class**:
    - This class contains methods to evaluate the performance of a car in a simulated racing environment.
    - It initializes with parameters received from the racing environment.
    - Methods are provided to calculate various aspects of car performance such as optimal speed ratio, angle of turn, whether the car is in a turn, etc.
    - The `evaluate()` method combines these performance metrics to calculate a reward value for the car's behavior.

2. **Reward Function**:
    - The `reward_function` is the main entry point for the racing environment to evaluate the car's performance.
    - It instantiates a `PerformanceEvaluator` object with the received parameters and calls its `evaluate()` method to get the reward value.

3. **Constants**:
    - Various constants are defined at the beginning of the code to fine-tune the performance evaluation process. These include parameters like maximum speed, minimum speed, maximum steering angle, etc.

4. **Parameter Initialization**:
    - The `init_params()` method initializes the class properties with the parameters received from the racing environment.

5. **Performance Evaluation Methods**:
    - Methods like `car_heading_error()`, `optimal_speed_ratio()`, `in_turn()`, etc., calculate specific aspects of the car's performance based on the current state and environment parameters.

6. **Reward Calculation**:
    - The `evaluate()` method calculates the overall reward value based on the car's performance metrics.
    - It checks various conditions such as track status, car heading, steering angle, etc., and assigns reward points accordingly.
    - The final reward value is returned based on these calculations.

7. **Logging**:
    - The code includes logging functionality to track the evaluation process. The `log_feature()` method accumulates log messages throughout the evaluation process.

```python
# -*- coding: utf-8 -*-

import math
import traceback

class PerformanceEvaluator:
    # CONSTANTS
    MAX_SPEED = 5.0
    MIN_SPEED = 1.5
    MAX_STEERING_ANGLE = 30
    SMOOTH_STEERING_TRESHOLD = 15
    SAFE_DISTANCE = 0.8
    CENTERLINE_FOLLOW_TRESHOLD = 0.12
    ANGLE_CURVE = 3
    MAX_PENALTY = 0.001
    MAX_REWARD = 89999

    def __init__(self, params):
        self.params = params
        self.init_params(params)

    def init_params(self, params):
        self.track_status = params['track_status']
        self.car_x = params['car_x']
        self.car_y = params['car_y']
        self.dist_center = params['dist_center']
        self.left_center = params['left_center']
        self.reversed = params['reversed']
        self.heading = params['heading']
        self.progress = params['progress']
        self.steps = params['steps']
        self.speed = params['speed']
        self.steering = params['steering']
        self.track_width = params['track_width']
        self.waypoints = params['waypoints']
        self.closest_waypoints = params['closest_waypoints']
        self.prev_waypoint = self.closest_waypoints[0]
        self.next_waypoint = self.closest_waypoints[1]
        self.logs = ""

    def status_report(self):
        status = self.params
        if 'waypoints' in status: del status['waypoints']
        status['log'] = self.logs
        print(status)

    def get_waypoint(self, index):
        if index > (len(self.waypoints) - 1):
            return self.waypoints[index - (len(self.waypoints))]
        elif index < 0:
            return self.waypoints[len(self.waypoints) + index]
        else:
            return self.waypoints[index]

    @staticmethod
    def distance_waypoints(prev, next):
        return math.sqrt(pow(next[1] - prev[1], 2) + pow(next[0] - prev[0], 2))

    @staticmethod
    def heading_waypoints(prev, next):
        direction = math.atan2(next[1] - prev[1], next[0] - prev[0])
        return math.degrees(direction)

    def car_heading_error(self):
        next_point = self.get_waypoint(self.next_waypoint)
        prev_point = self.get_waypoint(self.prev_waypoint)
        direction = math.atan2(next_point[1] - prev_point[1], next_point[0] - prev_point[0])
        direction = math.degrees(direction)
        return direction - self.heading

    def optimal_speed_ratio(self):
        if abs(self.car_heading_error()) >= self.MAX_STEERING_ANGLE:
            return 0.34
        if abs(self.car_heading_error()) >= (self.MAX_STEERING_ANGLE * 0.75):
            return 0.67
        current_position = (self.car_x, self.car_y)
        current_wp_index = self.next_waypoint
        length = self.distance_waypoints(current_position, self.get_waypoint(current_wp_index))
        current_track_heading = self.heading_waypoints(self.get_waypoint(current_wp_index),
                                                                   self.get_waypoint(current_wp_index + 1))
        while True:
            from_point = self.get_waypoint(current_wp_index)
            to_point = self.get_waypoint(current_wp_index + 1)
            length = length + self.distance_waypoints(from_point, to_point)
            if length >= self.SAFE_DISTANCE:
                heading_to_horizon = self.heading_waypoints(self.get_waypoint(self.closest_waypoints[1]), to_point)
                if abs(current_track_heading - heading_to_horizon) > (self.MAX_STEERING_ANGLE * 0.5):
                    return 0.33
                elif abs(current_track_heading - heading_to_horizon) > (self.MAX_STEERING_ANGLE * 0.25):
                    return 0.66
                else:
                    return 1.0

    def turn_angle(self):
        angle_ahead = self.heading_waypoints(self.get_waypoint(self.prev_waypoint), self.get_waypoint(self.next_waypoint))
        angle_behind = self.heading_waypoints(self.get_waypoint(self.prev_waypoint - 1), self.get_waypoint(self.prev_waypoint))
        result = angle_ahead - angle_behind
        if angle_ahead < -90 and angle_behind > 90:
            return 360 + result
        elif result > 180:
            return -180 + (result - 180)
        elif result < -180:
            return 180 - (result + 180)
        else:
            return result

    def in_turn(self):
        if abs(self.turn_angle()) >= self.ANGLE_CURVE:
            return True
        else:
            return False

    def reached_finish(self):
        max_waypoint_index = len(self.waypoints) - 1
        if self.next_waypoint == max_waypoint_index:
            return True
        else:
            return False

    def expected_turn_direction(self):
        current_waypoint_index = self.next_waypoint
        length = self.distance_waypoints((self.car_x, self.car_y), self.get_waypoint(current_waypoint_index))
        while True:
            from_point = self.get_waypoint(current_waypoint_index)
            to_point = self.get_waypoint(current_waypoint_index + 1)
            length = length + self.distance_waypoints(from_point, to_point)
            if length >= self.SAFE_DISTANCE * 4.5:
                result = self.heading_waypoints(self.get_waypoint(self.closest_waypoints[1]), to_point)
                if result > 2:
                    return "LEFT"
                elif result < -2:
                    return "RIGHT"
                else:
                    return "STRAIGHT"
            current_waypoint_index = current_waypoint_index + 1

    def in_optimized_corridor(self):
        if self.in_turn():
            turn_angle = self.turn_angle()
            if turn_angle > 0:
                if (self.left_center == True and self.dist_center <= (
                        self.CENTERLINE_FOLLOW_TRESHOLD * 2 * self.track_width) or
                        self.left_center == False and self.dist_center <= (
                                self.CENTERLINE_FOLLOW_TRESHOLD / 2 * self.track_width)):
                    return True
                else:
                    return False
            else:
                if self.left_center == True and self.dist_center <= (self.CENTERLINE_FOLLOW_TRESHOLD / 2 * self.track_width) or self.left_center == False and self.dist_center <= (self.CENTERLINE_FOLLOW_TRESHOLD *

 2 * self.track_width):
                    return True
                else:
                    return False
        else:
            next_turn = self.expected_turn_direction()
            if next_turn == "LEFT":
                if self.left_center == True and self.dist_center <= (
                        self.CENTERLINE_FOLLOW_TRESHOLD / 2 * self.track_width) or self.left_center == False and self.dist_center <= (self.CENTERLINE_FOLLOW_TRESHOLD * 2 * self.track_width):
                    return True
                else:
                    return False
            elif next_turn == "RIGHT":
                if self.left_center == True and self.dist_center <= (
                        self.CENTERLINE_FOLLOW_TRESHOLD * 2 * self.track_width) or self.left_center == False and self.dist_center <= (self.CENTERLINE_FOLLOW_TRESHOLD / 2 * self.track_width):
                    return True
                else:
                    return False
            else:
                if self.dist_center <= (self.CENTERLINE_FOLLOW_TRESHOLD * 2 * self.track_width):
                    return True
                else:
                    return False

    def optimum_speed(self):
        if abs(self.speed - (self.optimal_speed_ratio() * self.MAX_SPEED)) < (self.MAX_SPEED * 0.15) and self.MIN_SPEED <= self.speed <= self.MAX_SPEED:
            return True
        else:
            return False

    def log_feature(self, message):
        if message is None:
            message = 'NULL'
        self.logs = self.logs + str(message) + '|'

    def evaluate(self):
        self.init_params(self.params)
        result_reward = 0.001
        try:
            if self.track_status == False or self.reversed == True or (self.speed < (0.1 * self.MAX_SPEED)):
                self.log_feature("track_status or reversed issue")
                self.status_report()
                return self.MAX_PENALTY

            if abs(self.car_heading_error()) <= self.SMOOTH_STEERING_TRESHOLD:
                self.log_feature("car_heading_ok")
                result_reward += self.MAX_REWARD * 0.3

            if abs(self.steering) <= self.SMOOTH_STEERING_TRESHOLD:
                self.log_feature("steering_angle_ok")
                result_reward += self.MAX_REWARD * 0.15

            if self.in_optimized_corridor():
                self.log_feature("in_optimized_corridor")
                result_reward += self.MAX_REWARD * 0.45

            if not (self.in_turn()) and (abs(self.speed - self.MAX_SPEED) < (0.1 * self.MAX_SPEED)) \
                    and abs(self.car_heading_error()) <= self.SMOOTH_STEERING_TRESHOLD:
                self.log_feature("straight_on_max_speed")
                result_reward += self.MAX_REWARD * 1

            if self.in_turn() and self.optimum_speed():
                self.log_feature("optimum_speed_in_curve")
                result_reward += self.MAX_REWARD * 0.6

            TOTAL_NUM_STEPS = 150
            if (self.steps % 100 == 0) and self.progress > (self.steps / TOTAL_NUM_STEPS):
                self.log_feature("progressing_ok")
                result_reward += self.MAX_REWARD * 0.4

            if self.reached_finish():
                self.log_feature("reached_finish")
                result_reward = self.MAX_REWARD

        except Exception as e:
            print("Error : " + str(e))
            print(traceback.format_exc())

        if result_reward > 900000:
            result_reward = 900000

        self.log_feature(result_reward)
        return result_reward

def reward_function(params):
    evaluator = PerformanceEvaluator(params)
    return evaluator.evaluate()
```
