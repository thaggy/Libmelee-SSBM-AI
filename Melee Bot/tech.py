import melee

def fox_multishine(ai_state, controller):
    """ Frame-perfect Multishines as Fox """
    #If standing, shine
    if ai_state.action == melee.enums.Action.STANDING:
        controller.press_button(melee.enums.Button.BUTTON_B)
        controller.tilt_analog(melee.enums.Button.BUTTON_MAIN, .5, 0)
        return

    #Shine on frame 3 of knee bend, else nothing
    if ai_state.action == melee.enums.Action.KNEE_BEND:
        if ai_state.action_frame == 1:
            controller.press_button(melee.enums.Button.BUTTON_B)
            controller.tilt_analog(melee.enums.Button.BUTTON_MAIN, .5, 0)
            return
        controller.release_all()
        return

    shine_start = (ai_state.action == melee.enums.Action.DOWN_B_STUN or
                   ai_state.action == melee.enums.Action.DOWN_B_GROUND_START)

    #Jump out of shine
    if shine_start and ai_state.action_frame >= 4 and ai_state.on_ground:
        controller.press_button(melee.enums.Button.BUTTON_Y)
        return

    if ai_state.action ==melee.enums.Action.DOWN_B_GROUND:
        controller.press_button(melee.enums.Button.BUTTON_Y)
        return

    controller.release_all()

def falco_multishine(ai_state, controller):
    """ Frame-perfect Multishines as Falco """
    #If standing, shine
    if ai_state.action == melee.enums.Action.STANDING:
        controller.press_button(melee.enums.Button.BUTTON_B)
        controller.tilt_analog(melee.enums.Button.BUTTON_MAIN, .5, 0)
        return

    #Shine on knee bend, else nothing
    if ai_state.action == melee.enums.Action.KNEE_BEND:
        if ai_state.action_frame == 3:
            controller.press_button(melee.enums.Button.BUTTON_B)
            controller.tilt_analog(melee.enums.Button.BUTTON_MAIN, .5, 0)
            return
        controller.release_all()
        return

    shine_start = (ai_state.action == melee.enums.Action.DOWN_B_STUN or
                   ai_state.action == melee.enums.Action.DOWN_B_GROUND_START)

    #Jump out of shine
    if shine_start and ai_state.action_frame >= 4 and ai_state.on_ground:
        controller.press_button(melee.enums.Button.BUTTON_Y)
        return

    if ai_state.action ==melee.enums.Action.DOWN_B_GROUND:
        controller.press_button(melee.enums.Button.BUTTON_Y)
        return

    controller.release_all()

def marth_counter(ai_state, controller):
    counter_state =  (ai_state.action == melee.enums.Action.MARTH_COUNTER or 
                      ai_state.action == melee.enums.Action.MARTH_COUNTER_FALLING or
                      ai_state.action == melee.enums.Action.PARASOL_FALLING)
    if counter_state:
        print("Detecting counter state, releasing buttons")
        controller.release_all()
    else:
        print("Counter state not detected, pressing Down B")
        controller.press_button(melee.enums.Button.BUTTON_B)
        controller.tilt_analog(melee.enums.Button.BUTTON_MAIN, .5, 0)
