# Segway RMP 401 PPLUS chassis

## Installation
  * Ignition Gazebo
  * ros2-humble
  * [slam_toolbox](https://github.com/SteveMacenski/slam_toolbox)
  * [navstack2](https://navigation.ros.org/build_instructions/index.html)
  
* Create a workspace

```bash

mkdir -p colcon_ws/src && cd colcon_ws/src
```

  * Clone the repo
  * Build the workspace & source the setup 
 
```bash
colcon build --symlink-install

source install/setup.bash
```
## Launch

>Ign-Gazebo

```bash
ros2 launch igt_ignition igt_ignition.launch.py
```

<img src="./images/igt_gazebo.png" width=800/>
<img src="./images/ign_gazebo_image_display.png" width=800/>

### Launch with <code>ros_ign_bridge</code> for teleop

```bash
ros2 launch igt_ignition igt_ignition.launch.py

```

Make sure you start simulation physics by clicking "play" button in bottom left corner of ignition

and then open another terminal and run
```bash
ros2 run teleop_twist_keyboard teleop_twist_keyboard
```

### Move robot by publishing velocities

```bash
ign topic -t "/model/RMP/cmd_vel" -m ignition.msgs.Twist -p "linear: {x: 2.0}, angular: {z: 0.0}"
```

### Subscribe to topics

```bash
ign topic -t "/RMP/scan" -e
```
```bash
ign topic -t "/model/RMP/odom" -e
```
# Navigation

### Mapping with Slam Toolbox
 * Open another terminal and launch slam_toolbox for mapping and rviz2 using `online_sync_launch.py`:
   ```bash
   ros2 launch igt_nav online_sync_launch.py
   ```
 * Open another terminal and run the ros2 `teleop_twist_keyboard` node using:
   ```bash
   ros2 run teleop_twist_keyboard teleop_twist_keyboard
   ```
 * Use teleop to control the bot and map the world (as shown in the gif below). Save the map using:
   ```bash
   ros2 run nav2_map_server map_saver_cli -f name_of_map_file
   ```
   <img src="./images/mapping.gif" />

### Navigation2
 * Open another terminal and launch navigation2 using `navigation2.launch.py` launch file:
   ```bash
   ros2 launch igt_nav navigation2.launch.py
   ```
   This launches the `bringup.launch.py` launch file from `nav2_bringup` package and `map/lab_map.yaml` and `config/nav2.yaml` from igt_nav package as map and params_file. It also start rviz2 for visualization.
 * In rviz2, use `2D Pose Estimate` to provide initial pose of the bot to amcl so that it can start publishing the robot's pose & `map->odom tf`.
 * Rviz2 window will start updating with estimated robot pose from amcl as well as updated global and local costmap. Use the `2D Goal Pose` in rviz2 to provide the bot with a goal pose to start navigation. (shown below in gif) <br> <br>
   <img src="./images/navigation2.gif"/>
