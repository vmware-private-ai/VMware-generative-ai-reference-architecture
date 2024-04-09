# Installing NVIDIA Container Toolkit with Apt
# 1. Configure the repository:
curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg \
  && curl -s -L https://nvidia.github.io/libnvidia-container/stable/deb/nvidia-container-toolkit.list | \
    sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' | \
    sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list \
  && \
    sudo apt-get update
 
# 2. Install the NVIDIA Container Toolkit packages:
sudo apt-get install -y nvidia-container-toolkit


####################

# Configuring NVIDIA Container Toolkit with Docker
# 1. Configure the container runtime by using the nvidia-ctk command:
# The nvidia-ctk command modifies the /etc/docker/daemon.json file on the host. The file is updated so that Docker can use the NVIDIA Container Runtime.
sudo nvidia-ctk runtime configure --runtime=docker
 
 
# 2. Restart the Docker daemon:
sudo systemctl restart docker