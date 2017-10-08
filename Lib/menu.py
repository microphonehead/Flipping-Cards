# define some RGB colours.
BLACK =(0, 0, 0)
BLUE =(0, 0, 200)
GREEN =(0, 200, 0)
GREY =( 50, 50, 50)
RED =(200, 0, 0)
WHITE = (255, 255, 255)
YELLOW =(220, 220, 0)
# _.

WINWIDTH = 640 # width of the program's window, in pixels
WINHEIGHT = 480 # height in pixels
HALF_WINWIDTH = int(WINWIDTH / 2)
HALF_WINHEIGHT = int(WINHEIGHT / 2)

if __name__ == '__main__':
    fatal_err =False
    wr_say_ife =False   # used by the wr_say routine.
    myerrors =[]


    try:
        import pygame
    except:
        myerrors.append("Error importing library: pygame.")
        

    try:
        from pygame.locals import *
    except:
        myerrors.append("Error importing library: pygame (locals).")

    if len(myerrors) >0:
        # looks like one or more of the libraries from above
        # couldn't be loaded.
        #
        # game can't run without these.
        fatal_err =True

        
    if len(myerrors) >0: # there were errors.
        print("WARNING!")
        if fatal_err ==False:
            print(" Errors were encountered while trying to import one ", end ="")
            print("or more libraries.")
            print("")
        else:
            # I don't think the game can run without the core libraries.
            print(" Fatal errors were encountered while trying to import ", end ="")
            print("one or more libraries.")
            print("")
            
        print(myerrors)
        print("")
        print("")
        
    try:
        #pygame.mixer.pre_init(44100, -16, 2, 2048) # increase buffer size from 1024 default - might fix probs with crackling sound?
        pygame.mixer.pre_init(44100, -16, 2, 1024) 
        pygame.init()
    except:
        myerrors.append("Error initialising the pygame library.")


    fpsClock = pygame.time.Clock()

    # set up the window
    DISPLAYSURF = pygame.display.set_mode((WINWIDTH, WINHEIGHT), 0, 32)




# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# >> This is the class that needs to imported to make text based menus <<
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


