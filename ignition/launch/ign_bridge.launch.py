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

	namespace = ''
	use_sim_time = LaunchConfiguration('use_sim_time')
	robot_name = 'RMP'
	ign_model_prefix = '/model/' + robot_name

	# clock bridge
	clock_bridge = Node(package='ros_gz_bridge', executable='parameter_bridge',
			namespace=namespace,
			name='clock_bridge',
			output='screen',
			arguments=['/clock' + '@rosgraph_msgs/msg/Clock' + '[ignition.msgs.Clock'],
			condition=IfCondition(use_sim_time)
			)

	# cmd_vel bridge 
	cmd_vel_bridge = Node(package='ros_gz_bridge', executable='parameter_bridge',
			namespace = namespace,
			name = 'cmd_vel_bridge',
			output='screen',
			parameters=[{
				'use_sim_time': use_sim_time
			}],
			arguments = [
				'/cmd_vel' + '@geometry_msgs/msg/Twist' + ']ignition.msgs.Twist'
			])
			
	# color camera bridge 
	color_camera_bridge = Node(
			package='ros_gz_bridge', 
			executable='parameter_bridge',
			namespace = namespace,
			name = 'color_camera_bridge',
			output='screen',
			parameters=[{
				'use_sim_time': use_sim_time
			}],
			arguments = [
				 '/color_camera' + '@sensor_msgs/msg/Image' + '[ignition.msgs.Image'
			],
			remappings = [
				('/color_camera', '/color_camera')
			])

	# depth camera bridge 
	depth_camera_bridge = Node(
			package='ros_gz_bridge', 
			executable='parameter_bridge',
			namespace = namespace,
			name = 'depth_camera_bridge',
			output='screen',
			parameters=[{
				'use_sim_time': use_sim_time
			}],
			arguments = [
				'/depth_camera' + '@sensor_msgs/msg/Image' + '[ignition.msgs.Image',
				'/depth_camera/points' + '@sensor_msgs/msg/PointCloud2' + '[ignition.msgs.PointCloudPacked',
				'/camera_info' + '@sensor_msgs/msg/CameraInfo'+ '[ignition.msgs.CameraInfo'
			],
			remappings = [
				('/depth_camera', '/depth_camera'),
				('/camera_info', '/camera_info')])
			
	# IMU bridge 
	imu_bridge = Node(package='ros_gz_bridge', executable='parameter_bridge',
			namespace = namespace,
			name = 'imu_bridge',
			output='screen',
			parameters=[{
				'use_sim_time': use_sim_time
			}],
			arguments = [
				 '/imu' + '@sensor_msgs/msg/Imu' + '[ignition.msgs.IMU'
			])
	
	# odom bridge 
	odom_bridge = Node(package='ros_gz_bridge', executable='parameter_bridge',
			namespace = namespace,
			name = 'odometry_bridge',
			output='screen',
			parameters=[{'use_sim_time': use_sim_time}],
			arguments = [
				 '/odom' + '@nav_msgs/msg/Odometry' + '[ignition.msgs.Odometry'
			])

			
	# odom to base_link transform bridge
	odom_base_tf_bridge = Node(package='ros_gz_bridge', executable='parameter_bridge',
			namespace = namespace,
			name = 'odom_base_tf_bridge',
			output = 'screen',
			parameters=[{'use_sim_time': use_sim_time}],
			arguments = [
				'/tf' + '@tf2_msgs/msg/TFMessage' + '[ignition.msgs.Pose_V'
			])
			
	# joint states bridge 
	joint_states_bridge = Node(package='ros_gz_bridge', executable='parameter_bridge',
			namespace = namespace,
			name = 'joint_states_bridge',
			output='screen',
			parameters=[{'use_sim_time': use_sim_time}],
			arguments = [
				'/joint_states' + '@sensor_msgs/msg/JointState' + '[ignition.msgs.Model'
			])


	return LaunchDescription([
        DeclareLaunchArgument('use_sim_time', default_value=['false'],
                            description='use sim time from /clock'),
			clock_bridge,
			cmd_vel_bridge,
			color_camera_bridge,
			depth_camera_bridge,
			imu_bridge,
			odom_bridge,
			odom_base_tf_bridge,
			joint_states_bridge
	])
