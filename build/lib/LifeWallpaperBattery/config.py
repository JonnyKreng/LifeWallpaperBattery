#a path can be absolut or relative
#can be empty, than tranparent background is chosen
background = '' 
#can't be empty, make shure i has an trasparent background! Or it will really be ugly
battery = 'image.png'
#Size multipliyer of Battery image
size = 1

#Try it out min 0 max 255, only where alptha < maskfilter the pictures are combiend
maskfilter = 200

 #time between updates in s
frametime = 60

#True uses gradiants from green to red, False uses colorlist down below
unsimingly = True
#(percent, (r,g,b)) can be expanded(should keeped sorted, hight percentage to low)
colorlist = [(90,(0,255,0)),(80,(255,0,0)),(10,(0,0,255))] 

outputpath = 'out_image.png'
 #Monitor name to get size from optional if background is empty
name = ''