# --------------------------------------------------------------------
# Description:
#   The class has several routines to create, and manage a text based
#   menu interface.
#
#   The common steps to creating a menu with this class is as follows:
#       1.  Create a menu object.
#       2.  Add menu items for the user to select.
#       3.  Yield execution to menu control and wait for a menu item
#           to be selected.
#
# Summary:
#   Assists with the creation and management of a menu, including
#   interpreting which menu item has been selected by the user.
#
# NOTE(S):
#   The way I hacked the "type" keyword [str(type(txt_colour))] causes
#   a problem by ensure its not country indepenndant.
# --------------------------------------------------------------------
class MnuCntrl():

    # load the default fonts.
    print()
    print("Class MnuCntrl()")
    print("\tLoading menu fonts.")
    print()
            
    menu_def_list ={} # create a dictionary of default values to be used.        
    mnu_item_cntrls = [] # prep list for menu items.
    
    # --------------------------------------------------------------------
    def __init__(self):
        # init def fonts to use with the menu.
        
        self.mnuhdr =MnuCntrl.menu_def_list["header font"] 
        self.mnuitems_font =MnuCntrl.menu_def_list["items font"]
        
        self.items_col_active =MnuCntrl.menu_def_list["active colour"]
        self.items_col_inactive =MnuCntrl.menu_def_list["inactive colour"]

        print()
        print("Class MnuCntrl()")
        print("\tMenu header font =",MnuCntrl.menu_def_list["header font"])
        print("\tMenu item font =",MnuCntrl.menu_def_list["items font"])
        print()
    # __init__() ---------------------------------------------------------
                
    # --------------------------------------------------------------------
    # Description:
    #   This routine adds a new menu item for a menu object.
    #
    # Parameter(s):
    #   x, y            Integers
    #       Refer to the top left corner of the painted text.
    #
    #   item_caption    Str
    #       The caption given to the menu item.
    #
    #   txt_colour      Tuple
    #       Overrides the default colour of the menu item.
    #       Note:   Routine expect the Tuple to be 3 dimensions, the normal
    #               ranges of the RGB.
    # --------------------------------------------------------------------
    def add_item(self, x, y, item_caption, txt_colour =None):
        self.img_surf =[]
        looks_ok =False
        
        if txt_colour is None: # set the menu item to its default colour.
            txt_colour =self.items_col_inactive
        else:
            # verify parameter is valid
            #if "tuple" in str(type(txt_colour)):
            if isinstance(txt_colour, tuple):
                # variable is correct type.
                if len(txt_colour) ==3:
                    # things are looking good. Lets check if the
                    # tuple is made up of integers.
                    if isinstance(txt_colour[0], int):
                        if isinstance(txt_colour[1], int):
                            if isinstance(txt_colour[2], int):
                                looks_ok =True
                            else:
                                # the third element was the wrong type.
                                pass
                        else:
                            # the second element was the wrong type.
                            pass
                    else:
                        # the first element was the wrong type.
                        pass
                    
            if looks_ok ==False:
                # we got a problem, the calling routine has passed
                # the wrong variable type.

                # resort to using the default colour.
                txt_colour =self.items_col_inactive
                print("Resorted to using the default menu colour for a menu item control")

                           
        # lets add image refs ...
        #   - the colour of menu item text not clicked.
        #   - the colour of the bevel for the menu item.
        mf =self.mnuitems_font

        try:
            self.img_surf.append(mf.render(item_caption, True, txt_colour))
        except TypeError:
            # resort to using the default colour.
            txt_colour =self.items_col_inactive
            
            # make a final attemt at rendering the text using the
            # new configuration.
            self.img_surf.append(mf.render(item_caption, True, txt_colour))
            print("Resorted to using the default menu colour for a menu item control")
            
        self.img_surf.append(mf.render(item_caption, True, self.items_col_active))
        self.img_surf.append(mf.render(item_caption, True, GREY))
        self.img_rect =self.img_surf[0].get_rect()
        
        w =self.img_rect.width
        h = self.img_rect.height
        self.mnu_item_cntrls.append([x, y, w, h, self.img_surf, item_caption])
        return self.img_surf
    # add_item() -------------------------------------------------------
    
    # --------------------------------------------------------------------
    # Description:
    #   This routine paints all the menu items on the screen for the
    #   user to see.
    # --------------------------------------------------------------------
    def paint(self):
        # examine all the menu items controls and
        # paint them on the screen.
        for mnuitem in self.mnu_item_cntrls:
            # get the co-ordinates for the menu item.
            x =mnuitem[0]
            y =mnuitem[1]
            # start by painting the bevel for the text.
            for n in range(5):
                img_rect =mnuitem[4][0].get_rect()
                img_rect.topleft = (x+n, y+n)
                DISPLAYSURF.blit(mnuitem[4][2], img_rect)

            # paint the primary text on top to give bevel effect.
            img_rect =mnuitem[4][0].get_rect()
            img_rect.topleft = (x, y)
            DISPLAYSURF.blit(mnuitem[4][0], img_rect)
            pygame.display.flip()
        return True
    # paint() ------------------------------------------------------------
    
    # --------------------------------------------------------------------
    # Description:
    #   This routine examines the (passed) mouse co-ordinates and alters
    #   the menu items status to active and inactivet acordingly based on
    #   the players specified position.
    # --------------------------------------------------------------------
    def paint_items_state(self, mousexy):
        mnu_option =0
        msex, msey =mousexy
        for mnuitem in self.mnu_item_cntrls:
            mnu_option +=1
            w =mnuitem[2]
            h =mnuitem[3]
            active_button =False
            
            # get the co-ordinates for the menu item controls.
            x =mnuitem[0]
            y =mnuitem[1]
            # _.
            
            if msex >= x and msex <=x +w:
                if msey >= y and msey <=y +h:
                    # this button was clicked.
                    active_button =True
            if active_button ==True:
                # paint the menu item as active.
                img_rect =mnuitem[4][1].get_rect()
                img_rect.topleft = (x, y)
                DISPLAYSURF.blit(mnuitem[4][1], img_rect)
            else:
                # paint the menu item as inactive.
                img_rect =mnuitem[4][0].get_rect()
                img_rect.topleft = (x, y)
                DISPLAYSURF.blit(mnuitem[4][0], img_rect)
                
        pygame.display.flip()
    # paint_items_state() ----------------------------------------------
            
    # --------------------------------------------------------------------
    # Description:
    #   This routine removes all the menu items, and frees the
    #   image buffer
    #
    # Issues:
    #   I don't think so!!!
    # --------------------------------------------------------------------
    def reset(self):
        # need to figure out how to free the image buffer >???<
        
        mnu_item_cntrls =[]
    # reset() ------------------------------------------------------------
    
    # --------------------------------------------------------------------
    # Description:
    #   This routine waits for the user to select a menu item with the
    #   mouse.
    # --------------------------------------------------------------------
    def wait_ui(self):
        events =pygame.event.get() # clear kbd and mouse buffer.
    
        ui_ok =False
        while ui_ok ==False:
            #check for player input.
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                elif event.type == MOUSEBUTTONUP:
                    # Handle mouse click events
                    mousex, mousey = event.pos
                    
                    mnu_option =0
                    for cmdbutton in self.mnu_item_cntrls:
                        mnu_option +=1
                        w =cmdbutton[2]
                        h =cmdbutton[3]
                        if mousex >= cmdbutton[0] and mousex <=cmdbutton[0] +w:
                            if mousey >= cmdbutton[1] and mousey <=cmdbutton[1] +h:
                                # this button was clicked.
                                print("Menu item {} clicked.".format(mnu_option))
                                ui_ok =True
                                break
                elif event.type ==4:
                    # then its a mouse move event (?)
                    self.paint_items_state(event.pos)
                else:
                    # This is an event type that I haven't catered for.
                    pass
                
            pygame.display.flip()
            
        return cmdbutton
    # wait_ui() -------------------------------------------------------

    # --------------------------------------------------------------------
    # Description:
    #   Loads a specified font and returns the active font obj ref if
    #   possible.
    #
    #   The purpose of this wrapper routine is to trap any errors that
    #   might be encountered when selecting a font and resolve issues of
    #   incompatible fonts on different platforms by resorting to the
    #   default font when problems occur.
    # --------------------------------------------------------------------
    def wr_load_font(fnt_name, fnt_size):
        try:
            # try and load the desired font.
            cf =pygame.font.Font(fnt_name, fnt_size)
        except:
            try:
                # resort to loading the default font instead.
                cf =pygame.font.Font(None, fnt_size)
            except:
                cf =None
        print()
        print("menu.py - Class MnuCntrl().wr_load_font - Font =", cf)
        print()
        
        return cf # ref to currently (loaded) font.
    # wr_load_font() --------------------------------------------------------

    # using a dictionary object to make the variable data persistant (???)
