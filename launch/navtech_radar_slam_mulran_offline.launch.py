import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node

NAMESPACE = os.getenv("NAMESPACE")

def generate_launch_description():
    pkg_orora = get_package_share_directory('orora')
    pkg_sc_pgo = get_package_share_directory('sc_pgo')
    
    bag_file_arg = DeclareLaunchArgument(
        'bag_file', 
        description='Path to the ROS 2 bag file to process',
        default_value="/workspaces/navtech-radar-slam/data/red_2025-10-14-11-41/"
    )
    
    do_slam_arg = DeclareLaunchArgument(
        'do_slam', default_value='true', description='Enable SLAM'
    )
    algorithm_arg = DeclareLaunchArgument(
        'algorithm', default_value='ORORA', description='Algorithm to use'
    )
    dataset_arg = DeclareLaunchArgument(
        "dataset", default_value="mulran", description="Dataset to use"
    )

    # Configuration
    orora_params_file = os.path.join(pkg_orora, "config", "orora_params.yaml")
    
    orora_offline_node = Node(
        package="orora",
        executable="orora_offline",
        name="orora_offline",
        namespace=NAMESPACE,
        output="screen",
        arguments=[LaunchConfiguration('bag_file')],
        parameters=[
            orora_params_file,
            {
                "keypoint_extraction": "cen2018",
                "algorithm": LaunchConfiguration('algorithm'),
                "dataset": LaunchConfiguration('dataset'),
                "viz_extraction": False,
                "viz_matching": False,
                "frame_rate": 4.0,
            },
        ],
    )

    sc_pgo_launch = IncludeLaunchDescription(   
        PythonLaunchDescriptionSource(
            os.path.join(pkg_sc_pgo, 'launch', 'sc_pgo.launch.py')
        ),
        launch_arguments={
            "use_sim_time": "false", 
            "do_slam": LaunchConfiguration("do_slam"),
        }.items(),
    )

    return LaunchDescription([
        bag_file_arg,
        do_slam_arg,
        algorithm_arg,
        dataset_arg,
        orora_offline_node,
        sc_pgo_launch
    ])
