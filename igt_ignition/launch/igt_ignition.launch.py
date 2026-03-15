import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.actions import IncludeLaunchDescription
from launch.conditions import IfCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node

def generate_launch_description():

	pkg_ros_ign_gazebo = get_package_share_directory('ros_ign_gazebo')
	pkg_igt_ignition = get_package_share_directory('igt_ignition')
	urdf_path = pkg_igt_ignition + '/models/RobotRMP/model.urdf'
	
	use_sim_time = LaunchConfiguration('use_sim_time')
	
	pkg_nav2_bringup = get_package_share_directory('nav2_bringup')
	rviz_config_file = LaunchConfiguration('rviz_config', default=os.path.join(pkg_nav2_bringup, 'rviz', 'nav2_default_view.rviz'))
						
	# Gazebo launch
	gazebo = IncludeLaunchDescription(
		PythonLaunchDescriptionSource(
		    os.path.join(pkg_ros_ign_gazebo, 'launch', 'ign_gazebo.launch.py'),
		),
	)

	# launch ign_bridge
	ign_bridge = IncludeLaunchDescription(
		PythonLaunchDescriptionSource(
		    os.path.join(pkg_igt_ignition, 'launch', 'ign_bridge.launch.py'),
		),
        launch_arguments={
            'use_sim_time': use_sim_time}.items(),
		condition = IfCondition(LaunchConfiguration('with_bridge'))
	)
				
	# spawn_sdf node
	spawn_sdf = Node(package='ros_ign_gazebo', 
				executable='create',
				arguments=['-name', 'RMP',
					'-x', '0.0',
		        		'-y', '0.0',
					'-z', '0.0',
					'-Y', '-1.57',
					'-file', os.path.join(pkg_igt_ignition, 'models', 'RobotRMP', 'model.sdf')],
				output='screen')


	# robot_state_publisher node
	robot_state_publisher = Node(
				package='robot_state_publisher',
				executable='robot_state_publisher',
				output='screen',
				parameters = [
					{'ignore_timestamp': False},
                                        {'use_sim_time': use_sim_time},
					{'use_tf_static': True},
					{'robot_description': open(urdf_path).read()}],
				arguments = [urdf_path])
    
	
	# depthimage_to_laserscan node
	depthimage_to_laserscan = Node(
		    package='depthimage_to_laserscan',
		    executable='depthimage_to_laserscan_node',
		    name='depthimage_to_laserscan',
		    output='screen',
		    remappings=[
			('depth', '/depth_camera'),
			('depth_camera_info', '/camera_info')
		    ],
		    parameters=[
			os.path.join( get_package_share_directory('depthimage_to_laserscan'), 'cfg','param.yaml'),
			{'use_sim_time': use_sim_time},
			{'scan_time': 0.1},
			{'range_min': 0.1},
			{'range_max': 10},
			{'output_frame': 'base_link'}]
		)

        
        #launch rviz2
	rviz2 = Node(package='rviz2', executable='rviz2',
					name='rviz2',
					arguments=['-d', rviz_config_file],
					parameters=[{'use_sim_time': use_sim_time}],
					output='screen')
        
	return LaunchDescription([
		DeclareLaunchArgument(
		  'ign_args', default_value=[os.path.join(pkg_igt_ignition, 'worlds', 'lab.sdf') +
					 ' -v 2 --gui-config ' +
					 os.path.join(pkg_igt_ignition, 'ign', 'gui.config'), ''],
		  description='Ignition Gazebo arguments'),
		DeclareLaunchArgument('with_bridge', default_value=['true']),
        	DeclareLaunchArgument('use_sim_time', default_value=['true']),
		gazebo,
		spawn_sdf,
		ign_bridge,
		robot_state_publisher,
		depthimage_to_laserscan,
		rviz2
	])