##    menu_def_list["items font"] =wr_load_font('freesansbold.ttf', 60)
##    menu_def_list["header font"] =wr_load_font('freesansbold.ttf', 30)
    menu_def_list["items font"] =pygame.font.Font('freesansbold.ttf', 60)
    menu_def_list["header font"] =pygame.font.Font('freesansbold.ttf', 30)
    
    menu_def_list["active colour"] =YELLOW
    menu_def_list["inactive colour"] =WHITE
    
# Class MnuCntrl() --------------------------------------------------------
 


if __name__ == '__main__':
    # ---------------------------------------------------------------------
    # Description:
    #   This is the example code that invokes the class menu object.
    # ---------------------------------------------------------------------

    #fnt_header = wr_load_font('freesansbold.ttf', 30)
    menu_main =MnuCntrl() # create a new menu object.

    # attempt to load a font and let the routine handle/resolve
    # any errors.
    fnt_header =MnuCntrl.wr_load_font('freesansbold.ttf', 30)

    # >. Lets setup a line margin of 20 pixels per menu item and use it to
    # calculate the y position for the next menu item.
    ln_margin =20 # set the line margin.

    # Draw the menu caption on the 
    img_hdr_surf = fnt_header.render("Menu Control", True, BLUE)
    img_rect =img_hdr_surf.get_rect()
    x, y = HALF_WINWIDTH, 25
    img_rect.center = (x, y)
    DISPLAYSURF.blit(img_hdr_surf, img_rect)
    # _.

    #menu_main =MnuCntrl() # create a new menu object.
    
    # add menu items ...
    x, y = 20, 80
    menu_main.add_item(x, y, item_caption ="Play Game")

    y +=60 + ln_margin
    menu_main.add_item(x, y, "Hi Scores Table", (255, 255))
    
    y +=60 + ln_margin
    menu_main.add_item(x, y, "Help", WHITE)
    
    y +=60 + ln_margin
    menu_main.add_item(x, y, item_caption ="Quit")

    menu_main.paint()
    mnu_option =menu_main.wait_ui()

    print()
    print(mnu_option[5]) # write the name of the caption for the selected item.

    events =pygame.event.get() # clear kbd and mouse buffer.
    
    del menu_main # destroy the control and free memory.
    pygame.quit()
    quit()
