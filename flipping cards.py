# -------------------------------------------------------------------------
# NOTES:
#   Pygame comes with a builtin default font.
#
#   This can always be accessed by passing None as the font name.
# -------------------------------------------------------------------------

# -------------------------------------------------------------------------
# Thanks to:
#   python forum
#       snippsat
#           RE: using [isinstance] instead of [type].
#
# -------------------------------------------------------------------------

# VERSION INFORMATION
# -------------------------------------------------------------------------
# Version 0.21:
#   [1].    Fixed timing issue with playing sound, reduced the number of
#           channels from 8 to 2#

#   [2].    Added a wrapper routine for the espeak library.
#
#   [3].    Added exception handling when importing libraries.
#
#   [4].    Moved the card image files into the Images dir.
#
#   [5].    Update code to cleared the keyboard buffer.
#
#   [6].    Improved parameter checking
#
#   [7].    Added a background.
#
#   [8].    Used routine(s) from the os library to resolve path and
#           filename issues that may result from being run on other
#           platforms.
#
#   [9].    Found a nice bit of code from one of the members in the Python
#           forum and have found a way to position the game window at the
#           centre of the screen.
# -------------------------------------------------------------------------
# Version 0-20:
#   [1].    Updated the players status bar to incllude the round as well
#           as the level number.
#   [2].    Made some cosmetic changes to the code, and coments.
# -------------------------------------------------------------------------
# Version 0-19:
#   [1].    Introduced text to speach.
#   [2].    Made some enhancements to the data entry for the high score.
#   [3].    Expanded on the existing vocal prompts.
#   [4].    Added a level indicator under the timer.
# -------------------------------------------------------------------------
# Version 0-18:
#   [1].    added routines to save and load high score table from/to file.
# -------------------------------------------------------------------------
# Version 0-17:
#   [1].    Updated the hi-score table.
#
#   [2].    Added feature to allow user to add name to hst.
# -------------------------------------------------------------------------
# Version 0-16:
#   [1].    Added feature to reveal the cards to the player after they
#           got it wrong.
#
#   [2].    Update the phasing preparing the player to memorise the
#           cards before turning them over.
# -------------------------------------------------------------------------
# Version 0-15:
#   [1].    Added a non-functional hi-scores table.
# -------------------------------------------------------------------------
# Version 0-14:
#   [1].    Added some crude sound fx.
# -------------------------------------------------------------------------
# Version 0-13:
#   [1].    Modified game so that a sound when the user completes the
#           stage successfully, and another sound when the user fails to
#           complete the stage.
# -------------------------------------------------------------------------
# Version 0-12:
#   [1].    Introduced sound.
#               When the user turns over a card a sound is played.
#
#   [2].    Created a flash feature.
#               Text can flashed on the screen for a set number of intervals.
#
#   [3].    Improved message alerts.
#               The messages to the player have now been improved.
# -------------------------------------------------------------------------
# Version 0-11:
#   [1].    Worked on the naming convention of some of the routine to make it
#           more logical.
# =========================================================================

#import random, pygame, sys, time

fatal_err =False

# > ife (ignore further errors) flag(s)
ife_wr_say =False   # used by the wr_say routine .
# .

myerrors =[] # create a list object to hold errors that I encounter.


try:
    import random
except:
    #print("FATAL ERROR"
    #print("Failed to import one or more core libries.")
    myerrors.append("Error importing library: random.")

try:
    import pygame
except:
    myerrors.append("Error importing library: pygame.")
    
try:
    import sys
except:
    myerrors.append("Error importing library: sys.")

try:
    import time
except:
    myerrors.append("Error importing library: time.")

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

sys.path.insert(1,'code') # add a folder to the sys path search register ([code] ???).

try:
    from debugfc import cards_debug_print
except:
    myerrors.append("Error importing library: debugfc.")

try:
    from debugfc import debug_hst
except:
    myerrors.append("Error importing library: debugfc.")

try:
    from debugfc import deck_debug_print
except:
    myerrors.append("Error importing library: debugfc.")

try:
    from espeak import espeak
except:
    myerrors.append("Error importing library: espeak.")

try:
    import os
except:
    myerrors.append("Error importing library: sys.")

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


FPS = 30 # frames per second setting
#FPS = 3 # frames per second setting

WINWIDTH = 640 # width of the program's window, in pixels
WINHEIGHT = 480 # height in pixels
HALF_WINWIDTH = int(WINWIDTH / 2)
HALF_WINHEIGHT = int(WINHEIGHT / 2)

fpsClock = pygame.time.Clock()

# set up the window
infoObject = pygame.display.Info()
##display_width = int(infoObject.current_w /3)
##display_height = int(infoObject.current_h /3)

# display the pygame window in the middle of the screen.
x =(infoObject.current_w /2) -(WINWIDTH /2)
y =(infoObject.current_h /2) -(WINHEIGHT /2)
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (x, y)
DISPLAYSURF = pygame.display.set_mode((WINWIDTH, WINHEIGHT), 0, 32)

pygame.display.set_caption('Flipping Cards')


# define some RGB colours.
BLACK =(0, 0, 0)
BLUE =(0, 0, 200)
GREEN =(0, 200, 0)
RED =(200, 0, 0)
WHITE = (255, 255, 255)
YELLOW =(200, 200, 0)
# _.


BASICFONT = pygame.font.Font('freesansbold.ttf', 32)
IMG_CARD_BACK =0
IMG_CARD_1 =1
IMG_CARD_2 =2
IMG_CARD_3 =3

# index for navigating the card placement array list.
C_CPH_X =0
C_CPH_Y =1
C_CPH_STATUS =2
C_CPH_CRD =3

#catImg = pygame.image.load('card - back.png')

deck = []
cards = []
crd =[]

arr_card_place_holders = [
    [140, 140, False, None],
    [ 40, 140, False, None],
    [440,  20, False, None],
    [340,  20, False, None],
    [240,  20, False, None],
    [140,  20, False, None],
    [ 40,  20, False, None]]
    

score =0


# define a structure type to hold information on cards
class stype_deck():
    facedown =False     # True if the card is face-down.
    faceup =True        # True if the card is face-up.
    height =100
    img_bk =False       # image of the card face-down.
    img_face =False     # image of the card face-up.
    img_ref =False      # default image ref for the object.
    num =False          # the number painted of the face of the card.
    status =False
    width =70
    x =0
    y =0
# _.    
    

    

# load the card images as frames ...
cardimages = []
##cardimages.append( pygame.image.load('card - back.png'))
##cardimages.append( pygame.image.load('card - face01.png'))
##cardimages.append( pygame.image.load('card - face02.png'))
##cardimages.append( pygame.image.load('card - face03.png'))
##cardimages.append( pygame.image.load('card - face04.png'))
##cardimages.append( pygame.image.load('card - face05.png'))
##cardimages.append( pygame.image.load('card - face06.png'))
##cardimages.append( pygame.image.load('card - face07.png'))
##cardimages.append( pygame.image.load('card - face08.png'))
##cardimages.append( pygame.image.load('card - face09.png'))
##cardimages.append( pygame.image.load('card - face10.png'))
##cardimages.append( pygame.image.load('card - face11.png'))
##cardimages.append( pygame.image.load('card - face12.png'))

##cardimages.append( pygame.image.load("Images/card - back.png"))
##cardimages.append( pygame.image.load('Images/card - face01.png'))
##cardimages.append( pygame.image.load('Images/card - face02.png'))
##cardimages.append( pygame.image.load('Images/card - face03.png'))
##cardimages.append( pygame.image.load('Images/card - face04.png'))
##cardimages.append( pygame.image.load('Images/card - face05.png'))
##cardimages.append( pygame.image.load('Images/card - face06.png'))
##cardimages.append( pygame.image.load('Images/card - face07.png'))
##cardimages.append( pygame.image.load('Images/card - face08.png'))
##cardimages.append( pygame.image.load('Images/card - face09.png'))
##cardimages.append( pygame.image.load('Images/card - face10.png'))
##cardimages.append( pygame.image.load('Images/card - face11.png'))
##cardimages.append( pygame.image.load('Images/card - face12.png'))

