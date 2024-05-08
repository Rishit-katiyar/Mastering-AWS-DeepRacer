# Level 2

```python
def reward_function(params):
    # Read input parameters
    all_wheels_on_track = params['all_wheels_on_track']
    distance_from_center = params['distance_from_center']
    track_width = params['track_width']
    abs_steering = abs(params['steering_angle'])  # Absolute steering angle

    # Default reward
    reward = 1e-3

    # Reward for staying within the track borders
    if all_wheels_on_track and (0.5 * track_width - distance_from_center) >= 0.05:
        reward = 1.0

    # Penalize excessive steering
    ABS_STEERING_THRESHOLD = 15
    if abs_steering > ABS_STEERING_THRESHOLD:
        reward *= 0.8

    return float(reward)
```

In this level 2 reward function:

- It still rewards the agent for staying within the track borders as in level 1.
- Additionally, it penalizes excessive steering by multiplying the reward by 0.8 if the absolute steering angle exceeds a certain threshold (set to 15 degrees in this example).

This updated reward function encourages the agent not only to stay within the track borders but also to maintain smoother trajectories by minimizing excessive steering. Adjustments to the steering threshold value can be made to balance between allowing necessary steering for navigating curves and penalizing excessive steering.
