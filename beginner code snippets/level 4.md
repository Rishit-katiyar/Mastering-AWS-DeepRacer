# Level 4

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
    objects_distance = params['objects_distance']

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
    if min(objects_distance) < MIN_OBJECTS_DISTANCE:
        reward *= 0.5

    return float(reward)

```

In this level 4 reward function:

- It continues to reward the agent for staying within the track borders, penalizing excessive steering, and maintaining a desired speed, as in level 3.
- Additionally, it introduces rewards for reaching waypoints and penalties for collisions with obstacles.
- The agent is rewarded if it is heading towards the next waypoint within a certain angle threshold (π/4 radians in this example).
- It penalizes the agent if it detects obstacles within a certain distance (MIN_OBJECTS_DISTANCE), discouraging collisions with obstacles.

This enhanced reward function adds more complexity by incorporating waypoint navigation and obstacle avoidance, encouraging the agent to follow the desired path and avoid obstacles while maintaining smooth and efficient driving behavior. Adjustments to the waypoint angle threshold and minimum objects distance can be made based on the specific characteristics of the track and obstacles.