##cardimages.append(pygame.image.load("Images/card - back.png").convert())
##cardimages.append(pygame.image.load('Images/card - face01.png').convert())
##cardimages.append(pygame.image.load('Images/card - face02.png').convert())
##cardimages.append(pygame.image.load('Images/card - face03.png').convert())
##cardimages.append(pygame.image.load('Images/card - face04.png').convert())
##cardimages.append(pygame.image.load('Images/card - face05.png').convert())
##cardimages.append(pygame.image.load('Images/card - face06.png').convert())
##cardimages.append(pygame.image.load('Images/card - face07.png').convert())
##cardimages.append(pygame.image.load('Images/card - face08.png').convert())
##cardimages.append(pygame.image.load('Images/card - face09.png').convert())
##cardimages.append(pygame.image.load('Images/card - face10.png').convert())
##cardimages.append(pygame.image.load('Images/card - face11.png').convert())
##cardimages.append(pygame.image.load('Images/card - face12.png').convert())

### utilise the os library to load our card images to lower the risk of
### problems occurring while running on other platforms.
##cardimages.append(pygame.image.load(os.path.join("Images", "card - back.png")).convert())
##cardimages.append(pygame.image.load(os.path.join("Images", "card - face01.png")).convert())
##cardimages.append(pygame.image.load(os.path.join("Images", "card - face02.png")).convert())
##cardimages.append(pygame.image.load(os.path.join("Images", "card - face03.png")).convert())
##cardimages.append(pygame.image.load(os.path.join("Images", "card - face04.png")).convert())
##cardimages.append(pygame.image.load(os.path.join("Images", "card - face05.png")).convert())
##cardimages.append(pygame.image.load(os.path.join("Images", "card - face06.png")).convert())
##cardimages.append(pygame.image.load(os.path.join("Images", "card - face07.png")).convert())
##cardimages.append(pygame.image.load(os.path.join("Images", "card - face08.png")).convert())
##cardimages.append(pygame.image.load(os.path.join("Images", "card - face09.png")).convert())
##cardimages.append(pygame.image.load(os.path.join("Images", "card - face10.png")).convert())
##cardimages.append(pygame.image.load(os.path.join("Images", "card - face11.png")).convert())
##cardimages.append(pygame.image.load(os.path.join("Images", "card - face12.png")).convert())
##
##img_bkgnd_main =pygame.image.load(os.path.join("Images", "sunset.png")).convert()

#sfx['explosion_1'] = pygame.mixer.Sound(os.path.join(header.paths['sounds'],"smallexp.wav"))


#cardimages.append(pygame.image.load(os.path.join('Images', 'face12.png')).convert())
#img = pygame.image.load(os.path.join('C:/Users/Gebruiker/Desktop/Renders', 'Render.png')).convert()
# _.  



##
##
### prepare x number of cards for the deck
##for card_cntr in range(1, len(cardimages)):
##    crd = stype_deck()                      # create a new card object
##    crd.num =card_cntr                      # set the face value of the card.
##    crd.img_bk = cardimages[IMG_CARD_BACK]  
##    crd.img_face = cardimages[card_cntr]
##    crd.img_ref =crd.img_bk
##    crd.status = False
##    cards.append(crd)                       # add the card to the collection.
##    del crd
### _. 
##




### write a message to the screen (and center it) ...
##winSurf2 = BASICFONT.render('(Press "r" to restart.)', True, WHITE)
##winRect2 = winSurf2.get_rect()
##winRect2.center = (HALF_WINWIDTH, HALF_WINHEIGHT + 30)






# ---------------------------------------------------------------------------
# Summary:
#   This routine clears the screen.
# ---------------------------------------------------------------------------
def cls():
     # clear the screen.
    pygame.draw.rect(DISPLAYSURF, BLACK, (0, 0, WINWIDTH, WINHEIGHT))
# cls() ---------------------------------------------------------------------



# ---------------------------------------------------------------------------
# Summary:
#   I have designed this routine to excamine the array of card placements,
#   and remove any cards associated with it.
# ---------------------------------------------------------------------------
def cph_clear():
    global arr_card_place_holders
    
    # search for the next free slot where a card can be placed.
    for cph in arr_card_place_holders:
        if cph[C_CPH_CRD] !=False: # a card is occupping the space.
            # the card placement position is being used.
            cph[C_CPH_STATUS] =False    # change flag to show pos is available.

            # update the card properties before
            # removing it from the board.
            silently =False
            card_turn_facedown(cph[C_CPH_CRD], silently)
            cph[C_CPH_CRD] =None         # remove the card object from the array.
        
# cph_clear()----------------------------------------------------------------



# ---------------------------------------------------------------------------
# Summary:
#   I have designed this routine to pick a card from the deck.
#
# Desc:
#   Step 1-
#       select a card from the top of the deck.
#
#   Step 2-
#       Position the card in the next available slot position.
#
#   Step 3-
#       Paint the image on the screen.
#
# ---------------------------------------------------------------------------
def deal_a_card():
##C_CPH_X
##C_CPH_Y
##C_CPH_STATUS
##C_CPH_CRD
    global arr_card_place_holders, deck

    cph =stype_cph
    crd =stype_deck
    crd = deck.pop()
    
    # search for the next free slot where a card can be placed.
    for cntr in range(len(arr_card_place_holders), 0, -1):
        cph =arr_card_place_holders[cntr -1]
        if cph[2] ==False:
            # the card placement position is available.
            crd.x =cph[C_CPH_X]
            crd.y =cph[C_CPH_Y]
            cph[C_CPH_STATUS] =True     # change flag to show it is being used.
            cph[C_CPH_CRD] =crd         # store the cards obj ref.
            break
# deal_a_card() -------------------------------------------------------------        
    

        
# ---------------------------------------------------------------------------
# Description:
#   This routine shuffles the deck of cards.
# ---------------------------------------------------------------------------
def deck_shuffle(deck_size =len(deck)):
    global deck

    for cntr in range(0,deck_size -1):
        # relative to the number of cards in the shuffle the
        # deck x amount of times.
        index =random.randint(0, (deck_size -1))
        
        # take a card from the deck,
        # - remember it,
        # - then add it to the bottom of the pack.
        crd =deck.pop(index)
        deck.append(crd)
# deck_shuffle(~) -----------------------------------------------------------

        

# ---------------------------------------------------------------------------
# Description:
#   This routine creates a deck (pack) of cards to use.
# ---------------------------------------------------------------------------
def deck_build(num_of_cards =3):
    global deck, cards
    
    # check if there's an old pack of cards.
    if deck is not None:
        # throw away the old deck and start a new deck of cards.
        del deck
        deck =[]

    if num_of_cards > len(cards):
        # the calling routine is trying use more
        # cards than are avainlable.
        num_of_cards =len(cards)

    if num_of_cards <1:
        # the calling routine is trying build a deck of cards
        # with no cards
        num_of_cards =1

##    print()
##    print("ROUTINE: deck_build()")
##    print("\t var num_of_cards =", num_of_cards)
##    print()
    
    # put the cards into a deck        
    for card_cntr in range(0, num_of_cards, 1):
        # add the current card to the deck.
        crd =cards[card_cntr]
        deck.append(cards[card_cntr])
# deck_build(~) -------------------------------------------------------------



# ---------------------------------------------------------------------------
# Summary:
#   This routine removes the cards from view.
# ---------------------------------------------------------------------------
def cards_hide():
##C_CPH_X
##C_CPH_Y
##C_CPH_STATUS
##C_CPH_CRD

    # search for any cards that have been placed in one of our slots.
    for cntr in range(len(arr_card_place_holders), 0, -1):
        cph =arr_card_place_holders[cntr -1]
        # access the card's properties and update it so that it
        # indicates that the card should be drawn face down.
        
        if cph[C_CPH_CRD] is not None:
            # the list element is being used (presumably being a card obj.

            # attempt to reference the card obj.
            crd =cph[C_CPH_CRD] 
                        
            # erase the image of the card.
            #DISPLAYSURF.blit(img_ref, (crd.x, crd.y))
            pygame.draw.rect(DISPLAYSURF, BLACK, (crd.x, crd.y, crd.width, crd.height))

    # update screen with changes.
    #pygame.display.flip()
# cards_hide() --------------------------------------------------------------



# ---------------------------------------------------------------------------
# Description
#   This routine has been designed to examine all the cards that have
#   been placed in the card slots, and turn them over.
#
#
# ---------------------------------------------------------------------------
def cards_turn(ls =False, ip=False, tup =False):
##C_CPH_X
##C_CPH_Y
##C_CPH_STATUS
##C_CPH_CRD

    #nextcrd =1
    
