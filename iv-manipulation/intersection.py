
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

def rgbs_255thing(rgbs):
    
        return [[colour/255 for colour in rgb] for rgb in rgbs]


def stl_to_points(f):
    # "x1 y1 z1 x2 y2 z2 x3 y3 z3" -> [ [(x1, y1, z1), (x2, y2, z2), (x3, y3, z3)],... ]
    return [(lambda nums: [tuple(g) for g in [nums[:3], nums[3:6], nums[6:]]])([round(float(n),5) for n in line.split()]) for line in f.read().strip().split('\n')]


# def join_stl_rgb(stl_triplets, rgb_points, rgb_colors):
#     # [ [(x1, y1, z1), (x2, y2, z2), (x3, y3, z3)],... ], [(x, y, z),...], [(r, g, b),...] -> [(r, g, b),...]
#     match_stl_rgb = []
#     for triplet in stl_triplets:
        
#         rgbs = [rgb_colors[bisect_left(rgb_points,t)] for t in triplet]
#         grouped_rgb = zip(*rgbs)
#         average_colors = tuple(int(round(sum(color)/len(color))) for color in grouped_rgb)
#         match_stl_rgb.append(average_colors)
#     return match_stl_rgb
     
def stl_face_indices(stl_triplets, rgb_points):
    #[ [(x1, y1, z1), (x2, y2, z2), (x3, y3, z3)],... ], [(x, y, z),...],... -> [(0, 2, 3),...]

    match_stl_xyz = []
    for triplet in stl_triplets:
        xyz_triple = tuple(bisect_left(rgb_points,t) for t in triplet)
        match_stl_xyz.append(xyz_triple)

    return match_stl_xyz

def inventor_formatter(points, face_rgbs, face_indices):
    template =\
"""#Inventor V2.0 ascii

Separator
{{
Coordinate3
{{
point [
{points}
]
}}
Material
{{
diffuseColor [ {face_rgbs} ]
}}
MaterialBinding
{{
value PER_VERTEX_INDEXED
}}
IndexedTriangleStripSet {{
coordIndex [
{face_indices}
]
}}

}}"""
    points_formatted = "\n".join(" ".join(str(coord) for coord in xyz) + "," for xyz in points)
    face_rgbs_formatted = ",\n ".join(" ".join(str(component) for component in rgb) for rgb in face_rgbs)
    face_indices_formatted = "\n".join(", ".join(str(ind) for ind in indices) + ", -1," for indices in face_indices)

    return template.format(points=points_formatted,face_rgbs=face_rgbs_formatted,face_indices=face_indices_formatted)

def hsv2rgb(h, s, v):
    h = float(h)
    s = float(s)
    v = float(v)
    h60 = h / 60.0
    h60f = math.floor(h60)
    hi = int(h60f) % 6
    f = h60 - h60f
    p = v * (1 - s)
    q = v * (1 - f * s)
    t = v * (1 - (1 - f) * s)
    r, g, b = 0, 0, 0
    if hi == 0: r, g, b = v, t, p
    elif hi == 1: r, g, b = q, v, p
    elif hi == 2: r, g, b = p, v, t
    elif hi == 3: r, g, b = p, q, v
    elif hi == 4: r, g, b = t, p, v
    elif hi == 5: r, g, b = v, p, q
    r, g, b = int(r * 255), int(g * 255), int(b * 255)
    return r, g, b
    
def rgb2hsv(r, g, b):
    r, g, b = r/255.0, g/255.0, b/255.0
    mx = max(r, g, b)
    mn = min(r, g, b)
    df = mx-mn
    if mx == mn:
        h = 0
    elif mx == r:
        h = (60 * ((g-b)/df) + 360) % 360
    elif mx == g:
        h = (60 * ((b-r)/df) + 120) % 360
    elif mx == b:
        h = (60 * ((r-g)/df) + 240) % 360
    if mx == 0:
        s = 0
    else:
        s = df/mx
    v = mx
    return h, s, v


if __name__ == '__main__':
    # open files and stuff
    rgbxyz_file = open('head_xyzrgb.txt')
    decoded_stl_file = open('stl_triplet_coords_array.txt')

    xyz,rgb = split_xyzrgb(xyzrgb_to_points(rgbxyz_file))
    stl_points = stl_to_points(decoded_stl_file)
    # face_rgbs =  join_stl_rgb(stl_points,xyz,rgb)
    face_indices = stl_face_indices(stl_points,xyz)

    file_contents = inventor_formatter(xyz, rgb, face_indices)

    open("inventor_femur_head3.iv","w").write(file_contents)




# def unroll_stl_triples(triples):
#     # [ [(x1, y1, z1), (x2, y2, z2), (x3, y3, z3)],... ] -> [(x1, y1, z1), (x2, y2, z2)...]
#     unrolled_triples = []
#     for triple in triples:
#         for vertex in triple:
#             unrolled_triples.append(vertex)
#     print('stl verticies: {}'.format(len(unrolled_triples)))
#     return unrolled_triples


# def check_if_all_xyzrgb_in_stl(xpoints, spoints):
#     print('sanity check')
#     print 'distinct xpoints:', len(set(xpoints))
#     print(spoints[:3])
#     #excluded_vertices = set(xpoints).difference(set(spoints))
#     excluded_vertices = set(spoints).difference(set(xpoints))

#     if len(excluded_vertices) > 0:
#         print('we have something :|')
#         print(len(excluded_vertices))
#     else:
#         print('whatevs')
