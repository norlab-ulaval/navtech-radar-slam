import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration

def generate_launch_description():
    pkg_orora = get_package_share_directory('orora')
    pkg_sc_pgo = get_package_share_directory('sc_pgo')
    
    # Arguments
    seq_dir_arg = DeclareLaunchArgument(
        'seq_dir', default_value='/workspaces/navtech-radar-slam/data/red_2025-10-14-11-41', description='Sequence directory path'
    )
    do_slam_arg = DeclareLaunchArgument(
        'do_slam', default_value='true', description='Enable SLAM'
    )
    algorithm_arg = DeclareLaunchArgument(
        'algorithm', default_value='ORORA', description='Algorithm to use'
    )
    dataset_arg = DeclareLaunchArgument(
        "dataset", default_value="fomo", description="Dataset to use"
    )

    # Includes
    # Note: We assume the launch files are installed in the package share directory
    orora_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_orora, 'launch', 'run_orora.launch.py')
        ),
        launch_arguments={
            'seq_dir': LaunchConfiguration('seq_dir'),
            'do_slam': LaunchConfiguration('do_slam'),
            'algorithm': LaunchConfiguration('algorithm'),
            'dataset': LaunchConfiguration('dataset')
        }.items()
    )

    sc_pgo_launch = IncludeLaunchDescription(   
        PythonLaunchDescriptionSource(
            os.path.join(pkg_sc_pgo, 'launch', 'sc_pgo.launch.py')
        ),
        launch_arguments={
            'seq_dir': LaunchConfiguration('seq_dir'),
            'do_slam': LaunchConfiguration('do_slam'),
            'algorithm': LaunchConfiguration('algorithm'),
            'dataset': LaunchConfiguration('dataset')
        }.items()
    )

    return LaunchDescription([
        seq_dir_arg,
        do_slam_arg,
        algorithm_arg,
        dataset_arg,
        orora_launch,
        sc_pgo_launch
    ])