##    if ip ==True: # include pause.
##        pass

    tstatus =False
    
    #if "int" in str(type(ip)):
    if isinstance(ip, int):
        secs = ip *1000
    #elif "float" in str(type(ip)):
    elif isinstance(ip, float):
        secs = int(ip *1000)
    #elif "bool" in str(type(ip)):
    elif isinstance(ip, bool):
        secs =0
    else:
        # Error, an invalid parameter was passed.
        # we were expecting an integer.
        #
        # set the pause interval to 1 sec'.
        print("DEBUG [cards_facedown] - Runtime error.")
        print("      ip[{}]".format(ip))
        print("")
        
        ip =500 # default to half a sec'.
        
    if ls ==False:
        # search for any cards that have been placed in one of our slots.
        for cntr in range(len(arr_card_place_holders), 0, -1):
            cph =arr_card_place_holders[cntr -1]
            if cph[C_CPH_CRD] is not None:
                # the card placement position is being used.
                #            
                # access the card's properties and update it so that it
                # indicates that the card has turned around..
                crd =cph[C_CPH_CRD]
                if tup ==True:
                    tstatus =card_turn_faceup(crd)
                else:
                    tstatus =card_turn_facedown(crd)
                
    else:
        for nextcrd in range(1, len(arr_card_place_holders) +1):
            # turn over the cards in sequential order.
            for cntr in range(len(arr_card_place_holders), 0, -1):
                cph =arr_card_place_holders[cntr -1]
                if cph[C_CPH_CRD] is not None:
                    # the card placement position is being used.
                    #            
                    # access the card's properties and update if it's
                    # the next card to be turned over.
                    crd =cph[C_CPH_CRD]
                    if crd.num ==nextcrd:
                        # this is the next card and should be turned over.
                        if tup ==True:
                            # the cards need to be turned face up.
                            tstatus =card_turn_faceup(crd)

                            # paint an animated card cursor for
                            # the card we just turned over.
                            card_cursor_animate(crd)
                        else:
                            # the cards need to be turned face down.
                            tstatus =card_turn_facedown(crd)

                        if tstatus ==True:
                            # the card was already
                            # facing up/down.
                            
                            # paste the image to the image buffer.
                            DISPLAYSURF.blit(crd.img_ref, (crd.x, crd.y))
                            pygame.display.update()
                            pygame.time.wait(secs)
                            #exit
                            
                        break
# cards_turn() --------------------------------------------------------------



# ---------------------------------------------------------------------------
# Description:
#   This routine turns a card over (face up).
# ---------------------------------------------------------------------------
def card_cursor_animate(crd):
    fcol =YELLOW
    rgb_r =fcol[0]
    rgb_g =fcol[1]
    rgb_b =fcol[2]

    scrn=DISPLAYSURF
    incval =50
    
    for reps in range(1):
        r, g, b =0, 0, 0
        i =2
        while i <9:
            #r +=30 
            #g +=30
            #b +=30

            r +=incval 
            g +=incval
            b +=incval
            
            # create colour restrictions to ensure our
            # target colour isn't missed.
            if r >rgb_r:
                r =rgb_r
            if g >rgb_g:
                g =rgb_g
            if b >rgb_b:
                b =rgb_b
            
            #fcol =(rgb_r, rgb_g, rgb_b)
            pygame.draw.rect(scrn, (r, g, b), (crd.x -i, crd.y -i, crd.width +(i*2), crd.height +(i*2)), 3)
            pygame.display.flip()
            pygame.time.wait(50)
            pygame.draw.rect(scrn, BLACK, (crd.x -i, crd.y -i, crd.width +(i*2), crd.height +(i*2)), 3)
                
            i =(i * 1.6)
            incval -=10

        incval =50 # reset the incremental value.
        
        # perform the fade-out operation.    
        for a in range(6):
            #r -=30
            #g -=30
            #b -=30

            r -=incval
            g -=incval
            b -=incval
            if r <1:
                r =0
            if g <1:
                g =0
            if b <1:
                b =0
            pygame.draw.rect(scrn, (r, g, b), (crd.x -i, crd.y -i, crd.width +(i*2), crd.height +(i*2)), 3)
            pygame.display.flip()
            pygame.time.wait(100)
            pygame.draw.rect(scrn, BLACK, (crd.x -i, crd.y -i, crd.width +(i*2), crd.height +(i*2)), 3)
            if (r <1) and (g <1) and (b <1):
                break

            incval -=5
        
# card_cursor_animate(~) -----------------------------------------------------



# ---------------------------------------------------------------------------
# Description:
#   This routine turns a card over (face up).
# ---------------------------------------------------------------------------
def card_turn_faceup(crd):
##C_CPH_X
##C_CPH_Y
##C_CPH_STATUS
##C_CPH_CRD

    global click_sound
    retval =False
    
    # make sure the calling routine passed us something.
    if crd is not None:
        # access the card's properties and update it so that it
        # indicates that the card should be drawn face down.
        #crd =cph[C_CPH_CRD]
        if crd.facedown ==True:
            retval =True
            click_sound.play()
            
        crd.facedown =False
        crd.faceup =True

        crd.img_ref =crd.img_face

        return retval
# card_turn_faceup(~) -------------------------------------------------------



# ---------------------------------------------------------------------------
# Description:
#   This routine turns a card over (face up).
# ---------------------------------------------------------------------------
def card_turn_facedown(crd, silently =False):
##C_CPH_X
##C_CPH_Y
##C_CPH_STATUS
##C_CPH_CRD

    global click_sound
    retval =False

    # make sure the calling routine passed us something.
    if crd is not None:
        # access the card's properties and update it so that it
        # indicates that the card should be drawn face down.
        #crd =cph[C_CPH_CRD]
        if crd.faceup ==True:
            retval =True
            if silently ==False:
                click_sound.play()
            
        crd.facedown =True
        crd.faceup =False

        # set the default image based on the card's orientation.
##        if crd.facedown ==True:
##            img_ref =crd.img_bk
##        else:
##            img_ref =crd.img_face
        
        crd.img_ref =crd.img_bk

        #click_sound.play()
        return retval
# card_turn_facedown(~) -----------------------------------------------------



# ---------------------------------------------------------------------------
# Description:
#   This routine examines the card object and returns a value deppending on
#   the card being face-down or face-up.
# ---------------------------------------------------------------------------
def card_is_faceup(crd):
    # make sure the calling routine passed us something.
    if crd is not None:
        # access the card's properties and update it so that it
        # indicates that the card should be drawn face down.
        if crd.faceup ==True:
            return True
        else:
            return False
    else:
        return false
# card_is_faceup(~)---------------------------------------------------------------------------



# ---------------------------------------------------------------------------
# Description:
#   This routine examines the card placement list and paints all the cards
#   that are referenced in the list object.  The cards properties are examined
#   to determine if the card should be painted face down or face up.
#
# Summary:
#   This routine examines the card placement list and paints all the cards
#   that are referenced in the list object.
# ---------------------------------------------------------------------------
def cards_paint_active_cards():
##C_CPH_X
##C_CPH_Y
##C_CPH_STATUS
##C_CPH_CRD

    # search for any cards that have been placed in one of our slots.
    for cntr in range(len(arr_card_place_holders), 0, -1):
        cph =arr_card_place_holders[cntr -1]
        # access the card's properties and update it so that it
        # indicates that the card should be drawn face down.
        
        if cph[C_CPH_CRD] is not None:
            # the list element is being used (presumably being a card obj.

            # attempt to reference the card obj.
            crd =cph[C_CPH_CRD] 

            # check which image should be used when painting the card.
            if crd.facedown ==True:
                img_ref =crd.img_bk
            else:
                img_ref =crd.img_face

            # paste the image to the image buffer.
            DISPLAYSURF.blit(img_ref, (crd.x, crd.y))
            #pygame.display.update()
# cards_paint_active_cards(~) -----------------------------------------------



