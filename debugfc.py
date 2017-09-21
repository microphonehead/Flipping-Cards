

# ---------------------------------------------------------------------------
# Description:
#   This is a routine used for debugging.
#
#   It prints the elements of the cards object.
# ---------------------------------------------------------------------------
def cards_debug_print():
    global cards
    
    cntr =0

    print()
    print("DEBUG info - cards object")
    print("-------------------------")
    print("     header info:")
    print("         array size =", len(cards))
    
    for cntr in range(0, len(cards)):
        crd =cards[cntr]
        print("({}). card number is {}.".format(cntr, crd.num))
        cntr +=1

    print("")
# ---------------------------------------------------------------------------



# ---------------------------------------------------------------------------
# Summary:
#   This rountine list the attributes and their values for the hst obj.
# ---------------------------------------------------------------------------#
def debug_hst(hst =[]):
#def debug_hst():
    #global hst

    cntr =0
    print("DEBUG - hst (obj)")
    for pname, pscore in hst:
        #if cntr >0:
            #print("-")
        print("[", cntr, end ="] - ")
        #print(" name= ", pname)
        #print(" score= ", pscore)
        print(" name:[{0:40}] ==> score:[{1:10}]".format(pname, pscore))
        cntr +=1

    print("END DEBUG - hst")
    print()
    
# ---------------------------------------------------------------------------#



# ---------------------------------------------------------------------------
# Description:
#   This is a routine used for debugging.
#
#   It prints the elements of the deck object.
# ---------------------------------------------------------------------------
def deck_debug_print(msginfo =""):
    global deck
    
    cntr =0

    print()
    print("DEBUG info - deck object")
    print("-------------------------")
    print("     header info:")
    print("         array size =", len(deck))
    if msginfo != "":
        print("     msg info: ", msginfo)
        
    for cntr in range(0, len(deck)):
        crd =deck[cntr]
        print("({}). card number is {}.".format(cntr, crd.num))
        cntr +=1

    print("")
# ---------------------------------------------------------------------------

