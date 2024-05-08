# Level 3

```python
def reward_function(params):
    # Read input parameters
    all_wheels_on_track = params['all_wheels_on_track']
    distance_from_center = params['distance_from_center']
    track_width = params['track_width']
    abs_steering = abs(params['steering_angle'])  # Absolute steering angle
    speed = params['speed']

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

    return float(reward)
```

In this level 3 reward function:

- It continues to reward the agent for staying within the track borders and penalizes excessive steering, as in level 2.
- Additionally, it incentivizes maintaining a desired speed. If the current speed is equal to or greater than the desired speed (set to 2.5 in this example), the reward is multiplied by 1.2 to encourage maintaining or exceeding the desired speed. If the speed falls below the desired speed, the reward is multiplied by 0.8 to penalize slower speeds.

This enhanced reward function encourages the agent to not only stay within the track borders and minimize excessive steering but also to maintain a desired speed, which can contribute to smoother and more efficient driving behavior. Adjustments to the desired speed value can be made based on the specific requirements of the track and desired driving behavior.