# ---------------------------------------------------------------------------
# Summary:
#   Anything that needs to be performed before the level starts should be
#   placed.
# ---------------------------------------------------------------------------
def game_init():
    global hst
    global score, gstagecntr, glevel
    global cardimages, img_bkgnd_main
    global snd_lbegin, snd_gintro, snd_gend, snd_tmrl, click_sound
    global snd_send_ok, snd_send_fail, snd_cards_new
    

    score =0
    gstagecntr =0   # reset the stage number.
    glevel =0       # set the level number.

    # create a default hi-score table.
    hst =[]
    hst.append(["Stuart Charles", 300])
    hst.append(["Keano Reeves", 250])
    hst.append(["Tony Prescot", 200])
    hst.append(["Fireman Sam", 150])
    hst.append(["John Travolta", 100])
    # _.

    # -------------------------------------------------------------------------
    # utilise the os library to load our card images to lower the risk of
    # problems occurring while running on other platforms.
    cardimages.append(pygame.image.load(os.path.join("Images", "card - back.png")).convert())
    cardimages.append(pygame.image.load(os.path.join("Images", "card - face01.png")).convert())
    cardimages.append(pygame.image.load(os.path.join("Images", "card - face02.png")).convert())
    cardimages.append(pygame.image.load(os.path.join("Images", "card - face03.png")).convert())
    cardimages.append(pygame.image.load(os.path.join("Images", "card - face04.png")).convert())
    cardimages.append(pygame.image.load(os.path.join("Images", "card - face05.png")).convert())
    cardimages.append(pygame.image.load(os.path.join("Images", "card - face06.png")).convert())
    cardimages.append(pygame.image.load(os.path.join("Images", "card - face07.png")).convert())
    cardimages.append(pygame.image.load(os.path.join("Images", "card - face08.png")).convert())
    cardimages.append(pygame.image.load(os.path.join("Images", "card - face09.png")).convert())
    cardimages.append(pygame.image.load(os.path.join("Images", "card - face10.png")).convert())
    cardimages.append(pygame.image.load(os.path.join("Images", "card - face11.png")).convert())
    cardimages.append(pygame.image.load(os.path.join("Images", "card - face12.png")).convert())

##    print()
##    print("ROUTINE: game_init()")
##    print("\t var: cardimages - size=", len(cardimages))
##    print()
    
    img_bkgnd_main =pygame.image.load(os.path.join("Images", "sunset.png")).convert()
    # -------------------------------------------------------------------------
    
    
    # -------------------------------------------------------------------------
    # load some sounds ...
##    snd_lbegin =pygame.mixer.Sound("Sound/game_intro.ogg") # this file <-- ???
##    snd_tmrl =pygame.mixer.Sound("Sound/TimeLow.ogg")
##    click_sound = pygame.mixer.Sound("Sound/CardReveal.wav")
##    snd_send_ok =pygame.mixer.Sound("Sound/stageend_ok.ogg")
##    snd_send_fail =pygame.mixer.Sound("Sound/stageend_fail.ogg")
##    snd_gintro =pygame.mixer.Sound("Sound/game_intro.ogg")
##    snd_gend =pygame.mixer.Sound("Sound/GameOver.ogg")
##    snd_cards_new =pygame.mixer.Sound("Sound/NewCards.wav")

    snd_lbegin =pygame.mixer.Sound(os.path.join("Sound", "game_intro.ogg")) # this file <-- ???
    snd_tmrl =pygame.mixer.Sound(os.path.join("Sound", "TimeLow.ogg"))
    click_sound = pygame.mixer.Sound(os.path.join("Sound", "CardReveal.wav"))
    snd_send_ok =pygame.mixer.Sound(os.path.join("Sound", "stageend_ok.ogg"))
    snd_send_fail =pygame.mixer.Sound(os.path.join("Sound", "stageend_fail.ogg"))
    snd_gintro =pygame.mixer.Sound(os.path.join("Sound", "game_intro.ogg"))
    snd_gend =pygame.mixer.Sound(os.path.join("Sound", "GameOver.ogg"))
    snd_cards_new =pygame.mixer.Sound(os.path.join("Sound", "NewCards.wav"))

    

    # prepare x number of cards for the deck
    for card_cntr in range(1, len(cardimages)):
        crd = stype_deck()                      # create a new card object
        crd.num =card_cntr                      # set the face value of the card.
        crd.img_bk = cardimages[IMG_CARD_BACK]  
        crd.img_face = cardimages[card_cntr]
        crd.img_ref =crd.img_bk
        crd.status = False
        cards.append(crd)                       # add the card to the collection.
        del crd
    # _. 


    # -------------------------------------------------------------------------


    hstable_load() # load the high score table.

# game_init() ----------------------------------------------------------------



# ---------------------------------------------------------------------------
# Summary:
#   Anything that needs to be performed before the game starts should be
#   placed here.
# ---------------------------------------------------------------------------
def game_begin():
    global snd_gintro
    global score, gstagecntr, glevel
    
    score =0
    gstagecntr =0   # reset the stage number.
    glevel =1       # set the level number.
    
# game_begin() --------------------------------------------------------------



# ---------------------------------------------------------------------------
# Summary:
#   Anything that needs to be performed at the end of a level.
# ---------------------------------------------------------------------------
def game_end():
    global snd_lbegin
    
    y =HALF_WINHEIGHT
    lmargine =10
    l = 0               # the text line number.
    
    snd_gend.play()     # play the sound associated with the end of game.
    
    fnt_title = pygame.font.Font('freesansbold.ttf', 40)

    tl =7
    strmsg ="Game Over"
    def_col=RED
    flash_msg =True
    pauselock =False
    pause_msg(tl, strmsg, def_col, flash_msg, pauselock)
        
    cls()

    hstable_paint() # list the high scores.
# game_end() -----------------------------------------------------------------



# ---------------------------------------------------------------------------
# Summary:
#   This rountine inserts a new high score into the hi-score table.
# ---------------------------------------------------------------------------
def hstable_insert(n_name, n_score):
    fnd =False
    ip =False       # insertion pointer

    # search the hst for a place to insert the new rec. 
    for ip in range(len(hst) +1): 
        c_name, c_score =hst[ip]
        if n_score > c_score: # we've found the insertion point.
            fnd =True
            break

    if fnd ==True: # an insertion point was found.
        hst.insert(ip, (n_name, n_score))   # insert the new high score record.
        hst.pop()                           # delete the last hs record from the list.

# hstable_insert(~) ---------------------------------------------------------



# ---------------------------------------------------------------------------
# Summary:
#   This rountine looks at the hi-score table and searches for the lowest
#   score, and returns it to the calling routine.
# ---------------------------------------------------------------------------
def hstable_min_get():
    lscore =-1
    for pname, pscore in hst:
        if pscore <lscore or lscore ==-1: # we've found a new high.
            lscore =pscore

    # return the lowest score.
    return lscore
# hstable_min_get() ---------------------------------------------------------



# ---------------------------------------------------------------------------
# Summary:
#   This rountine saves the hi-score table.
# ---------------------------------------------------------------------------
def hstable_save():
    file_a =open("hiscore.txt", mode="w", encoding="utf-8")
    for pname, pscore in hst:
        # write the rec to file with padded spaces so we can read
        # it back easier.
        file_a.write("{0:40}".format(pname))
        file_a.write("{0:10}".format(str(pscore)))
    file_a.close()
# hstable_save() ------------------------------------------------------------



# ---------------------------------------------------------------------------
# Summary:
#   This rountine loads the hi-score table.
# ---------------------------------------------------------------------------
def hstable_load():
    global hst
    
    #debug_hst(hst)
    try:
        file_a =open("hiscore.txt", encoding="utf-8")
    except:
        # file can't be loaded. Skip it.
        return False
    
    hst =[] # reset/clear the variable for the hs table.

    # reload the hs table from the existing file.
    for cntr in range(5):
        pname =file_a.read(40)          # load the player's name.
        pscore =int(file_a.read(10))    # load the score for that player.

        hst.append([pname, pscore])     # update hst with new record.
    file_a.close()
    #debug_hst(hst)

    return True
# hstable_load() ------------------------------------------------------------



# ---------------------------------------------------------------------------
# Summary:
#   This rountine paints the hi-score table.
# ---------------------------------------------------------------------------
def hstable_paint():
    lnmargin =3
    rmargin =550
    
    y =40
    
    # write all the status msg's to the screen...
    for l in range(len(hst)):
        # render the end of stage message.
        pname, pscore =hst[l]
        img_gn_surf = fnt_title.render(pname, True, BLUE)
        img_rect =img_gn_surf.get_rect()
        img_rect.topleft = (50, y)
        DISPLAYSURF.blit(img_gn_surf, img_rect)

        img_gn_surf = fnt_title.render(str(pscore), True, BLUE)
        img_rect =img_gn_surf.get_rect()
        img_rect.topleft =(rmargin -img_rect.width, y)
        DISPLAYSURF.blit(img_gn_surf, img_rect)
        y =y +img_rect.height + lnmargin

    pygame.display.flip()
        
    pygame.time.wait(1500)

    tl =7
    def_col=WHITE
    flash_msg =False
    pauselock =False    # remove the lock so the user can exit the pause period.
    fntsize =20
    strmsg ="Press any key"
    pause_msg(tl, strmsg, def_col, flash_msg, pauselock, fntsize)
        
    cls()
    
