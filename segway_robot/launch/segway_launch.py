import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.conditions import IfCondition
from launch.substitutions import LaunchConfiguration

def generate_launch_description():
    # Path to URDF (I already copied it from igt_ignition to segway)
    pkg_segway = get_package_share_directory('segway')
    urdf_path = os.path.join(pkg_segway, 'model', 'robot.urdf')
    
    with open(urdf_path, 'r') as infp:
        robot_desc = infp.read()

    start_rviz_arg = DeclareLaunchArgument(
        'rviz',
        default_value='false',
        description='Open RViz2 if set to true'
    )

    rviz = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        output='screen',
        condition=IfCondition(LaunchConfiguration('rviz')) # Only runs if rviz:=true
    )
    
    return LaunchDescription([
        start_rviz_arg,
        rviz,
        # robot_state_publisher
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            name='robot_state_publisher',
            output='screen',
            parameters=[{
                'robot_description': robot_desc,
                'use_sim_time': False # ALWAYS False for real hardware
            }]
        ),

        # depthimage_to_laserscan
        Node(
            package='depthimage_to_laserscan',
            executable='depthimage_to_laserscan_node',
            name='depthimage_to_laserscan',
            remappings=[
                ('depth', '/camera/camera/depth/image_rect_raw'),
                ('depth_camera_info', '/camera/camera/depth/camera_info'),
                ('scan', '/scan')
            ],
            parameters=[{
                'scan_time': 0.1,
                'range_min': 0.1,
                'range_max': 10.0,
                'output_frame': 'camera_link' # Match with URDF camera frame
            }]
        )

    ])
