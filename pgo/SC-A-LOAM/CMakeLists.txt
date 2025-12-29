cmake_minimum_required(VERSION 3.5)
project(sc_pgo)

# Default to C++17
if(NOT CMAKE_CXX_STANDARD)
  set(CMAKE_CXX_STANDARD 17)
endif()

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(std_msgs REQUIRED)
find_package(geometry_msgs REQUIRED)
find_package(nav_msgs REQUIRED)
find_package(sensor_msgs REQUIRED)
find_package(tf2 REQUIRED)
find_package(tf2_ros REQUIRED)
find_package(tf2_geometry_msgs REQUIRED)
find_package(image_transport REQUIRED)
find_package(cv_bridge REQUIRED)
find_package(pcl_conversions REQUIRED)

find_package(PCL REQUIRED)
find_package(OpenCV REQUIRED)
find_package(OpenMP REQUIRED)
find_package(GTSAM REQUIRED QUIET)

include_directories(
  include
  ${PCL_INCLUDE_DIRS}
  ${OpenCV_INCLUDE_DIRS}
  ${GTSAM_INCLUDE_DIR}
)

add_executable(alaserPGO 
  src/laserPosegraphOptimization.cpp
  include/scancontext/Scancontext.cpp
)

ament_target_dependencies(alaserPGO
  rclcpp
  std_msgs
  geometry_msgs
  nav_msgs
  sensor_msgs
  tf2
  tf2_ros
  tf2_geometry_msgs
  image_transport
  cv_bridge
  pcl_conversions
)

target_link_libraries(alaserPGO
  ${PCL_LIBRARIES}
  ${OpenCV_LIBRARIES}
  ${OpenMP_CXX_FLAGS}
  gtsam
)

# OpenMP
if(OpenMP_CXX_FOUND)
    target_link_libraries(alaserPGO OpenMP::OpenMP_CXX)
endif()


install(TARGETS
  alaserPGO
  DESTINATION lib/${PROJECT_NAME}
)

install(DIRECTORY include/
  DESTINATION include/${PROJECT_NAME}
)

# Install launch files if any (none yet seen)
install(DIRECTORY launch
  DESTINATION share/${PROJECT_NAME}
)

ament_package()