# hstable_paint() -----------------------------------------------------------


    
# ---------------------------------------------------------------------------
# Summary:
#   This rountine prepares game for a new level.
# ---------------------------------------------------------------------------
def level_ini():

    global snd_lbegin, snd_lend, snd_tmrl
    
# level_ini() ---------------------------------------------------------------



# ---------------------------------------------------------------------------
# Summary:
#   This routine goes through the process of preparing for a level to
#   be played.
# ---------------------------------------------------------------------------
def level_begin():
    strmsg ="-- NEW LEVEL --"
    
    cls()               # clear the screen.

    # skip the new level msg if its still the 1st level.
    if glevel >1:
        #espeak.synth("You have completed level {}.".format(glevel -1))
        wr_say("You have completed level {}.".format(glevel -1))
        pause_msg(2, strmsg, GREEN, True )
        #espeak.synth("Now try level {}.".format(glevel))
        wr_say("Now try level {}.".format(glevel))
# level_begin() -------------------------------------------------------------



# ---------------------------------------------------------------------------
# Summary:
#   This routine starts the level.
# ---------------------------------------------------------------------------
def level_play():
    global gstagecntr, glevel, card_total, tsil, card_total, tl
    global GREEN
    
    ss =False           # stage staus.
        
    
    # run all the stages for this level.
    for gstagecntr in range(1, tsil +1):
        stage_ini()    
        stage_start()       # start the stage.
        ss =stage_play()
        
        # play the stuff that goes on the end of the stage...
        if ss ==True: # check the returned stage status.
            # the stage was completed ok.
            stage_end(ss) # run the end-stage in a special next-stage mode.
        else:
            # player failed to complete the stage successfully.
            stage_end()         # end the stage.
            break                # skip the other stages.

    return ss # stage status
# level_play() --------------------------------------------------------------



# ---------------------------------------------------------------------------
# Summary:
#   This rountine runs the things that need to be done when a level ends.
# ---------------------------------------------------------------------------
def level_end():

    cls()
# level_end() ---------------------------------------------------------------



# ---------------------------------------------------------------------------
# Summary:
#   This routine paints the game logo on the screen.
# ---------------------------------------------------------------------------
def play_title_screen():
    global fnt_title, snd_lbegin

    snd_gintro.play()
    #snd_gintro.music.play()
    
    fnt_title = pygame.font.Font('freesansbold.ttf', 40)

    # render the game name.
    img_gn_surf = fnt_title.render("Flipping Cards", True, BLUE)
    img_rect =img_gn_surf.get_rect()
    img_rect.center = (HALF_WINWIDTH, HALF_WINHEIGHT)
    DISPLAYSURF.blit(img_gn_surf, img_rect)

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
                else:
                    #print("user pressed a key to proceed.")
                    ui_ok =True
            elif event.type == MOUSEBUTTONUP:
                # Handle mouse click events
                #mousex, mousey = event.pos

                #print("User clicked a mouse button to proceed.")
                ui_ok =True
                
        pygame.display.flip()
        fpsClock.tick(FPS)
           
    pygame.draw.rect(DISPLAYSURF, BLACK, (img_rect.x, img_rect.y, img_rect.width, img_rect.height))
    
    snd_gintro.fadeout(1500)
    
    pygame.time.wait(2000)
# play_title_screen() -------------------------------------------------------


   
# ---------------------------------------------------------------------------
# Summary:
#   This routine is used to paint the timer on the screen.
# ---------------------------------------------------------------------------
def pause_msg(tl, strmsg, def_col=GREEN, flash_msg =False, pauselock =True, fntsize =40, pyield =False ):

    global fnt_title
    
    to =time.time()         # start the timer
    tr =1                   # time remaining
    tr_prev =0              # time remaining last time we checked.
    skip_pause =False       # True = the user can end the pause prematurely
    retval = False
    
    fnt_title = pygame.font.Font('freesansbold.ttf', fntsize)
    img_surf = fnt_title.render(strmsg, True, def_col)
    img_rect = img_surf.get_rect()
    img_rect.center = (HALF_WINWIDTH, 400)

    x,y =img_rect.topleft
    
    while tr >0:
        # prepare the screen area before printing the text msg.
        #pygame.draw.rect(DISPLAYSURF, BLACK, (x, y, img_rect.width, img_rect.height))
        
        # we need to blank out the whole area used by the alert message
        # because we're not keeping track of what we last wrote.
        x =0
        pygame.draw.rect(DISPLAYSURF, BLACK, (x, y, 550, img_rect.height))
        # ._

        
        tr =tl -(time.time() -to)   # calcualate the remaining time.

        # lets limit the checks to the buffer to 1 every second.
        if not tr_prev ==tr :
            # check to see if the user hit the [ESC] key to quit the game.
            for event in pygame.event.get():
                if event.type == QUIT:
                    # the user tried to close the window.
                    pygame.quit()
                    sys.exit()
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                        #quit()
            
        tr_prev =tr
        
        if tr >0: # there is still time left on the clock.
            # display the pause message.
            if flash_msg ==True:
                # the message needs to flashing
                if (tr -int(tr)) >=0.5: # this is the visible interval.
                    DISPLAYSURF.blit(img_surf, img_rect)

            else:
                # the msg shouldn't flash.
                DISPLAYSURF.blit(img_surf, img_rect)
        
            pygame.display.flip()

            if pauselock ==False: # skip pause if user has clicked anything.
                for event in pygame.event.get():
                    if event.type == QUIT:
                        #pygame.quit()
                        #sys.exit()
                        pass
                    elif event.type == KEYDOWN:
                        if event.key == K_ESCAPE:
                            pygame.quit()
                            sys.exit()
                        else: # set flag to exit pause routine.
                            skip_pause =True
                    elif event.type == MOUSEBUTTONUP:
                        # Handle mouse click events
                        #mousex, mousey = event.pos
                        skip_pause =True
                        
                if skip_pause ==True: # eixt the pause routine
                    break
                
            retval =True # set the return value.
            
            # we need to let the calling routine do their thing
            # while we're in the paused fased.
            if pyield ==True:
                break

    ## remove the old pause msg from the screen.
    #pygame.draw.rect(DISPLAYSURF, BLACK, (img_rect.x, img_rect.y, img_rect.width, img_rect.height))

    if tr <=0:
        # remove the old pause msg from the screen.
        pygame.draw.rect(DISPLAYSURF, BLACK, (img_rect.x, img_rect.y, img_rect.width, img_rect.height))
        return False
    else:
        # return the remaining time.
        return tr
# pause_msg() ---------------------------------------------------------------

        
        
# ---------------------------------------------------------------------------
# Summary:
#   This rountine does stuff that needs to be performed before a stage begins.
# ---------------------------------------------------------------------------
def stage_ini():
    global crdval, end_stage, card_total, card_next
    global img_yl_surf, img_yl_rect, img_yw_surf, img_yw_rect, fnt_title
    
    
    crdval =1           # points for turning over correct card.
    #retval =False
    end_stage =False
    card_next =1
    card_total =0       # the number of cards the player needs to turn over.
    #tmr_str =""
    
    # reset the placement array.
    cph_clear() # remove the cards from the play area.

    fnt_title = pygame.font.Font('freesansbold.ttf', 20)
    
    # render the common text for loosing.
    img_yl_surf = fnt_title.render("You Loose!", True, RED)
    img_yl_rect =img_yl_surf.get_rect()

    # render the common text for winning.
    img_yw_surf = fnt_title.render("You win!", True, GREEN)
    img_yw_rect = img_yw_surf.get_rect()
    
# stage_ini() ---------------------------------------------------------------



