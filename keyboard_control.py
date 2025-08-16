'''
Control drone flight via keyboard
'''
import sys
import time
import airsim
import pygame

# >------>>>  pygame settings   <<<------< #
pygame.init()                                         # Initialize pygame
screen = pygame.display.set_mode((160, 160))         # Set screen size
pygame.display.set_caption('keyboard control')       # Set window title
screen.fill((0, 0, 0))                               # Fill screen with black

# >------>>>  AirSim settings   <<<------< #
vehicle_name = "Drone"                         # Name of the drone to control (set in settings.json)
AirSim_client = airsim.MultirotorClient()      # Connect to AirSim
AirSim_client.confirmConnection()             # Verify connection and print status
AirSim_client.enableApiControl(True, vehicle_name=vehicle_name)   # Get control authority
AirSim_client.armDisarm(True, vehicle_name=vehicle_name)          # Arm the drone
AirSim_client.takeoffAsync(vehicle_name=vehicle_name).join()      # Take off     client.landAsync().join() to land

base_velocity = 2.0             # Base control speed (m/s)
speedup_ratio = 10.0           # Temporary speed boost multiplier
speedup_flag = False             # Flag for temporary speed boost
base_yaw_rate = 5.0             # Base yaw rate

while True:
    yaw_rate = 0.0
    velocity_x = 0.0
    velocity_y = 0.0
    velocity_z = 0.0

    time.sleep(0.02)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    scan_wrapper = pygame.key.get_pressed()

    # Press SPACE for 10x speed boost
    if scan_wrapper[pygame.K_SPACE]:
        scale_ratio = speedup_ratio
    else:
        scale_ratio = speedup_ratio / speedup_ratio

    # Set yaw rate based on 'A' and 'D' keys
    if scan_wrapper[pygame.K_a] or scan_wrapper[pygame.K_d]:
        yaw_rate = (scan_wrapper[pygame.K_d] - scan_wrapper[pygame.K_a]) * scale_ratio * base_yaw_rate

    # Set pitch axis velocity (NED frame, x is forward)
    if scan_wrapper[pygame.K_UP] or scan_wrapper[pygame.K_DOWN]:
        velocity_x = (scan_wrapper[pygame.K_UP] - scan_wrapper[pygame.K_DOWN]) * scale_ratio

    # Set roll axis velocity (NED frame, y is right)
    if scan_wrapper[pygame.K_LEFT] or scan_wrapper[pygame.K_RIGHT]:
        velocity_y = -(scan_wrapper[pygame.K_LEFT] - scan_wrapper[pygame.K_RIGHT]) * scale_ratio

    # Set z-axis velocity (NED frame, z up is negative)
    if scan_wrapper[pygame.K_w] or scan_wrapper[pygame.K_s]:
        velocity_z = -(scan_wrapper[pygame.K_w] - scan_wrapper[pygame.K_s]) * scale_ratio

    # print(f": Expectation gesture: {velocity_x}, {velocity_y}, {velocity_z}, {yaw_rate}")

    # Set velocity control and yaw control
    AirSim_client.moveByVelocityBodyFrameAsync(
        vx=velocity_x, vy=velocity_y, vz=velocity_z, duration=0.02,
        yaw_mode=airsim.YawMode(True, yaw_or_rate=yaw_rate), vehicle_name=vehicle_name)

    # Press 'Esc' to quit
    if scan_wrapper[pygame.K_ESCAPE]:
        pygame.quit()
        sys.exit()