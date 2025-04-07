from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import (DeclareLaunchArgument, SetEnvironmentVariable, 
                            IncludeLaunchDescription, SetLaunchConfiguration)
from launch.substitutions import PathJoinSubstitution, LaunchConfiguration, TextSubstitution
from launch_ros.actions import Node
from launch.launch_description_sources import PythonLaunchDescriptionSource

def generate_launch_description():
    pkg_ros_gz_sim = get_package_share_directory('ros_gz_sim')
    gz_launch_path = PathJoinSubstitution([pkg_ros_gz_sim, 'launch', 'gz_sim.launch.py'])
    gz_model_path = '/home/lqx/code/gazebox_try/model'

    GZ_SIM_RESOURCE_PATH=SetEnvironmentVariable('GZ_SIM_RESOURCE_PATH', gz_model_path)
    gz_sim_launch=IncludeLaunchDescription(
            PythonLaunchDescriptionSource(gz_launch_path),
            launch_arguments={
                'gz_args': ["/home/lqx/code/gazebox_try/moving_robot.sdf"],
                # 'on_exit_shutdown': 'True'
            }.items(),
        )
    gz_parameter_bridge=Node(
        package="ros_gz_bridge",
        executable="parameter_bridge",
        name="parameter_bridge",
        arguments=[
            "sensor/lidar@sensor_msgs/msg/LaserScan[gz.msgs.LaserScan",
            "/keyboard/keypress@std_msgs/msg/Int32@gz.msgs.Int32"
        ],
        output="screen",
    )
    return LaunchDescription([
        GZ_SIM_RESOURCE_PATH,
        gz_sim_launch,
        gz_parameter_bridge
    ])

