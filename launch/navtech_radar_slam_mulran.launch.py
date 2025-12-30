import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration

def generate_launch_description():
    pkg_orora = get_package_share_directory('orora')
    pkg_sc_pgo = get_package_share_directory('sc_pgo')
    
    do_slam_arg = DeclareLaunchArgument(
        'do_slam', default_value='true', description='Enable SLAM'
    )
    algorithm_arg = DeclareLaunchArgument(
        'algorithm', default_value='ORORA', description='Algorithm to use'
    )
    dataset_arg = DeclareLaunchArgument(
        "dataset", default_value="fomo", description="Dataset to use"
    )
    sim_time_arg = DeclareLaunchArgument(
        "use_sim_time", default_value="true", description="Use sim time"
    )

    # Includes
    # Note: We assume the launch files are installed in the package share directory
    orora_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_orora, 'launch', 'run_orora.launch.py')
        ),
        launch_arguments={
            'algorithm': LaunchConfiguration('algorithm'),
            'dataset': LaunchConfiguration('dataset'),
            "use_sim_time": LaunchConfiguration("use_sim_time")
        }.items()
    )

    sc_pgo_launch = IncludeLaunchDescription(   
        PythonLaunchDescriptionSource(
            os.path.join(pkg_sc_pgo, 'launch', 'sc_pgo.launch.py')
        ),
        launch_arguments={
            "use_sim_time": LaunchConfiguration("use_sim_time"),
            "do_slam": LaunchConfiguration("do_slam"),
        }.items(),
    )

    return LaunchDescription([
        do_slam_arg,
        sim_time_arg,
        algorithm_arg,
        dataset_arg,
        orora_launch,
        sc_pgo_launch
    ])
