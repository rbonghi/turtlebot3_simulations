# Copyright 2022 Open Source Robotics Foundation, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, RegisterEventHandler
from launch.event_handlers import OnProcessExit
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch.actions import ExecuteProcess
from launch_ros.actions import Node

TURTLEBOT3_MODEL = os.environ['TURTLEBOT3_MODEL']

def generate_launch_description():
    load_joint_state_controller = ExecuteProcess(
        cmd=['ros2', 'control', 'load_controller', '-c', '/controller_manager', '--set-state', 'start',
             'joint_state_broadcaster'],
        output='screen'
    )

    load_joint_trajectory_controller = ExecuteProcess(
        cmd=['ros2', 'control', 'load_controller', '-c', '/controller_manager', '--set-state', 'start',
             'diff_drive_base_controller'],
        output='screen'
    )

    # Ensure diffdrive_controller_node starts after load_joint_state_controller
    diff_drive_base_controller_callback = RegisterEventHandler(
        event_handler=OnProcessExit(
            target_action=load_joint_state_controller,
            on_exit=[load_joint_trajectory_controller],
        )
    )

    return LaunchDescription([
        load_joint_state_controller,
        diff_drive_base_controller_callback
    ])
