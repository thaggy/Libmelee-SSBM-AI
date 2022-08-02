import melee
from melee.enums import Action, Button, Character

class Tech:
    """
    Presses buttons and checks action frames in order to execute techniques
    """
    neutral = [Action.STANDING, Action.DASHING, Action.TURNING, \
            Action.RUNNING, Action.EDGE_TEETERING_START, Action.EDGE_TEETERING]
    edge = [Action.EDGE_HANGING, Action.EDGE_CATCHING, Action.EDGE_GETUP_SLOW, \
        Action.EDGE_GETUP_QUICK, Action.EDGE_ATTACK_SLOW, Action.EDGE_ATTACK_QUICK, Action.EDGE_ROLL_SLOW, Action.EDGE_ROLL_QUICK]
    onEdge = [Action.EDGE_HANGING, Action.EDGE_CATCHING]

    def __init__(self, ai_state, human_state, controller, stage):
        self.ai = ai_state
        self.human = human_state
        self.controller = controller
        self.stage = stage

    def jump_cancel_frames(self):
        """
        returns number of frames (int) when the character should be pressing another input to jump cancel (This was found by taking their jumpsquat animation and
        subtracting 2, for some reason I found that this always worked better) 

        This is easily modifyable if someone finds that this number does not work for them as it did for me
        """
        if self.ai.character == Character.FOX or self.ai.character == Character.POPO or self.ai.character == Character.KIRBY  or \
        self.ai.character == Character.SAMUS or self.ai.character == Character.SHEIK or self.ai.character == Character.PICHU or \
        self.ai.character == Character.PICHU:
            return 1
        elif self.ai.character == Character.DOC or self.ai.character == Character.MARIO or self.ai.character == Character.LUIGI or \
        self.ai.character == Character.CPTFALCON or self.ai.character == Character.YLINK or self.ai.character == Character.NESS or \
        self.ai.character == Character.MARTH or self.ai.character == Character.GAMEANDWATCH:
            return 2
        elif self.ai.character == Character.FALCO or self.ai.character == Character.PEACH or self.ai.character == Character.YOSHI or \
        self.ai.character == Character.DK or self.ai.character == Character.JIGGLYPUFF or self.ai.character == Character.MEWTWO or \
        self.ai.character == Character.ROY:
            return 3
        elif self.ai.character == Character.GANONDORF or self.ai.character == Character.ZELDA or self.ai.character == Character.LINK:
            return 4
        elif self.ai.character == Character.BOWSER:
            return 6

    def isFoxOrFalco(self):
        """
        same as jump_cancel_frames except it is only for Fox or Falco for efficiency

        returns 3 if Falco (or rather not Fox), 1 if Fox (This is because this is the frame needed to jump for wavedash/waveshining)
        """
        if self.ai.character == Character.FOX:
            return 1
        return 3

    def multishine(self):
        """ 
        Frame-perfect Multishines as either Fox or Falco
        """
        #If standing, shine
        if self.ai.action == Action.STANDING:
            self.controller.press_button(Button.BUTTON_B)
            self.controller.tilt_analog(Button.BUTTON_MAIN, .5, 0)
            return

        #Shine on frame 3 of knee bend, else nothing
        if self.ai.action == Action.KNEE_BEND:
            if self.ai.action_frame == self.isFoxOrFalco():
                self.controller.press_button(Button.BUTTON_B)
                self.controller.tilt_analog(Button.BUTTON_MAIN, .5, 0)
                return
            self.controller.release_all()
            return

        shine_start = (self.ai.action == Action.DOWN_B_STUN or
                       self.ai.action == Action.DOWN_B_GROUND_START)

        #Jump out of shine
        if shine_start and self.ai.action_frame >= 4 and self.ai.on_ground:
            self.controller.press_button(Button.BUTTON_Y)
            return

        if self.ai.action == Action.DOWN_B_GROUND:
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
        if self.ai == melee.enums.Action.SHIELD_STUN:
            self.controller.empty_input()
            return
        if self.ai.off_stage:
            self.controller.empty_input()
            return
        IsShineStart = self.ai.action in [melee.enums.Action.DOWN_B_STUN, melee.enums.Action.DOWN_B_GROUND, melee.enums.Action.DOWN_B_GROUND_START]
        if IsShineStart and self.ai.action_frame >= 3 and self.ai.on_ground:
            self.controller.press_button(melee.enums.Button.BUTTON_Y)
            return

        isShielding = self.ai.action in [Action.SHIELD_START, Action.SHIELD, \
           Action.SHIELD_RELEASE, Action.SHIELD_STUN, Action.SHIELD_REFLECT]
        isNeutral = self.ai.action in [Action.STANDING, Action.DASHING, Action.TURNING, \
            Action.RUNNING, Action.EDGE_TEETERING_START, Action.EDGE_TEETERING]
        jumpcancel = (self.ai.action == Action.KNEE_BEND) and (self.ai.action_frame >= self.jump_cancel_frames())
        jumping = [Action.JUMPING_ARIAL_FORWARD, Action.JUMPING_ARIAL_BACKWARD]

        if isShielding or isNeutral:
            if self.controller.prev.button[Button.BUTTON_Y]:
                self.controller.empty_input()
                return
            self.controller.press_button(Button.BUTTON_Y)
            return

        if jumpcancel or self.ai.action in jumping:
            self.controller.press_button(Button.BUTTON_L)
            onLeft = self.ai.position.x < self.human.position.x
            x = -1
            if onLeft == towards:
                x = 1
            self.controller.tilt_analog(Button.BUTTON_MAIN, x, .35)
            return

        if self.ai.action == Action.LANDING_SPECIAL:
            self.controller.empty_input()
            return

        self.controller.empty_input()


    def waveshine(self, towards = True):
        """
        performs frameperfect waveshine, this can be either towards or away from the opponent, (False if away, True or no argument if towards)
    
        Arguments:
        (optional) Towards (boolean)
        """
        if self.ai == Action.SHIELD_STUN:
            self.controller.empty_input()
            return
        if self.ai.off_stage:
            self.controller.empty_input()
            return
        IsShineStart = self.ai.action in [Action.DOWN_B_STUN, Action.DOWN_B_GROUND, Action.DOWN_B_GROUND_START]
        if IsShineStart and self.ai.action_frame >= 3 and self.ai.on_ground:
            self.controller.press_button(Button.BUTTON_Y)
            return

        isShielding = self.ai.action in [Action.SHIELD_START, Action.SHIELD, \
           Action.SHIELD_RELEASE, Action.SHIELD_STUN, Action.SHIELD_REFLECT]
        isNeutral = self.ai.action in [Action.STANDING, Action.DASHING, Action.TURNING, \
            Action.RUNNING, Action.EDGE_TEETERING_START, Action.EDGE_TEETERING]
        jumpcancel = (self.ai.action == Action.KNEE_BEND) and (self.ai.action_frame >= self.isFoxOrFalco())
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

        if jumpcancel or self.ai.action in jumping:
            self.controller.press_button(Button.BUTTON_L)
            onLeft = self.ai.position.x < self.human.position.x
            x = -1
            if onLeft == towards:
                x = 1
            self.controller.tilt_analog(Button.BUTTON_MAIN, x, .35)
            return

        if self.ai.action == Action.LANDING_SPECIAL:
            self.controller.empty_input()
            return

        self.controller.empty_input()


    def hardReset(self):
        """
        this method is used to reset the state of the Bot, basically it releases all buttons
        """
        self.controller.release_all()

    def recover(self):
        """
        used to get back onto the stage

        This is currently designed for specifically fox (and not very well tbh)
        """
        jumping = [Action.JUMPING_ARIAL_FORWARD, Action.JUMPING_ARIAL_BACKWARD]
        #if we are on stage why would we recover
        if not self.ai.off_stage:
            self.controller.empty_input()
            return
        onLeft = self.ai.position.x > 0
        x = 1
        if onLeft:
            x = 0
        # we are free falling, we are just gonna move towards the stage
        if self.ai.action == Action.DEAD_FALL or self.ai.action == Action.SWORD_DANCE_1_AIR:
            self.controller.release_button(Button.BUTTON_B)
            self.controller.tilt_analog(Button.BUTTON_MAIN, x, .5)
            return
        #If we are on the ledge we are just gonna roll back on
        if self.ai.action in self.onEdge:
            if self.controller.prev.button[Button.BUTTON_L]:
                self.controller.empty_input()
                return
            self.controller.press_button(Button.BUTTON_L)
            return
        #If we cant jump, make sure that we dont try and mess something up
        if self.ai.jumps_left == 0 or self.ai.action in jumping:
            self.controller.release_button(Button.BUTTON_Y)
        #if we are in the middle of jumping, dont
        if self.ai.action in jumping and self.ai.action_frame < 10:
            self.controller.empty_input()
            return
        # are we off stage to the left or to the right? (the middle of every stage is zero and goes from - to + left to right respectively)
        distance_from_ledge = - abs(self.ai.position.x) - abs(melee.stages.EDGE_GROUND_POSITION[self.stage])
        canIllusion = (distance_from_ledge < 85) and (self.ai.position.y > -16.5)
        canJump = (distance_from_ledge < 30) and (self.ai.position.y > -30)
        needsToJump = (distance_from_ledge > 80) or (self.ai.position.y < -100)

        if canJump and self.ai.jumps_left > 0:
            if self.controller.prev.button[Button.BUTTON_Y]:
                self.controller.empty_input()
                return
            self.controller.press_button(Button.BUTTON_Y)
            self.controller.tilt_analog(Button.BUTTON_MAIN, x, .5)
            return
        if needsToJump and self.ai.jumps_left > 0:
            if self.controller.prev.button[Button.BUTTON_Y]:
                self.controller.empty_input()
                return
            self.controller.press_button(Button.BUTTON_Y)
            self.controller.tilt_analog(Button.BUTTON_MAIN, x, .5)
            return
        if canIllusion:
            self.controller.tilt_analog(Button.BUTTON_MAIN,x,0.5)
            self.controller.press_button(Button.BUTTON_B)
            return
        
        #We are about to take off
        if self.ai.action == Action.SWORD_DANCE_3_LOW:
            #We are above the stage
            if self.ai.position.y > 0:
                self.controller.tilt_analog(Button.BUTTON_MAIN, x, .5)
                return
            #We are under the stage
            if abs(self.ai.position.x) < melee.stages.EDGE_GROUND_POSITION[self.stage] + 30:
                self.controller.tilt_analog(Button.BUTTON_MAIN, .5, 1)
                return
            if self.ai.position.y < 0:
                self.controller.tilt_analog(Button.BUTTON_MAIN, x, 1)
                return

        #If we are within firefox range, firefox
        canFireFox = distance_from_ledge < 160
        if canFireFox:
            self.controller.press_button(Button.BUTTON_B)
            self.controller.tilt_analog(Button.BUTTON_MAIN, 0.5, 1)
            return

        self.controller.empty_input()

    def grab(self):
        if self.controller.prev.button[Button.BUTTON_Z]:
            self.controller.empty_input()
            return
        if self.ai.action == Action.GRAB:
            self.controller.empty_input()
            return
        if self.ai.action == Action.LANDING_SPECIAL:
            self.controller.empty_input()
            return
        if self.ai.action in [Action.DOWN_B_GROUND_START, Action.DOWN_B_GROUND] and self.ai.action_frame >=1:
            self.controller.press_button(Button.BUTTON_Y)
            self.controller.press_button(Button.BUTTON_Z)
            return
        if self.ai.action == Action.KNEE_BEND:
            if self.controller.prev.button[Button.BUTTON_Z]:
                self.controller.release_button(Button.BUTTON_Z)
                return
            self.controller.press_button(Button.BUTTON_Z)
            return
        #We successfully grabbed
        if self.ai.action in [Action.GRAB_WAIT, Action.GRAB_PULLING]:
            self.controller.release_button(Button.BUTTON_Z)
            self.controller.tilt_analog(Button.BUTTON_MAIN, .5, 0)
            return
        if self.controller.prev.button[Button.BUTTON_Z]:
            self.controller.release_button(Button.BUTTON_Z)
            return
        if not self.ai.action in [Action.LYING_GROUND_UP, Action.TECH_MISS_UP, Action.TECH_MISS_DOWN]:
            self.controller.press_button(Button.BUTTON_Z)
        