# ---------------------------------------------------------------------------
# Summary:
#   This routine is used to start the stage.
# ---------------------------------------------------------------------------
def stage_start():

    global arr_card_place_holders, crdval
    global RED, GREEN, C_CPH_CRD
    global retval, end_stage, card_next, card_total, tmr_str, to
    global img_yl_surf, img_yl_rect, img_yw_surf, img_yw_rect, fnt_title
    global gstagecntr, glevel, cards, cardsinplay
    global click_sound, snd_send_ok, snd_send_fail, snd_cards_new
      
    cardsinplay =glevel +3 # calculate the number of cards to use.

    img_rect =img_bkgnd_main.get_rect()
    img_rect.topleft =0, 0
    DISPLAYSURF.blit(img_bkgnd_main, img_rect)
        
    psp_score_paint()
    psp_timer_paint(0, 0) # paint the timer caption.
    psp_level_paint()
    psp_round_paint()
    deck_build(cardsinplay)
    deck_shuffle(cardsinplay)

    # deal all the cards for this level
    for cc in range(cardsinplay):
        deal_a_card()           # deal a card from the pack.
   
    card_total =cardsinplay
    snd_cards_new.play()
        
    cards_turn()                # ensure cards are face down.
    cards_paint_active_cards()  # paint all the cards that have been place down.
    pygame.display.flip()
    
    def_col =WHITE      # set the default colour of the text image.
    flash_msg =False    # set the flag to flash the image.    
    pauselock =True     # allow the user to end the pause early.
    strmsg ="Round " +str(gstagecntr)
        
    #espeak.synth("Player.  Get ready")
    wr_say("Player.  Get ready")
              
    pause_msg(3, strmsg, def_col, flash_msg, pauselock)

    cards_turn(False,False,True)    # turn cards faceup.
    cards_paint_active_cards()      # paint all the cards that have been place down.
    pygame.display.flip()
    
    tl =3                       # set the timer for 3 sec's.
    to =time.time()             # set the timer to start from now.
    tr =16                      # set the remaining time var to non zero
    
    #espeak.synth("You  have three  secounds")
    wr_say("You  have three  secounds")
              
    pause_msg(4, "Memorise these cards", WHITE)
    
    cards_turn()                # turn all the cards facedown.
    cards_paint_active_cards()  # paint all the cards that have been place down.
    
    pygame.display.flip()
# stage_start() -------------------------------------------------------------    

    

# ---------------------------------------------------------------------------
# Summary:
#   This routine has been designed to enable the user to play stage in the
#   game.
# ---------------------------------------------------------------------------
def stage_play():
##C_CPH_X
##C_CPH_Y
##C_CPH_STATUS
##C_CPH_CRD
    
    global score
    global retval, end_stage, card_next, card_total, tmr_str, tl
    global img_yl_surf, img_yl_rect, img_yw_surf, img_yw_rect
    global snd_send_ok, snd_send_fail, click_sound
    
    end_stage =False
    tl =int(card_total *1.2)    # set the time limit for this stage.
    to =time.time()             # set the timer to start from now.
    tr =16
    ltsp =0                     # last time sound was played
    

    events =pygame.event.get() # clear kbd and mouse buffer.

    img_rect =img_bkgnd_main.get_rect()
    img_rect.topleft =0, 0
    while end_stage ==False:
        #check for player input.
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            #elif event.type == MOUSEBUTTONUP:
            elif event.type == MOUSEBUTTONDOWN:
                # Handle mouse click events
                mousex, mousey = event.pos
                
                # examine all the cards that have been placed in one of our slots
                # to see if they have been clicked.
                for cntr in range(len(arr_card_place_holders), 0, -1):
                    cph =arr_card_place_holders[cntr -1]
                    # access the card's properties and update it so that it
                    # indicates that the card should be drawn face down.
                    
                    if cph[C_CPH_CRD] is not None:
                        # the list element is being used (presumably being a card obj.

                        # attempt to reference the card obj.
                        crd =cph[C_CPH_CRD]
                        
                        if mousex >= crd.x and mousex < (crd.x +crd.width):
                            if mousey >= crd.y and mousey < (crd.y +crd.height):
                                # the user has clicked with the visible area of the
                                # card.
                                
                                # check if the card has already been turned over.
                                if card_is_faceup(crd) ==False:
                                    # the card hasn't been turned over.
                                    # update the crd object so that its face up.
                                    card_turn_faceup(crd)
                                    cards_paint_active_cards()
                                    #psp_score_paint()
                                    psp_paint(tl, to)
                                    card_cursor_animate(crd)
                                    
                                    # check if the correct card was turned over.
                                    if crd.num == card_next:
                                        # the player turned the correct card over.
                                        psp_score_addpoints()
                                    else:
                                        # the player turned over the wrong card.
                                        #psp_timer_hide()
                                        retval =False
                                        end_stage =True
                                        break
                                        
                                    psp_score_paint()
                                    
                                    # calc the value of the next card.
                                    card_next +=1 


        tr =psp_timer_paint(tl, to)
        #psp_level_paint()
        if end_stage !=True:
            # the game hasn't ended due to an incorrect answer.
            
            if card_next >card_total:
                # player has turned over all the cards.
                end_stage =True
                snd_send_ok.play()

                #espeak.synth("Well done")
                wr_say("Well done")

                bonus_points =psp_score_addtime_calc(tr) # add bonus points.
                
                psp_score_addtime(tr)
                                    
                tl =2
                strmsg ="You win"
                def_col=GREEN
                flash_msg =True
                pauselock =True
                pause_msg(tl, strmsg, def_col, flash_msg, pauselock)
   
                retval =True
                
            elif tr <0:
                # time expired.

                snd_send_fail.play()

                #espeak.synth("You ran out of time")
                wr_say("You ran out of time")
                
                tl =7
                strmsg ="Out of time"
                def_col=RED
                flash_msg =False
                pauselock =True
                pause_msg(tl, strmsg, def_col, flash_msg, pauselock)
                
                end_stage =True
                retval =False
            elif tr <9:
                if int(tr) !=int(ltsp):
                    # play the sound again.
                    snd_tmrl.play()
                    ltsp =int(tr)
            
        else:
            snd_send_fail.play()

            #espeak.synth("Wrong")
            wr_say("Wrong")
            
            tl =3
            strmsg ="You Loose"
            def_col=RED
            flash_msg =True
            pauselock =True
            pause_msg(tl, strmsg, def_col, flash_msg, pauselock)

            #espeak.synth("That  was  the wrong card.")
            wr_say("That  was  the wrong card.")
            
            card_turn_facedown(crd) # turn the last card face down.
            cards_paint_active_cards()
            card_cursor_animate(crd)
            card_cursor_animate(crd)
            card_cursor_animate(crd)
            pygame.time.wait(2000)

            #espeak.synth("This is how it should be done.")
            wr_say("This is how it should be done.")
              
            pygame.time.wait(2500)
            cards_turn(True, 0.5, True)

            tl =3
            strmsg ="Game over"
            def_col=RED
            flash_msg =False
            pauselock =True
            pause_msg(tl, strmsg, def_col, flash_msg, pauselock)

            #pygame.time.wait(5000)
            #espeak.synth("Better luck next time.")
            wr_say("Better luck next time.")
            
            #snd_send_fail.play()
            retval =False
        
        pygame.display.update()

        # prepare the screen buffer with a fresh coat of the background image.
        DISPLAYSURF.blit(img_bkgnd_main, img_rect)
        cards_paint_active_cards()
        psp_score_paint()
        fpsClock.tick(FPS)

    return retval
# stage_play() --------------------------------------------------------------



# ---------------------------------------------------------------------------
# Summary:
#   This rountine runs the things that need to be done when a level ends.
# ---------------------------------------------------------------------------
def stage_end(nextstage =False):
    global fnt_title
    global gstagecntr
    global snd_send_ok, snd_send_fail
    
    y =HALF_WINHEIGHT
    lmargine =10
    l = 0               # the text line number.
    
    fnt_title = pygame.font.Font('freesansbold.ttf', 30)
    psp_timer_hide()    # remove the timer from view.
    psp_level_hide()    # remove the level indicator from view.

    cards_turn()        # place all the cards face down.
    cls()               # clear the screen.

# stage_end(~) --------------------------------------------------------------



