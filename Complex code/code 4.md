# Code 4

```python
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
    reward -= CENTER_PENALTY * distance_from_center / track_width

    # Direction penalty
    if is_left_of_center:
        angle_from_center = abs(heading - 90)
    else:
        angle_from_center = abs(heading + 270)
    reward -= DIRECTION_PENALTY * angle_from_center / 90.0

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

    # Cap reward to maximum
    reward = max(MIN_REWARD, min(MAX_REWARD, reward))

    return float(reward)
```

This code is similar to the previous one, but let's break it down:

- **Constants**: These are parameters that can be adjusted to fine-tune the behavior of the DeepRacer.

- **Extract Data**: The relevant data such as distance from the center, track width, heading, progress, speed, and steering angle is extracted from the input parameters.

- **Reward Initialization**: The initial reward is set to a minimum value.

- **Center Penalty**: It penalizes the car for being away from the center of the track.

- **Direction Penalty**: Penalizes the car for deviating from the ideal direction towards the center of the track.

- **Speed Penalty**: Penalizes the car for speed deviation from a predefined threshold.

- **Progress Reward**: Rewards the car for making progress along the track.

- **Excessive Steering Penalty**: Penalizes the car for excessive steering angle.

- **Smooth Steering Reward**: Provides a reward for smooth steering.

- **Reward Capping**: Ensures that the reward remains within a specified range.

This function is designed to guide the DeepRacer agent to exhibit behaviors that lead to efficient and effective racing. Adjustments to the constants can fine-tune the behavior of the DeepRacer agent.
