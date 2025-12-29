from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    sc_pgo_node = Node(
        package='sc_pgo',
        executable='alaserPGO',
        name='alaserPGO',
        output='screen',
        sigterm_timeout="120",  # Wait 120 seconds before escalating to SIGTERM
        sigkill_timeout="10",  # Wait 5 more seconds before SIGKILL
        parameters=[{
            'keyframe_meter_gap': 0.2,
            'sc_dist_thres': 0.45
        }],
        remappings=[
            ('/velodyne_cloud_registered_local', '/orora/cloud_local'),
            ('/aft_mapped_to_init', '/orora/odom')
        ]
    )

    return LaunchDescription([
        sc_pgo_node
    ])