# ---------------------------------------------------------------------------
# Discription:
#   This lets the user type in there name and press enter.
# ---------------------------------------------------------------------------
def playername_get():
    K_ENTER =13
    K_BACKSPC =8
    
    pname =""
    nc =False
    img_msg =""
    plyri =""

    ib_x, ib_y, ib_width, ib_height =50, 100, 500, 45
    
    
    cls()

    # paint the input box.
    pygame.draw.rect(DISPLAYSURF, RED, (ib_x, ib_y, ib_width, ib_height))
    pygame.draw.rect(DISPLAYSURF, WHITE, (ib_x -5, ib_y -5, ib_width +10, ib_height +10), 3)

    # paint the prompt asking the user to enter their name.
    fnt_title = pygame.font.Font('freesansbold.ttf', 20)
    img_msg =fnt_title.render("Please enter your name...", True, BLUE)
    img_rect =img_msg.get_rect()
    DISPLAYSURF.blit(img_msg, img_rect)

    # paint the title for the high score.
    fnt_title = pygame.font.Font('freesansbold.ttf', 40)
    img_surf = fnt_title.render("HI SCORE TABLE", True, BLUE)
    img_rect =img_surf.get_rect()
    img_rect.topleft = (HALF_WINWIDTH -int((img_rect.width /2)), 40)
    DISPLAYSURF.blit(img_surf, img_rect)
    
    # add the cursor to the input box.
    img_surf = fnt_title.render("_", True, WHITE)
    img_rect =img_surf.get_rect()
    img_rect.topleft = (53, 100)
    DISPLAYSURF.blit(img_surf, img_rect)
    
    
    pygame.display.flip()

    events =pygame.event.get() # clear kbd and mouse buffer.
    
    while plyri !=K_ENTER:
        nc =False
        for event in pygame.event.get():
            if event.type == QUIT:
                #pygame.quit()
                #sys.exit()
                pass
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    #pygame.quit()
                    #sys.exit()
                    pass
                elif event.key ==K_ENTER:
                    plyri =K_ENTER
                    break
                elif event.key ==K_BACKSPC:
                    if len(pname) >1:
                        pname =pname[0:(len(pname) -1)]
                    else:
                        pname =""
                    nc =True
                elif chr(event.key) in ("_-0123456789abcdefghijklmnopqrstuvwxyz "):
                    # the player pressed an acceptable key for their name.
                    if len(pname) <20:
                        plyri =event.key
                        pname +=str.upper(chr(plyri))
                        nc =True
                else:
                    ## write some dubug info to the screen for the typed key.
                    #print("user pressed the key [", chr(event.key), "] asci code(", str(event.key), ").")
                    pass
                
        if nc ==True: # the player has altered his name.
            img_surf = fnt_title.render(pname + "_", True, WHITE)
            img_rect =img_surf.get_rect()
            img_rect.topleft = (53, 100)

            pygame.draw.rect(DISPLAYSURF, RED, (img_rect.x, img_rect.y, 500, img_rect.height))
            
            DISPLAYSURF.blit(img_surf, img_rect)
            pygame.display.flip()
            
    return pname
# playername_get() ----------------------------------------------------------



# ---------------------------------------------------------------------------
# Description:
#   Paints the player status panel used to display the status of the player.
#                                              
# Parameter(s):
#   tl          integer
#       Specifies the desired tl (time limit).
#
#   to          integer
#       When the timer was started.
# ---------------------------------------------------------------------------
def psp_paint(tl =0, to =0):
    psp_score_paint()
    psp_timer_paint(tl, to)
    psp_level_paint()
    psp_level_paint()
# panel_ply_status() --------------------------------------------------------



# ---------------------------------------------------------------------------
# Summary:
#   This routine is used remove the image of the level from the screen.
# ---------------------------------------------------------------------------
def psp_level_hide():
    boc =BLACK
    pygame.draw.rect(DISPLAYSURF, boc, [590, 100, 37, 30])
    #DISPLAYSURF.blit(img_surf, img_rect)
    
# psp_level_hide() --------------------------------------------------------------



# ---------------------------------------------------------------------------
# Summary:
#   This routine is used to paint the level on the screen.
# ---------------------------------------------------------------------------
def psp_level_paint():
##    # erase old images drawn within the area used to show the level number.
##    #   - set the default background colur to black.
##    boc =BLACK
##    pygame.draw.rect(DISPLAYSURF, boc, [590, 100, 37, 30])

    # render a new image of remaining time.
    x, y= 590, 100
    img_surf = fnt_main.render("Level", True, BLACK)
    img_rect = img_surf.get_rect()
    img_rect.topleft = (x -1, y)
    #x,y =img_rect.center
    DISPLAYSURF.blit(img_surf, img_rect)
    img_rect.topleft = (x +1, y)
    DISPLAYSURF.blit(img_surf, img_rect)
    img_rect.topleft = (x, y -1)
    DISPLAYSURF.blit(img_surf, img_rect)
    img_rect.topleft = (x, y +1)
    DISPLAYSURF.blit(img_surf, img_rect)
    
    img_surf = fnt_main.render("Level", True, WHITE)
    img_rect = img_surf.get_rect()
    img_rect.topleft = (x, y)
    x,y =img_rect.center
    DISPLAYSURF.blit(img_surf, img_rect)

    img_surf = fnt_main.render(str(glevel), True, WHITE)
    img_rect = img_surf.get_rect()
    #img_rect.topright = (635, 115)
    img_rect.center = (x, 125)
    DISPLAYSURF.blit(img_surf, img_rect)

# psp_level_paint()--------------------------------------------------------------



# ---------------------------------------------------------------------------
# Summary:
#   This routine is used to paint the stage/round on the screen.
# ---------------------------------------------------------------------------
def psp_round_paint():
    # erase old images drawn within the area used to draw the timer.
    #   - set the default background colur to black.
    boc =BLACK
    pygame.draw.rect(DISPLAYSURF, boc, [590, 150, 37, 30])

    # render a new image of remaining time.
    img_surf = fnt_main.render("Round", True, WHITE)
    img_rect = img_surf.get_rect()
    img_rect.topleft = (590, 150)
    x,y =img_rect.center
    DISPLAYSURF.blit(img_surf, img_rect)

    img_surf = fnt_main.render(str(gstagecntr), True, WHITE)
    img_rect = img_surf.get_rect()
    img_rect.center = (x, 175)
    DISPLAYSURF.blit(img_surf, img_rect)

# psp_round_paint()--------------------------------------------------------------



# ---------------------------------------------------------------------------
# Summary:
#   This routine adds some point to the player's score.
# ---------------------------------------------------------------------------
def psp_score_addpoints(tpoints =0, addcardval =True):
    global crdval, score

    if addcardval ==True:
        score +=crdval
        crdval +=crdval *2
    else:
        score +=tpoints
# psp_score_addpoints(~) ---------------------------------------------------------



# ---------------------------------------------------------------------------
# Summary:
#   This routine adds additional points to the player's score using the
#   remaining time as a guide.
# ---------------------------------------------------------------------------
def psp_score_addtime(tr):
    bp =psp_score_addtime_calc(tr) # calc the time bonus points.
    time_bonus =bp

    if bp  <=0:
        # player has zero bonus points.
        return False
        
    tl =2
    strmsg =str(bp) +" Time Bonus points"
    def_col=WHITE
    flash_msg =False
    pauselock =True
    pause_msg(tl, strmsg, def_col, flash_msg, pauselock)
    
    while bp >0: # there are more bonus points to add to the score
        bp -=1                      # reduce the number of bonus points.
        psp_score_addpoints(1, False)   # add a single bonus point to the score.
        psp_score_paint()               # paint the rendered score to the screen.

        tl =2
        strmsg =str(bp) +" Time Bonus points"
        def_col=WHITE
        flash_msg =False
        pauselock =True
        pause_msg(tl, strmsg, def_col, flash_msg, pauselock, pyield =True)

        #pygame.display.flip()
         
    return time_bonus
# psp_score_addtime(~) ------------------------------------------------------



# ---------------------------------------------------------------------------
# Summary:
#   This routine works out the number of bonus points to add to the score.
# ---------------------------------------------------------------------------
def psp_score_addtime_calc(tr):
    #global score

    time_bonus =(tr * (5 +glevel))
    #score +=time_bonus

    return time_bonus
# psp_score_addtime_calc(~) -------------------------------------------------



