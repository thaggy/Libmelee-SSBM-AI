import melee
from melee.enums import Action, Button

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

def wavedash(ai_state, controller, human_state):
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
    jumpcancel = (ai_state.action == Action.KNEE_BEND) and (ai_state.action_frame >= 1)
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
        if onLeft:
            x = 1
        controller.tilt_analog(Button.BUTTON_MAIN, x, .35)
        return

    if ai_state.action == Action.LANDING_SPECIAL:
        controller.empty_input()
        return

    controller.empty_input()


def waveshine_WIP2(ai_state, controller, human_state):
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
    jumpcancel = (ai_state.action == Action.KNEE_BEND) and (ai_state.action_frame >= 1)
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
        if onLeft:
            x = 1
        controller.tilt_analog(Button.BUTTON_MAIN, x, .35)
        return

    if ai_state.action == Action.LANDING_SPECIAL:
        controller.empty_input()
        return

    controller.empty_input()

def waveshine_WIP(ai_state, controller, human_state, gamestate):
    shineablestates = [Action.TURNING, Action.STANDING, Action.WALK_SLOW, Action.WALK_MIDDLE, \
            Action.WALK_FAST, Action.EDGE_TEETERING_START, Action.EDGE_TEETERING, Action.CROUCHING, \
            Action.RUNNING, Action.RUN_BRAKE, Action.CROUCH_START, Action.CROUCH_END, Action.SHIELD_RELEASE]
    jcshine = (ai_state.action == Action.KNEE_BEND) and (ai_state.action_frame == 3)
    lastdashframe = (ai_state.action == Action.DASHING) and (ai_state.action_frame == 12)
    landing_over = (ai_state.action == Action.LANDING) and (ai_state.action_frame >= 4)

    if ai_state.action == Action.DOWN_B_AIR:
        controller.empty_input()
        return
    if ai_state.off_stage:
        controller.empty_input()
        return
    #TODO: Detect no longer powershielding
    if ai_state.action  == Action.SHIELD_RELEASE:
        controller.press_button(Button.BUTTON_Y)
        return
    if ai_state.action in shineablestates or lastdashframe or jcshine or landing_over:
        print("here")
        controller.press_button(Button.BUTTON_B)
        controller.tilt_analog(Button.BUTTON_MAIN, .5, 0)
        return

    if jcshine and gamestate.distance < 11.8 and human_state.hitlag_left == 0 and human_state.hitstun_frames_left == 0:
        controller.press_button(Button.BUTTON_B)
        controller.tilt_analog(Button.BUTTON_MAIN, .5, 0)
        return
    
    if ai_state.action == Action.KNEE_BEND and ai_state.action_frame < 3:
        controller.empty_input()
        return

    if ai_state.action == Action.DASHING:
        controller.release_button(Button.BUTTON_B)
        controller.tilt_analog(Button.Button_Main, int(not ai_state.facing), .5)
        return

    isInShineStart = ai_state.action in [Action.DOWN_B_GROUND_START, Action.DOWN_B_GROUND]
    needsJC = ai_state.action in [Action.SHIELD, Action.TURNING_RUN]
    
    if needsJC or (ai_state.action == Action.TURNING and ai_state.action_frame in range(2,12)):
        if controller.prev.button[Button.BUTTON_Y]:
            controller.empty_input()
            return
        controller.press_button(Button.BUTTON_Y)
        return

    if isInShineStart:
        if ai_state.action_frame >= 3:
            controller.press_button(Button.BUTTON_Y)
            return

    jumping = [Action.JUMPING_ARIAL_FORWARD, Action.JUMPING_ARIAL_BACKWARD]

    if jcshine or ai_state.action in jumping:
        print("doing wavedash")
        controller.press_buton(Button.BUTTON_L)
        humanspeed = human_state.spseed_x_attack + human_state.speed_ground_x_self
        direction = opponentspeed > 0
        onLeft = ai_state.position.x < opponent_state.position.x
        if abs(opponentspeed < 0.01):
            direction = onLeft

        edge_x = melee.stages.EDGE_GROUND_POSITION(gamestate.stage)
        if ai_state.position.x < 0:
            edge_x = -edge_x
        edgedistance = abs(edge_x - ai_state.position)
        if edgedistance < 0.5:
            direction = ai_state.position.x < 0
        x = .5
        facinginwards = ai_state.facing == (ai_state.position.x < 0)
        moving_out = direction == (0 < ai_state.position.x)
        if edgedistance < 18.5 and moving_out and not facinginwards:
            x = 0
        delta = (x/2)
        if not direction:
            delta = -delta
        controller.tilt_analog(Button.BUTTON_MAIN, .5 + delta, .35)
        return
    
    if ai_state.action == Action.LANDING_SPECIAL:
        controller.empty_input()
        return

    controller.empty_input()