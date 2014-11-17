
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
    face_rgbs_formatted = ",\n ".join(" ".join(str(component/255) for component in rgb) for rgb in face_rgbs)
    #face_rgbs_formatted = ",\n ".join(" ".join(str(component) for component in rgb) for rgb in face_rgbs)
    face_indices_formatted = "\n".join(", ".join(str(ind) for ind in indices) + ", -1," for indices in face_indices)

    return template.format(points=points_formatted,face_rgbs=face_rgbs_formatted,face_indices=face_indices_formatted)

