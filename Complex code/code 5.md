# Code 5

```python
import numpy as np
import math

def reward_function(params):
    # Constants
    MIN_REWARD = 1e-3
    MAX_REWARD = 1.0
    WAYPOINT_REWARD = 0.5
    CENTER_PENALTY = 0.2
    DIRECTION_PENALTY = 0.3
    SPEED_THRESHOLD = 1.0
    SPEED_PENALTY = 0.1
    PROGRESS_REWARD = 0.3
    STEERING_THRESHOLD = 15.0
    SMOOTHNESS_REWARD = 0.2
    ACCELERATION_REWARD = 0.1
    TURNING_REWARD = 0.1

    # Extract relevant data
    distance_from_center = params['distance_from_center']
    track_width = params['track_width']
    is_left_of_center = params['is_left_of_center']
    heading = params['heading']
    progress = params['progress']
    speed = params['speed']
    steering = abs(params['steering_angle'])

    # Initialize reward
    reward = MIN_REWARD

    # Penalty for being away from the center
    reward -= CENTER_PENALTY * (distance_from_center / (0.5 * track_width))

    # Direction penalty
    if is_left_of_center:
        angle_from_center = abs(heading - 90)
    else:
        angle_from_center = abs(heading + 270)
    reward -= DIRECTION_PENALTY * (angle_from_center / 90.0)

    # Penalty for speed deviation
    if speed < SPEED_THRESHOLD:
        reward -= SPEED_PENALTY * (SPEED_THRESHOLD - speed)

    # Reward for making progress
    reward += PROGRESS_REWARD * progress

    # Penalty for excessive steering
    if steering > STEERING_THRESHOLD:
        reward -= (steering - STEERING_THRESHOLD) / 90.0

    # Reward for smooth steering
    if steering < 10:
        reward += SMOOTHNESS_REWARD

    # Reward for acceleration
    if 'last_speed' in params:
        acceleration = speed - params['last_speed']
        if acceleration > 0:
            reward += ACCELERATION_REWARD

    # Reward for turning
    if 'last_heading' in params:
        heading_change = abs(heading - params['last_heading'])
        if heading_change > 5:
            reward += TURNING_REWARD

    # Cap reward to maximum
    reward = max(MIN_REWARD, min(MAX_REWARD, reward))

    return float(reward)

```

This version of the reward function includes additional features such as rewards for acceleration and turning:

- **Acceleration Reward**: Provides a reward if the car is accelerating.

- **Turning Reward**: Provides a reward if the car is turning.

These additional features make the reward function more complex and allow for finer control over the behavior of the DeepRacer agent. Adjustments to the constants can further fine-tune the behavior of the agent.