# ---------------------------------------------------------------------------
# Summary:
#   This routine paints the score on the screen.
# ---------------------------------------------------------------------------
def psp_score_paint():

    y =0
    lm =1       # set the line margin.

    x,y =590, 0

    # > Paint a black border around the caption score.
    img_surf = fnt_main.render("Score", True, BLACK)
    img_rect = img_surf.get_rect()
    img_rect.topleft = (x-1, y)
    DISPLAYSURF.blit(img_surf, img_rect)
    img_rect.topleft = (x+1, y)
    DISPLAYSURF.blit(img_surf, img_rect)
    img_rect.topleft = (x, y-1)
    DISPLAYSURF.blit(img_surf, img_rect)
    img_rect.topleft = (x, y+1)
    DISPLAYSURF.blit(img_surf, img_rect)
    # .

    # > Paint the score caption over the blacked out borders
    img_surf = fnt_main.render("Score", True, WHITE)
    img_rect = img_surf.get_rect()
    img_rect.topleft = (x, y)
    DISPLAYSURF.blit(img_surf, img_rect)
    # .
    
    # get ready to paint on the next line.
    y +=img_rect.height
    y +=lm
    
    ## erase the previous displayed number.
    #imgwidth =img_rect.width
    #pygame.draw.rect(DISPLAYSURF, BLACK, (590, y, imgwidth, img_rect.height))
    # no need to black out the section of screen any more because we are
    # using a background image.
    
    img_surf = fnt_main.render(str(score), True, WHITE)
    img_rect = img_surf.get_rect()
    #img_rect.center = (610, y)
    #img_rect.topleft =(img_rect.x, y)
    img_rect.topright =(635, y)
    
    DISPLAYSURF.blit(img_surf, img_rect)
# psp_score_paint() -------------------------------------------------------------
 

   
# ---------------------------------------------------------------------------
# Summary:
#   This routine removes the timer image from the screen.
# ---------------------------------------------------------------------------
def psp_timer_hide():
    img_surf = fnt_main.render("Time", True, WHITE)
    img_rect = img_surf.get_rect()

    pygame.draw.rect(DISPLAYSURF, BLACK, [590, 40, img_rect.width, img_rect.height])
    pygame.draw.rect(DISPLAYSURF, BLACK, [590, 60, 37, 30])
# psp_timer_hide() --------------------------------------------------------------


# ---------------------------------------------------------------------------
# Summary:
#   This routine is used to paint the timer on the screen.
# ---------------------------------------------------------------------------
def psp_timer_paint(tl, to, def_col=GREEN, lti =True):
    tr =tl -int(time.time() -to) # calcualate the remaining time.

    rgb_caption =WHITE  # set the default colour of the timer caption
    
    # erase old images drawn within the area used to draw the timer.
    if lti ==True:
        # the low time indicator should be used when the remaining
        # time falls below a certain level.
        if tr <3:
            # make the background flash.
            if tr % 2 ==0:
                #boc =RED    # block out colour.
                rgb_caption =RED
            else:
                #boc =BLACK
                pass
        else:
            #boc =BLACK  # block out colour.
            pass
    else:
        ## set the default background colur to black.
        #boc =BLACK
        pass

    #pygame.draw.rect(DISPLAYSURF, boc, [590, 70, 37, 30])

    # render a new image of remaining time.
    #   -   paint a black border where the caption will be
    #       so the text stands out and can be seen.
    #
    #   -   paint the time caption over the blacked out
    #       border.
    x,y =590, 50
    img_surf = fnt_main.render("Time", True, BLACK)
    img_rect = img_surf.get_rect()
    img_rect.topleft = (x-1, y)
    DISPLAYSURF.blit(img_surf, img_rect)
    img_rect.topleft = (x+1, y)
    DISPLAYSURF.blit(img_surf, img_rect)
    img_rect.topleft = (x, y-1)
    DISPLAYSURF.blit(img_surf, img_rect)
    img_rect.topleft = (x, y+1)
    DISPLAYSURF.blit(img_surf, img_rect)
    
    #img_surf = fnt_main.render("Time", True, WHITE)
    img_surf = fnt_main.render("Time", True, rgb_caption)
    img_rect = img_surf.get_rect()
    img_rect.topleft = (590, 50)
    DISPLAYSURF.blit(img_surf, img_rect)

    # paint the time remaining only if its larger than zero.
    #tmr_str =str(tl -int(to -time.time()))
    #tmr_str =str(tr)
    if tr >=0: 
        tmr_str =str(tr)
        img_surf = fnt_main.render(tmr_str, True, def_col)
        img_rect = img_surf.get_rect()
        img_rect.center = (610, 80)
        DISPLAYSURF.blit(img_surf, img_rect)

    
    return tr # return the remaining time.
# psp_timer_paint(~) --------------------------------------------------------


# ---------------------------------------------------------------------------
# Description:
#   define a structure to help deal with the numerous card placement
#   holders (cph) positions (places on the screen).
# ---------------------------------------------------------------------------
def stype_cph():
    x =0
    y =0
    status =0
# stype_cph() ---------------------------------------------------------------
    


# ---------------------------------------------------------------------------
# Description:
#   I am a little unsure of how to resolve the issue that not all computers
#   will have access to the espeak library, so I built this routine in an
#   attempt to trap the error of not having the library available, but still
#   permitting it to run the game without having to comment out all the
#   statements by hand.
#
# Summary:
#   I designed this wrapper routine to make it easier to trap errors when
#   working with the speach synth from "espeak".
# ---------------------------------------------------------------------------
def wr_say(voice):
    global ife_wr_say # ife (ignore further error) flag
    
    #if not "str" in str(type(voice)):
    if not isinstance(voice, str):
        # I don't think we can work with anything other than strings,
        # so lets exit this routine.
        return false
        
    try:
        espeak.synth(voice)
        return True
    except:
        # something went wrong when trying to calling the a routine in
        # espeak.
        if ife_wr_say ==False:
            # this is the 1st instance of the msg being displayed.
            print("")
            print("*********************************************************")
            print("                     WARNING")
            print(" Something went wrong when trying to calling a routine")
            print(" from the espeak library.")
            print("")
            print(" Its not fatal but it probably means you won't hear any")
            print(" comands/prompts from the computer voice.")
            print(" ********************************************************")
            ife_wr_say =True # ignore further errors.
            
# wr_say( ~ ) ---------------------------------------------------------------






catx = 10
caty = 10
direction = 'right'

fnt_main = pygame.font.Font('freesansbold.ttf', 16)
fnt_title = 0

# prepare variables that will be used to play sounds.
click_sound ="%?"   # default sound of a card being turned over.
snd_send_ok ="%?"   # successful stage end sound.
snd_send_fail ="%?" # failed stage ending sound.
snd_lbegin ="%?"    # level begining sound.
snd_gintro ="%?%"   # game intro sound.
snd_gend ="%?%"     # end game sound.
snd_tmrl ="%?%"     # timers low time remaining.



gstagecntr =0
glevel =0
retval =False
end_stage =False
card_next =1
card_total =0 # the number of cards the player needs to turn over.
tmr_str =""

game_init() # initialise the game.

exitgame =False
while exitgame ==False:
    #play_title_screen()
    
    game_begin()
    play_title_screen()

    #print( playername_get() )
    
    ls =True # trigger flag so we can enter loop.
    while ls ==True:
        
        tsil = (glevel * 2)     # calc total stages in level.
        
        level_ini()
        level_begin()
        ls =level_play()
        level_end()

        glevel +=1

    #score +=1000   # add cheat so we can get on the high score table.
    
    if score >hstable_min_get(): # we have a new high score
        new_name =playername_get()
        hstable_insert(new_name, score)
        hstable_save()  # save the hs table.
        
    game_end()
    

print("Player scored ", score)
# ---------------------------------------------------------------------------

   



### ---------------------------------------------------------------------------
### move the card around the screen
##while True: # the main game loop
##    DISPLAYSURF.fill(BLACK)
##    
##    if direction == 'right':
##        catx += 5
##        if catx == 280:
##            direction = 'down'
##    elif direction == 'down':
##        caty += 5
##        if caty == 220:
##            direction = 'left'
##    elif direction == 'left':
##        catx -= 5
##        if catx == 10:
##            direction = 'up'
##    elif direction == 'up':
##        caty -= 5
##        if caty == 10:
##            direction = 'right'
##            
##
##    
##    # paint a card image to the graphics buffer.
##    DISPLAYSURF.blit(cardimages[ 3 ], (catx, caty))
##    
##    # scan input devices to check for user input.
##    for event in pygame.event.get():
##        if event.type == QUIT:
##            # a close request on the window was made.
##            pygame.quit()
##            sys.exit()
##        elif event.type == KEYDOWN:
##            if event.key == K_ESCAPE:
##                pygame.quit()
##                sys.exit()
##            
##    #pygame.display.update()
##    pygame.display.flip()
##    fpsClock.tick(FPS)
