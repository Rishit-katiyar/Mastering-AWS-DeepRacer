# Level 5

```python
import math

def reward_function(params):
    # Read input parameters
    all_wheels_on_track = params['all_wheels_on_track']
    distance_from_center = params['distance_from_center']
    track_width = params['track_width']
    abs_steering = abs(params['steering_angle'])  # Absolute steering angle
    speed = params['speed']
    waypoints = params['waypoints']
    closest_waypoints = params['closest_waypoints']
    heading = params['heading']
    objects_distance = min(params['objects_distance'])  # Minimum distance to objects
    objects_heading = params['objects_heading']

    # Default reward
    reward = 1e-3

    # Reward for staying within the track borders
    if all_wheels_on_track and (0.5 * track_width - distance_from_center) >= 0.05:
        reward = 1.0

    # Penalize excessive steering
    ABS_STEERING_THRESHOLD = 15
    if abs_steering > ABS_STEERING_THRESHOLD:
        reward *= 0.8

    # Maintain desired speed
    DESIRED_SPEED = 2.5  # Adjust this value as needed
    if speed >= DESIRED_SPEED:
        reward *= 1.2
    else:
        reward *= 0.8

    # Reward for reaching waypoints
    next_waypoint = waypoints[closest_waypoints[1]]
    waypoint_heading = math.atan2(next_waypoint[1] - params['y'], next_waypoint[0] - params['x'])
    angle_difference = abs(heading - waypoint_heading)
    if angle_difference < math.pi / 4:
        reward *= 1.5

    # Penalty for collisions with obstacles
    MIN_OBJECTS_DISTANCE = 2.0  # Adjust this value as needed
    if objects_distance < MIN_OBJECTS_DISTANCE:
        reward *= 0.5

    # Penalize abrupt steering changes
    MAX_STEERING_ANGLE_DIFFERENCE = 10.0  # Adjust this value as needed
    if abs(params['steering_angle']) > 0:
        reward *= math.cos(math.radians(abs(params['steering_angle']) - MAX_STEERING_ANGLE_DIFFERENCE))

    return float(reward)

```

In this level 5 reward function:

- It continues to reward the agent for staying within the track borders, penalizing excessive steering, maintaining a desired speed, reaching waypoints, and avoiding collisions with obstacles, as in level 4.
- Additionally, it penalizes abrupt steering changes by reducing the reward based on the difference between the current steering angle and the maximum allowable steering angle difference (MAX_STEERING_ANGLE_DIFFERENCE). The penalty is calculated using the cosine function, encouraging smoother steering transitions.

This enhanced reward function promotes smoother and more natural steering behavior, contributing to improved driving performance and stability of the agent. Adjustments to the maximum steering angle difference can be made to control the level of penalization for abrupt steering changes.
