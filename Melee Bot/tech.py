import melee
from melee.enums import Action, Button, Character

class Tech:
    """
    Tech class, an instance of this makes it easier to call all of the functions essentially. I honestly just made this into a class 
    just so I had to type less.
    """
    def __init__(self, ai_state, human_state, controller):
        self.ai_state = ai_state
        self.human_state = human_state
        self.controller = controller

    def jump_cancel_frames(self):
        """
        returns number of frames (int) when the character should be pressing another input to jump cancel (This was found by taking their jumpsquat animation and
        subtracting 2, for some reason I found that this always worked better) 

        This is easily modifyable if someone finds that this number does not work for them as it did for me

        Arguments:
        ai_state (gamestate.controller[ai_port])
        """
        if self.ai_state.character == Character.FOX or self.ai_state.character == Character.POPO or self.ai_state.character == Character.KIRBY  or \
        self.ai_state.character == Character.SAMUS or self.ai_state.character == Character.SHEIK or self.ai_state.character == Character.PICHU or \
        self.ai_state.character == Character.PICHU:
            return 1
        elif self.ai_state.character == Character.DOC or self.ai_state.character == Character.MARIO or self.ai_state.character == Character.LUIGI or \
        self.ai_state.character == Character.CPTFALCON or self.ai_state.character == Character.YLINK or self.ai_state.character == Character.NESS or \
        self.ai_state.character == Character.MARTH or self.ai_state.character == Character.GAMEANDWATCH:
            return 2
        elif self.ai_state.character == Character.FALCO or self.ai_state.character == Character.PEACH or self.ai_state.character == Character.YOSHI or \
        self.ai_state.character == Character.DK or self.ai_state.character == Character.JIGGLYPUFF or self.ai_state.character == Character.MEWTWO or \
        self.ai_state.character == Character.ROY:
            return 3
        elif self.ai_state.character == Character.GANONDORF or self.ai_state.character == Character.ZELDA or self.ai_state.character == Character.LINK:
            return 4
        elif self.ai_state.character == Character.BOWSER:
            return 6

    def isFoxOrFalco(self):
        """
        same as jump_cancel_frames except it is only for Fox or Falco for efficiency

        returns 3 if Falco (or rather not Fox), 1 if Fox (This is because this is the frame needed to jump for wavedash/waveshining)
        """
        if self.ai_state.character == Character.FOX:
            return 1
        return 3

    def multishine(self):
        """ 
        Frame-perfect Multishines as either Fox or Falco
        """
        #If standing, shine
        if self.ai_state.action == Action.STANDING:
            self.controller.press_button(Button.BUTTON_B)
            self.controller.tilt_analog(Button.BUTTON_MAIN, .5, 0)
            return

        #Shine on frame 3 of knee bend, else nothing
        if self.ai_state.action == Action.KNEE_BEND:
            if self.ai_state.action_frame == self.isFoxOrFalco():
                self.controller.press_button(Button.BUTTON_B)
                self.controller.tilt_analog(Button.BUTTON_MAIN, .5, 0)
                return
            self.controller.release_all()
            return

        shine_start = (self.ai_state.action == Action.DOWN_B_STUN or
                       self.ai_state.action == Action.DOWN_B_GROUND_START)

        #Jump out of shine
        if shine_start and self.ai_state.action_frame >= 4 and self.ai_state.on_ground:
            self.controller.press_button(Button.BUTTON_Y)
            return

        if self.ai_state.action == Action.DOWN_B_GROUND:
            self.controller.press_button(Button.BUTTON_Y)
            return

        self.controller.release_all()

    def wavedash(self, towards = True):
        """
        performs frameperfect wavedash, this can be either towards or away from the opponent, (False if away, True or no argument if towards)
        This works regardless of character in use
        Arguments:
        (optional) Towards (boolean)
        """
        if self.ai_state == melee.enums.Action.SHIELD_STUN:
            self.controller.empty_input()
            return
        if self.ai_state.off_stage:
            self.controller.empty_input()
            return
        IsShineStart = self.ai_state.action in [melee.enums.Action.DOWN_B_STUN, melee.enums.Action.DOWN_B_GROUND, melee.enums.Action.DOWN_B_GROUND_START]
        if IsShineStart and self.ai_state.action_frame >= 3 and self.ai_state.on_ground:
            self.controller.press_button(melee.enums.Button.BUTTON_Y)
            return

        isShielding = self.ai_state.action in [Action.SHIELD_START, Action.SHIELD, \
           Action.SHIELD_RELEASE, Action.SHIELD_STUN, Action.SHIELD_REFLECT]
        isNeutral = self.ai_state.action in [Action.STANDING, Action.DASHING, Action.TURNING, \
            Action.RUNNING, Action.EDGE_TEETERING_START, Action.EDGE_TEETERING]
        jumpcancel = (self.ai_state.action == Action.KNEE_BEND) and (self.ai_state.action_frame >= self.jump_cancel_frames())
        jumping = [Action.JUMPING_ARIAL_FORWARD, Action.JUMPING_ARIAL_BACKWARD]

        if isShielding or isNeutral:
            if self.controller.prev.button[Button.BUTTON_Y]:
                self.controller.empty_input()
                return
            self.controller.press_button(Button.BUTTON_Y)
            return

        if jumpcancel or self.ai_state.action in jumping:
            self.controller.press_button(Button.BUTTON_L)
            onLeft = self.ai_state.position.x < self.human_state.position.x
            x = -1
            if onLeft == towards:
                x = 1
            self.controller.tilt_analog(Button.BUTTON_MAIN, x, .35)
            return

        if self.ai_state.action == Action.LANDING_SPECIAL:
            self.controller.empty_input()
            return

        self.controller.empty_input()


    def waveshine(self, towards = True):
        """
        performs frameperfect waveshine, this can be either towards or away from the opponent, (False if away, True or no argument if towards)
    
        Arguments:
        (optional) Towards (boolean)
        """
        if self.ai_state == melee.enums.Action.SHIELD_STUN:
            self.controller.empty_input()
            return
        if self.ai_state.off_stage:
            self.controller.empty_input()
            return
        IsShineStart = self.ai_state.action in [melee.enums.Action.DOWN_B_STUN, melee.enums.Action.DOWN_B_GROUND, melee.enums.Action.DOWN_B_GROUND_START]
        if IsShineStart and self.ai_state.action_frame >= 3 and self.ai_state.on_ground:
            self.controller.press_button(melee.enums.Button.BUTTON_Y)
            return

        isShielding = self.ai_state.action in [Action.SHIELD_START, Action.SHIELD, \
           Action.SHIELD_RELEASE, Action.SHIELD_STUN, Action.SHIELD_REFLECT]
        isNeutral = self.ai_state.action in [Action.STANDING, Action.DASHING, Action.TURNING, \
            Action.RUNNING, Action.EDGE_TEETERING_START, Action.EDGE_TEETERING]
        jumpcancel = (self.ai_state.action == Action.KNEE_BEND) and (self.ai_state.action_frame >= self.isFoxOrFalco())
        jumping = [Action.JUMPING_ARIAL_FORWARD, Action.JUMPING_ARIAL_BACKWARD]

        if isShielding:
            if self.controller.prev.button[Button.BUTTON_Y]:
                self.controller.empty_input()
                return
            self.controller.press_button(Button.BUTTON_Y)
            return

        if isNeutral:
            if self.controller.prev.button[Button.BUTTON_B]:
                self.controller.empty_input()
                return
            self.controller.tilt_analog(Button.BUTTON_MAIN, .5, 0)
            self.controller.press_button(Button.BUTTON_B)
            return

        if jumpcancel or self.ai_state.action in jumping:
            self.controller.press_button(Button.BUTTON_L)
            onLeft = self.ai_state.position.x < self.human_state.position.x
            x = -1
            if onLeft == towards:
                x = 1
            self.controller.tilt_analog(Button.BUTTON_MAIN, x, .35)
            return

        if self.ai_state.action == Action.LANDING_SPECIAL:
            self.controller.empty_input()
            return

        self.controller.empty_input()