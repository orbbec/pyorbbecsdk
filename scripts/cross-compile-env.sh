# Define the target directory and Ubuntu version
mkdir -p ../cc-env/sysroot
SYSROOT_DIR="../cc-env/sysroot/ubuntu-16.04"
UBUNTU_VERSION="xenial"  # Ubuntu 16.04 codename

# Use debootstrap to create the sysroot
sudo debootstrap --arch amd64 ${UBUNTU_VERSION} ${SYSROOT_DIR} http://archive.ubuntu.com/ubuntu/
