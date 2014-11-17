from bisect import bisect_left


def xyzrgb_to_points(f):
    # "x y z r g b\n..." -> [(x, y, z, r, g, b),...]
    points = [tuple(round(float(n),5) for n in line.split()) for line in f.read().strip().split('\n')]
    print('length of xyzrgb points: {}'.format(len(points)))
    return points

def split_xyzrgb(points_and_colors):
    # [(x, y, z, r, g, b),...] -> [(x, y, z),...], [(r/255, g/255, b/255),....] 


    # [(x, y, z, r, g, b),...] -> [(x, y, z),...], [(r, g, b),....] 
    xyzs, rgbs = zip(*[[v[:3],v[3:]] for v in sorted(points_and_colors)])
    return xyzs, rgbs

def stl_to_points(f):
    # "x1 y1 z1 x2 y2 z2 x3 y3 z3" -> [ [(x1, y1, z1), (x2, y2, z2), (x3, y3, z3)],... ]
    return [(lambda nums: [tuple(g) for g in [nums[:3], nums[3:6], nums[6:]]])([round(float(n),5) for n in line.split()]) for line in f.read().strip().split('\n')]

def stl_face_indices(stl_triplets, rgb_points):
    #[ [(x1, y1, z1), (x2, y2, z2), (x3, y3, z3)],... ], [(x, y, z),...],... -> [(0, 2, 3),...]

    match_stl_xyz = []
    for triplet in stl_triplets:
        xyz_triple = tuple(bisect_left(rgb_points,t) for t in triplet)
        match_stl_xyz.append(xyz_triple)
    return match_stl_xyz

def xyz_rgb_findices():
    # open files and stuff
	rgbxyz_file = open('../head_xyzrgb.txt')
	decoded_stl_file = open('../stl_triplet_coords_array.txt')

	xyz,rgb = split_xyzrgb(xyzrgb_to_points(rgbxyz_file))
	stl_points = stl_to_points(decoded_stl_file)
	face_indices = stl_face_indices(stl_points,xyz)
	return xyz,rgb,face_indices