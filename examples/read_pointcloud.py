import sys

try:
    import open3d as o3d
except ImportError:
    print("Please install open3d-python first.")
    print("You can install it by pip install open3d")
    print("See: http://www.open3d.org/docs/release/getting_started.html")
    sys.exit(-1)


def main():
    filename = sys.argv[1]
    # read ply file
    pcd = o3d.io.read_point_cloud(filename)
    # visualize point cloud
    o3d.visualization.draw_geometries([pcd])


if __name__ == "__main__":
    main()
