FROM --platform=linux/amd64 ros:humble-ros-base

# Install standard development tools
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    git \
    wget \
    curl \
    vim \
    gdb \
    clang \
    clang-format \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

# Install PCL and other specific dependencies if not included in desktop
RUN apt-get update && apt-get install -y \
    libpcl-dev \
    libopencv-dev \
    libceres-dev \
    libgoogle-glog-dev \
    libboost-all-dev \
    ros-humble-pcl-conversions \
    ros-humble-tf2-eigen \
    ros-humble-rosbag2-storage-mcap \
    ros-humble-cv-bridge \
    ros-humble-image-transport \
    && rm -rf /var/lib/apt/lists/*

RUN cd /opt && git clone https://github.com/borglab/gtsam.git -b 4.2 \
    && cd gtsam \
    && mkdir build \
    && cd build \
    && cmake .. \
    && make install

# Setup user (optional but recommended for dev containers to avoid root issues)
ARG USERNAME=vscode
ARG USER_UID=1000
ARG USER_GID=$USER_UID

RUN groupadd --gid $USER_GID $USERNAME \
    && useradd --uid $USER_UID --gid $USER_GID -m $USERNAME \
    && echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME \
    && chmod 0440 /etc/sudoers.d/$USERNAME

USER $USERNAME
ENV SHELL /bin/bash
