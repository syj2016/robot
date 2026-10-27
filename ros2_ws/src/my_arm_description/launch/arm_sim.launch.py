import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, Command
from launch_ros.actions import Node


def generate_launch_description():
    pkg_dir = get_package_share_directory("my_arm_description")
    pkg_ros_gz_sim = get_package_share_directory("ros_gz_sim")

    urdf_path = os.path.join(pkg_dir, "urdf", "arm.urdf")

    use_sim_time = LaunchConfiguration("use_sim_time")
    use_composition = LaunchConfiguration("use_composition")
    create_own_container = LaunchConfiguration("create_own_container")

    # 1. robot_state_publisher，发布URDF和TF
    robot_state_publisher = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        output="screen",
        parameters=[
            {"robot_description": Command(["cat ", urdf_path])},
            {"use_sim_time": use_sim_time}
        ]
    )


    sdf_args = os.path.join(pkg_dir,"sdf","my_world.sdf")


    # 2. Jazzy标准方式：引入ros_gz_sim自带gz_sim.launch.py，支持composition两个参数
    gz_sim = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_ros_gz_sim, "launch", "gz_sim.launch.py")
        ),
        launch_arguments={
            "gz_args": sdf_args,
            "use_composition": use_composition,
            "create_own_container": create_own_container,
        }.items()
    )

    # 3. Spawn模型进Gazebo（保持你原来写法）
    spawn_model = Node(
        package="ros_gz_sim",
        executable="create",
        arguments=[
            "-topic", "/robot_description",
            "-name", "two_link_arm",
            "-x", "0", "-y", "0", "-z", "0.5"
        ],
        output="screen"
    )




    # 4. ros_gz_bridge：相机图像桥接
    bridge = Node(
        package="ros_gz_bridge",
        executable="parameter_bridge",
        arguments=[
            "/arm_camera@sensor_msgs/msg/Image@gz.msgs.Image",
        ],
        output="screen"
    )

    return LaunchDescription([
        DeclareLaunchArgument("use_sim_time", default_value="true"),
        DeclareLaunchArgument("use_composition", default_value="true"),
        DeclareLaunchArgument("create_own_container", default_value="true"),
        robot_state_publisher,
        gz_sim,
        spawn_model,
        bridge
    ])
