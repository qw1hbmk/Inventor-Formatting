import readsource
import colorthreshold
import ivtemplate

#readsource should do everything, except write to a template. It should return stls, rgbs, everything as
#lists or files
#then colorthreshold will use just the rgb list (convert to hsl, manipulate) and return a new list of rgbs
#new function alayzecolor
#then ivtemplate will use either original rgbs or colorhtreshold rgbs and turn to iv viewer file



if __name__ == '__main__':

    xyz,rgb,face_indices = readsource.xyz_rgb_findices()
    #rgb = colorthreshold ...
    file_contents = ivtemplate.inventor_formatter(xyz,rgb,face_indices)
    
    open("inventor_femur_head3.iv","w").write(file_contents)
