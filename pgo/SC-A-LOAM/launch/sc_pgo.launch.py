from launch import LaunchDescription
import os

from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument
from launch.conditions import IfCondition
from launch.substitutions import LaunchConfiguration

NAMESPACE = os.getenv("NAMESPACE")
STORAGE_PATH = os.getenv("STORAGE_PATH", "/tmp")

def generate_launch_description():
    sim_time_arg = DeclareLaunchArgument(
        "use_sim_time", default_value="true", description="Use sim time"
    )
    do_slam_arg = DeclareLaunchArgument(
        "do_slam", default_value="false", description="Enable SLAM mode"
    )

    sc_pgo_node = Node(
        package='sc_pgo',
        executable='alaserPGO',
        namespace=NAMESPACE,
        name='loop_closure',
        output='screen',
        sigterm_timeout="120",  # Wait 120 seconds before escalating to SIGTERM
        sigkill_timeout="10",  # Wait 5 more seconds before SIGKILL
        parameters=[{
            'keyframe_meter_gap': 2.0,
            'keyframe_deg_gap': 10.0,
            'odom_noise_score': 0.1,
            'loop_noise_score': 3.0,
            'loop_fitness_score_threshold': 0.3,
            'sc_dist_thres': 0.45,
            'pcd_save_dir': STORAGE_PATH,
            "use_sim_time": LaunchConfiguration("use_sim_time"),
        }],
        condition=IfCondition(LaunchConfiguration("do_slam")),
    )

    return LaunchDescription([
        sim_time_arg, do_slam_arg, sc_pgo_node
    ])
