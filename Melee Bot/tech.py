import melee
from melee.enums import Action, Button, Character

def jump_cancel_frames(ai_state):
    """
    returns number of frames (int) when the character should be pressing another input to jump cancel (This was found by taking their jumpsquat animation and
    subtracting 2, for some reason I found that this always worked better) 

    This is easily modifyable if someone finds that this number does not work for them as it did for me

    Arguments:
    ai_state (gamestate.controller[ai_port])
    """
    if ai_state.character == Character.FOX or ai_state.character == Character.POPO or ai_state.character == Character.KIRBY  or \
    ai_state.character == Character.SAMUS or ai_state.character == Character.SHEIK or ai_state.character == Character.PICHU or \
    ai_state.character == Character.PICHU:
        return 1
    elif ai_state.character == Character.DOC or ai_state.character == Character.MARIO or ai_state.character == Character.LUIGI or \
    ai_state.character == Character.CPTFALCON or ai_state.character == Character.YLINK or ai_state.character == Character.NESS or \
    ai_state.character == Character.MARTH or ai_state.character == Character.GAMEANDWATCH:
        return 2
    elif ai_state.character == Character.FALCO or ai_state.character == Character.PEACH or ai_state.character == Character.YOSHI or \
    ai_state.character == Character.DK or ai_state.character == Character.JIGGLYPUFF or ai_state.character == Character.MEWTWO or \
    ai_state.character == Character.ROY:
        return 3
    elif ai_state.character == Character.GANONDORF or ai_state.character == Character.ZELDA or ai_state.character == Character.LINK:
        return 4
    elif ai_state.character == Character.BOWSER:
        return 6

def isFoxOrFalco(ai_state):
    """
    same as jump_cancel_frames except it is only for Fox or Falco for efficiency

    returns 3 if Falco (or rather not Fox), 1 if Fox (This is because this is the frame needed to jump for wavedash/waveshining)
    """
    if ai_state.character == Character.FOX:
        return 1
    return 3

def multishine(ai_state, controller):
    """ 
    Frame-perfect Multishines as either Fox or Falco
    
    Arguments
    ai_state (gamestate.players[ai_port])
    controller (melee.Controller(console=console, port=self.ai_port) or meleeManager.ai_controller)
    """
    #If standing, shine
    if ai_state.action == melee.enums.Action.STANDING:
        controller.press_button(melee.enums.Button.BUTTON_B)
        controller.tilt_analog(melee.enums.Button.BUTTON_MAIN, .5, 0)
        return

    #Shine on frame 3 of knee bend, else nothing
    if ai_state.action == melee.enums.Action.KNEE_BEND:
        if ai_state.action_frame == isFoxorFalco(ai_state):
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
    """ 
    Frame-perfect Multishines as Falco 
    Deprecated, replaced with just multishine (That function checks for either fox or falco)
    """
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

def wavedash(ai_state, controller, human_state, towards = True):
    """
    performs frameperfect wavedash, this can be either towards or away from the opponent, (False if away, True or no argument if towards)
    This works regardless of character in use
    Arguments:
    ai_state (gamestate.players[ai_port])
    controller (melee.Controller(console=console, port=self.ai_port) or manager.ai_controller)
    human_state (gamestate.players[human_port])
    (optional) Towards (boolean)
    """
    if ai_state == melee.enums.Action.SHIELD_STUN:
        controller.empty_input()
        return
    if ai_state.off_stage:
        controller.empty_input()
        return
    IsShineStart = ai_state.action in [melee.enums.Action.DOWN_B_STUN, melee.enums.Action.DOWN_B_GROUND, melee.enums.Action.DOWN_B_GROUND_START]
    if IsShineStart and ai_state.action_frame >= 3 and ai_state.on_ground:
        controller.press_button(melee.enums.Button.BUTTON_Y)
        return

    isShielding = ai_state.action in [Action.SHIELD_START, Action.SHIELD, \
       Action.SHIELD_RELEASE, Action.SHIELD_STUN, Action.SHIELD_REFLECT]
    isNeutral = ai_state.action in [Action.STANDING, Action.DASHING, Action.TURNING, \
        Action.RUNNING, Action.EDGE_TEETERING_START, Action.EDGE_TEETERING]
    jumpcancel = (ai_state.action == Action.KNEE_BEND) and (ai_state.action_frame >= jump_cancel_frames(ai_state))
    jumping = [Action.JUMPING_ARIAL_FORWARD, Action.JUMPING_ARIAL_BACKWARD]

    if isShielding or isNeutral:
        if controller.prev.button[Button.BUTTON_Y]:
            controller.empty_input()
            return
        controller.press_button(Button.BUTTON_Y)
        return

    if jumpcancel or ai_state.action in jumping:
        controller.press_button(Button.BUTTON_L)
        onLeft = ai_state.position.x < human_state.position.x
        x = -1
        if onLeft == towards:
            x = 1
        controller.tilt_analog(Button.BUTTON_MAIN, x, .35)
        return

    if ai_state.action == Action.LANDING_SPECIAL:
        controller.empty_input()
        return

    controller.empty_input()


def waveshine(ai_state, controller, human_state, towards = True):
    """
    performs frameperfect waveshine, this can be either towards or away from the opponent, (False if away, True or no argument if towards)
    
    Arguments:
    ai_state (gamestate.players[ai_port])
    controller (melee.Controller(console=console, port=self.ai_port) or manager.ai_controller)
    human_state (gamestate.players[human_port])
    (optional) Towards (boolean)
    """
    if ai_state == melee.enums.Action.SHIELD_STUN:
        controller.empty_input()
        return
    if ai_state.off_stage:
        controller.empty_input()
        return
    IsShineStart = ai_state.action in [melee.enums.Action.DOWN_B_STUN, melee.enums.Action.DOWN_B_GROUND, melee.enums.Action.DOWN_B_GROUND_START]
    if IsShineStart and ai_state.action_frame >= 3 and ai_state.on_ground:
        controller.press_button(melee.enums.Button.BUTTON_Y)
        return

    isShielding = ai_state.action in [Action.SHIELD_START, Action.SHIELD, \
       Action.SHIELD_RELEASE, Action.SHIELD_STUN, Action.SHIELD_REFLECT]
    isNeutral = ai_state.action in [Action.STANDING, Action.DASHING, Action.TURNING, \
        Action.RUNNING, Action.EDGE_TEETERING_START, Action.EDGE_TEETERING]
    jumpcancel = (ai_state.action == Action.KNEE_BEND) and (ai_state.action_frame >= isFoxOrFalco(ai_state))
    jumping = [Action.JUMPING_ARIAL_FORWARD, Action.JUMPING_ARIAL_BACKWARD]

    if isShielding:
        if controller.prev.button[Button.BUTTON_Y]:
            controller.empty_input()
            return
        controller.press_button(Button.BUTTON_Y)
        return

    if isNeutral:
        if controller.prev.button[Button.BUTTON_B]:
            controller.empty_input()
            return
        controller.tilt_analog(Button.BUTTON_MAIN, .5, 0)
        controller.press_button(Button.BUTTON_B)
        return

    if jumpcancel or ai_state.action in jumping:
        controller.press_button(Button.BUTTON_L)
        onLeft = ai_state.position.x < human_state.position.x
        x = -1
        if onLeft == towards:
            x = 1
        controller.tilt_analog(Button.BUTTON_MAIN, x, .35)
        return

    if ai_state.action == Action.LANDING_SPECIAL:
        controller.empty_input()
        return

    controller.empty_input()