#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from geometry_msgs.msg import Twist
import numpy as np
import cv2
from cv_bridge import CvBridge

class ObstacleAvoider(Node):
    def __init__(self):
        super().__init__('obstacle_avoider')

        self.bridge = CvBridge()

        # Subscription to the depth image topic
        self.sub = self.create_subscription(
            Image,
            '/camera/camera/depth/image_rect_raw',
            self.callback,
            10)

        # Publisher for velocity commands
        self.pub = self.create_publisher(Twist, '/cmd_vel', 10)

    def callback(self, msg):
        try:
            # Convert ROS Image message to OpenCV format (16-bit unsigned)
            depth = self.bridge.imgmsg_to_cv2(msg, desired_encoding='passthrough')

            # Crop to the center region of the image
            h, w = depth.shape
            center = depth[h//3:2*h//3, w//3:2*w//3]

            # Filter out 0 (invalid/noise) and non-finite values
            mask = (center > 0) & (np.isfinite(center))
            valid_depths = center[mask]

            cmd = Twist()

            if len(valid_depths) == 0:
                # If no valid data is found, stop the robot for safety
                cmd.linear.x = 0.0
                cmd.angular.z = 0.0
            else:
                # Convert from millimeters to meters
                min_dist_m = np.min(valid_depths) / 1000.0

                # Obstacle avoidance logic
                if min_dist_m < 0.6:
                    self.get_logger().info(f"Obstacle at {min_dist_m:.2f}m! Turning.")
                    cmd.linear.x = 0.1
                    cmd.angular.z = 0.6 # Rotate
                else:
               	    self.get_logger().info(f"Path clear! Moving forward.")
                    cmd.linear.x = 0.1  # Move forward
                    cmd.angular.z = 0.0

            self.pub.publish(cmd)

        except Exception as e:
            self.get_logger().error(f"Callback failed: {str(e)}")

def main(args=None):
    rclpy.init(args=args)
    node = ObstacleAvoider()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
