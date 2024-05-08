# Code 2

### Advanced AWS DeepRacer Reward Function

```python
import numpy as np
import math

def reward_function(params):
    # Extracting parameters
    all_wheels_on_track = params['all_wheels_on_track']
    distance_from_center = params['distance_from_center']
    track_width = params['track_width']
    is_left_of_center = params['is_left_of_center']
    heading = params['heading']
    waypoints = params['waypoints']
    progress = params['progress']
    speed = params['speed']
    steering = params['steering_angle']

    # Constants and weights
    MIN_REWARD = 1e-3
    FULL_REWARD_DISTANCE = 0.4 * track_width
    CENTER_WEIGHT = 0.5
    DIRECTION_WEIGHT = 0.3
    SPEED_WEIGHT = 0.3
    PROGRESS_WEIGHT = 0.2
    CURVATURE_WEIGHT = 0.2
    WAYPOINT_WEIGHT = 0.3
    SMOOTHNESS_WEIGHT = 0.1
    PROXIMITY_WEIGHT = 0.2
    
    SPEED_MIN = 0.8
    SPEED_MAX = 1.0
    
    reward = MIN_REWARD
    
    # Track constraints check
    if all_wheels_on_track:
        # Distance from center penalty
        deviation_penalty = CENTER_WEIGHT * distance_from_center
        reward += max((1 - deviation_penalty), 0)
        
        # Full reward distance
        if distance_from_center <= FULL_REWARD_DISTANCE:
            reward += 1.0
        
        # Direction penalty
        if is_left_of_center:
            angle_from_center = abs(heading - 90)
        else:
            angle_from_center = abs(heading + 270)
        
        direction_penalty = DIRECTION_WEIGHT * angle_from_center
        reward += max((1 - direction_penalty), 0)
        
        # Speed penalty
        if speed < SPEED_MIN:
            reward -= SPEED_WEIGHT * (SPEED_MIN - speed)
        elif speed > SPEED_MAX:
            reward -= SPEED_WEIGHT * (speed - SPEED_MAX)
        
        # Progress reward
        reward += PROGRESS_WEIGHT * progress
        
        # Curvature penalty
        curvature_deviation = abs(steering) / 30.0
        reward -= CURVATURE_WEIGHT * curvature_deviation
        
        # Waypoint reward
        next_waypoint_index = params['closest_waypoints'][1]
        next_waypoint = waypoints[next_waypoint_index]
        distance_to_next_waypoint = math.sqrt((params['x'] - next_waypoint[0]) ** 2 + (params['y'] - next_waypoint[1]) ** 2)
        reward += WAYPOINT_WEIGHT * max((1 - (distance_to_next_waypoint / track_width)), 0)
        
        # Smoothness reward
        if abs(steering) < 5:
            reward += SMOOTHNESS_WEIGHT
        
        # Proximity reward
        proximity_reward = PROXIMITY_WEIGHT * np.mean(np.abs(np.array(params['closest_waypoints']) - np.array(params['car_coordinates'])))
        reward += proximity_reward
    
    else:
        reward = MIN_REWARD
    
    return float(reward)
```

#### Explanation:
This Python function represents a hyper-advanced reward function for AWS DeepRacer, a reinforcement learning-based autonomous racing car. Here's a breakdown of its components and functionality:

- **Input Parameters**: The function takes various parameters such as the car's position, speed, steering angle, track information, and progress.

- **Constants and Weights**: Various constants and weights are defined to adjust the contribution of different factors to the overall reward calculation.

- **Track Constraints Check**: It checks if all wheels of the car are on the track. If not, the reward remains at a minimum value.

- **Distance from Center Penalty**: Calculates a penalty based on how far the car is from the center of the track and adjusts the reward accordingly. Being closer to the center earns more reward.

- **Full Reward Distance**: If the car is within a certain distance from the center of the track, it receives a full reward.

- **Direction Penalty**: Calculates a penalty based on the deviation of the car's heading from the ideal direction (centered on the track).

- **Speed Penalty**: Penalizes the car if its speed is lower than a defined minimum or higher than a defined maximum.

- **Progress Reward**: Rewards the car for making progress along the track.

- **Curvature Penalty**: Penalizes the car for excessive steering, aiming for smoother turns.

- **Waypoint Reward**: Rewards the car for reaching waypoints along the track. The reward decreases as the distance to the next waypoint increases.

- **Smoothness Reward**: Provides a reward for smooth steering, encouraging less abrupt changes in direction.

- **Proximity Reward**: Calculates a reward based on the proximity of the car to the next waypoints, encouraging the car to stay close to the optimal path.

- **Return Reward**: Finally, the calculated reward is returned as a float value.
