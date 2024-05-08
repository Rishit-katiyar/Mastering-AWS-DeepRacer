# Level-1 

```python
def reward_function(params):
    # Read input parameters
    all_wheels_on_track = params['all_wheels_on_track']
    distance_from_center = params['distance_from_center']
    track_width = params['track_width']
    
    # Give a very low reward by default
    reward = 1e-3

    # Give a high reward if no wheels go off the track and
    # the agent is somewhere in between the track borders
    if all_wheels_on_track and (0.5 * track_width - distance_from_center) >= 0.05:
        reward = 1.0

    # Always return a float value
    return float(reward)
```

This code implements a basic reward function for level 1, where the agent is rewarded for staying within the track borders. The function checks if all wheels are on the track and if the distance from the center is within a certain range from the track borders. If both conditions are met, a high reward of 1.0 is given; otherwise, a very low reward of 1e-3 is returned. Adjustments to the threshold value (0.05) can be made to fine-tune the agent's behavior.
