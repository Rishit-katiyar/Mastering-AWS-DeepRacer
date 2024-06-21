import math

def reward_function(params):
    # Read input parameters
    all_wheels_on_track = params['all_wheels_on_track']
    distance_from_center = params['distance_from_center']
    track_width = params['track_width']
    heading = params['heading']
    waypoints = params['waypoints']
    progress = params['progress']
    speed = params['speed']
    steering = params['steering_angle']
    closest_waypoints = params['closest_waypoints']
    x = params['x']
    y = params['y']

    # Define constants
    MIN_REWARD = 1e-3
    FULL_REWARD_DISTANCE = 0.3 * track_width  # Allow more deviation from center
    CENTER_WEIGHT = 0.1
    DIRECTION_WEIGHT = 0.1
    SPEED_WEIGHT = 3.0  # Significantly increased weight for speed
    PROGRESS_WEIGHT = 0.2
    CURVATURE_WEIGHT = 0.05
    WAYPOINT_WEIGHT = 0.1
    SMOOTHNESS_WEIGHT = 0.05
    HIGH_SPEED_BONUS = 4.0  # Increased bonus for maintaining high speed

    SPEED_MIN = 3.0  # Encourage faster minimum speed
    SPEED_MAX = 5.0  # Increase maximum speed to push limits

    reward = MIN_REWARD

    if all_wheels_on_track:
        # Reward for staying close to the center
        if distance_from_center <= FULL_REWARD_DISTANCE:
            reward += 1.0
        else:
            deviation_penalty = CENTER_WEIGHT * (distance_from_center / (track_width / 2))
            reward += max(1.0 - deviation_penalty, 0)

        # Reward for maintaining the correct direction
        next_waypoint = waypoints[closest_waypoints[1]]
        prev_waypoint = waypoints[closest_waypoints[0]]
        track_direction = math.degrees(math.atan2(
            next_waypoint[1] - prev_waypoint[1], 
            next_waypoint[0] - prev_waypoint[0]
        ))
        direction_diff = abs(heading - track_direction)
        if direction_diff > 180:
            direction_diff = 360 - direction_diff
        direction_penalty = DIRECTION_WEIGHT * (direction_diff / 180)
        reward += max(1.0 - direction_penalty, 0)

        # Reward for optimal speed
        if speed < SPEED_MIN:
            speed_penalty = SPEED_WEIGHT * (SPEED_MIN - speed) / SPEED_MIN
            reward -= speed_penalty
        elif speed > SPEED_MAX:
            speed_penalty = SPEED_WEIGHT * (speed - SPEED_MAX) / SPEED_MAX
            reward -= speed_penalty
        else:
            speed_reward = SPEED_WEIGHT * (speed / SPEED_MAX)
            reward += speed_reward
            # Bonus for maintaining high speed
            if speed >= SPEED_MAX * 0.8:
                reward += HIGH_SPEED_BONUS

        # Reward for progress
        reward += PROGRESS_WEIGHT * (progress / 100.0)

        # Penalize for excessive steering
        curvature_penalty = CURVATURE_WEIGHT * (abs(steering) / 30.0)
        reward -= curvature_penalty

        # Reward for being close to the next waypoint
        distance_to_next_waypoint = math.sqrt(
            (x - next_waypoint[0]) ** 2 + (y - next_waypoint[1]) ** 2
        )
        waypoint_reward = WAYPOINT_WEIGHT * max(1.0 - (distance_to_next_waypoint / track_width), 0)
        reward += waypoint_reward

        # Reward for smooth driving
        if abs(steering) < 5:
            reward += SMOOTHNESS_WEIGHT
    else:
        reward = MIN_REWARD

    return float(reward)
