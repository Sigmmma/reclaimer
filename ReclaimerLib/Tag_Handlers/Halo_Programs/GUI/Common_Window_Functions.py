#these are just constants to illustrate what's going on
X_Scl_Idx = 0
Y_Scl_Idx = 1
X_Pos_Idx = 1
Y_Pos_Idx = 2


#this function will allow the supplied child windows to move with the supplied parent window
def Dock_Window_Movement(Parent_Window, Child_Windows):

    Parent_Window.Window_Docking_Updating = True
    
    #the .geometry() returns the dimensions as a string that looks like "WidthxHeight+PosX+PosY"
    #an example would be "200x200+50+50". Because of that we need to split them apart at the x and +
    Root_Dimensions = Parent_Window.geometry().split('+')
    
    #we want to move the child windows with the main, but keep their relative position to the main
    if ((int(Root_Dimensions[X_Pos_Idx]) != Parent_Window.Previous_Pos_X) or
        (int(Root_Dimensions[Y_Pos_Idx]) != Parent_Window.Previous_Pos_Y)):
        
        #get the amount that the main window has been moved
        root_x_shift = (int(Root_Dimensions[X_Pos_Idx]) - Parent_Window.Previous_Pos_X)
        root_y_shift = (int(Root_Dimensions[Y_Pos_Idx]) - Parent_Window.Previous_Pos_Y)

        #set the new parent window's location
        Parent_Window.Previous_Pos_X = int(Root_Dimensions[X_Pos_Idx])
        Parent_Window.Previous_Pos_Y = int(Root_Dimensions[Y_Pos_Idx])

        if Parent_Window.docking_state:
            
            #move each of the child windows with the parent
            for Child_Window in Child_Windows:

                '''MAYBE ADD ABILITY TO SCALE CHILD WINDOWS WITH PARENT'''
                
                Child_Dimensions = Child_Window.geometry().split('+')
                
                Child_Window.Previous_Pos_X = int(Child_Dimensions[X_Pos_Idx])
                Child_Window.Previous_Pos_Y = int(Child_Dimensions[Y_Pos_Idx])
                
                Child_Dimensions = (Child_Dimensions[0]+"+"+
                                    str(root_x_shift + Child_Window.Previous_Pos_X)+"+"+
                                    str(root_y_shift + Child_Window.Previous_Pos_Y) )
                
                Child_Window.geometry(Child_Dimensions)

    Parent_Window.Window_Docking_Updating = False



#this function will make the supplied child windows minimize and maximize with the parent window and vice versa
def Minimize_Maximize_Children_with_Parent(Parent_Window, Child_Windows, New_State):
    if not Parent_Window.Mini_Maxi_State_Changing:
        Parent_Window.Mini_Maxi_State_Changing = True

        if New_State == "MAX":
            Parent_Window.wm_state('normal')
            for Window in Child_Windows:
                Window.wm_state('normal')
        else:
            Parent_Window.wm_state('iconic')
            for Window in Child_Windows:
                Window.wm_state('iconic')
            
        Parent_Window.Mini_Maxi_State_Changing = False
        
