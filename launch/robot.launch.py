import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():

    pkg_igt_ignition = get_package_share_directory('igt_ignition')
    urdf_path = os.path.join(pkg_igt_ignition, 'models', 'RobotRMP', 'model.urdf')

    use_sim_time = LaunchConfiguration('use_sim_time')

    pkg_nav2_bringup = get_package_share_directory('nav2_bringup')
    rviz_config_file = os.path.join(pkg_nav2_bringup, 'rviz', 'nav2_default_view.rviz')

    # Robot state publisher (publishes TF tree from URDF)
    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='screen',
        parameters=[
            {'use_sim_time': use_sim_time},
            {'robot_description': open(urdf_path).read()}
        ]
    )

    # Convert depth camera to LaserScan
    depthimage_to_laserscan = Node(
        package='depthimage_to_laserscan',
        executable='depthimage_to_laserscan_node',
        name='depthimage_to_laserscan',
        output='screen',
        remappings=[
            ('depth', '/camera/camera/depth/image_rect_raw'),
            ('depth_camera_info', '/camera/camera/depth/camera_info'),
            ('scan', '/scan')
        ],
        parameters=[
            {'scan_time': 0.1},
            {'range_min': 0.1},
            {'range_max': 10.0},
            {'output_frame': 'base_link'}
        ]
    )

    # RViz visualization
    rviz2 = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        arguments=['-d', rviz_config_file],
        parameters=[{'use_sim_time': use_sim_time}],
        output='screen'
    )

    return LaunchDescription([

        DeclareLaunchArgument(
            'use_sim_time',
            default_value='false'
        ),

        robot_state_publisher,
        depthimage_to_laserscan,
        rviz2
    ])


