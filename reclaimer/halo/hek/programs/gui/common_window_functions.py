#these are just constants to illustrate what's going on
x_pos_idx = 1
y_pos_idx = 2


#this function will allow the supplied child windows to move with the supplied parent window
def dock_window_movement(parent_window, child_windows):
    parent_window.window_docking_updating = True
    
    #the .geometry() returns the dimensions as a string that looks like
    #"widthxheight+posx+posy". an example would be "200x200+50+50".
    #Because of that we need to split them apart at the x and +
    root_dim = parent_window.geometry().split('+')
    
    #we want to move the child windows with the main, but keep their relative position to the main
    if ((int(root_dim[x_pos_idx]) != parent_window.prev_pos_x) or
        (int(root_dim[y_pos_idx]) != parent_window.prev_pos_y)):
        
        #get the amount that the main window has been moved
        root_x_shift = (int(root_dim[x_pos_idx]) - parent_window.prev_pos_x)
        root_y_shift = (int(root_dim[y_pos_idx]) - parent_window.prev_pos_y)

        #set the new parent window's location
        parent_window.prev_pos_x = int(root_dim[x_pos_idx])
        parent_window.prev_pos_y = int(root_dim[y_pos_idx])

        if parent_window.docking_state:
            
            #move each of the child windows with the parent
            for child_window in child_windows:

                '''MAYBE ADD ABILITY TO SCALE CHILD WINDOWS WITH PARENT'''
                
                child_dim = child_window.geometry().split('+')
                
                child_window.prev_pos_x = int(child_dim[x_pos_idx])
                child_window.prev_pos_y = int(child_dim[y_pos_idx])
                
                child_dim = (child_dim[0]+"+"+
                             str(root_x_shift + child_window.prev_pos_x)+"+"+
                             str(root_y_shift + child_window.prev_pos_y) )
                
                child_window.geometry(child_dim)

    parent_window.window_docking_updating = False
