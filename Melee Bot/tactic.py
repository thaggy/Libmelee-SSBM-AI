import melee
from melee.enums import Action
import tech

class Tactic:
    """
    Checks to see what the AI / Human Player is doing,
    """
    def __init__(self, framedata, human, ai, stage):
        self.framedata = framedata
        self.ai = ai
        self.human = human
        self.stage = stage

    def beingAttacked(self):
        """
        returns true if the opponent throws an attack that will hit us
        """
        if self.framedata.is_attack(self.human.character, self.human.action):
            hitframe = self.framedata.in_range(self.human, self.ai, self.stage)
            if(hitframe != 0):
                return True
        return False

    def framesUntilHit(self):
        """
        returns the number of frames until the opponent will hit our ai
        """
        hitframe = self.framedata.in_range(self.human, self.ai, self.stage)
        if(hitframe == 0):
            #if hitframe is zero, then that means they wont hit
            return hitframe
        framesuntilhit = hitframe - self.human.action_frame
        return framesuntilhit

    def isInHitStun(self):
        """
        returns true if the ai is currently in hit stun
        """
        if self.ai.hitlag_left == 1:
            return True
        return False

    def isHumanInHitStun(self):
        """
        returns true if the human player is currenty in hit stun
        """
        if self.human.hitstun_frames_left > 0:
            return True
        return False

    def howManyFramesOfHitStun(self):
        """
        if we are being hit, will return the number of hitframes until we are about to be hit
        """
        return self.human.hitstun_frames_left

    def isDead(self):
        """
        returns true if the ai is dead or in the process of respawning
        """
        if self.ai.action in [Action.ON_HALO_DESCENT, Action.DEAD_DOWN]:
            return True
        return False

    def isHumanDead(self):
        """
        returns true if the human is dead or currently respawning
        """
        if self.human.action in [Action.ON_HALO_DESCENT, Action.DEAD_DOWN]:
            return True
        return False

    def isOnStage(self):
        """
        returns true if the ai is off stage
        """
        return not self.ai.off_stage

    def isHumanOnStage(self):
        """
        returns true if the human on the stage
        """
        return not self.human.off_stage

    def canGrab(self):
        """
        Checks to see if we are facing the same direction and the ai is close to the 
        """
        distance_away_x = abs(self.ai.position.x - self.human.position.x)
        distance_away_y = abs(self.ai.position.y - self.human.position.y)
        onLeft = self.ai.position.x < self.human.position.x
        grab_distance = 15
        if abs(self.ai.speed_ground_x_self) > 2:
            grab_distance = 30
        facingRightDirection = onLeft == self.ai.facing
        if (not self.isInHitStun()) and (distance_away_x < grab_distance) and (self.isOnStage) and (facingRightDirection) and (distance_away_y < 1.5) and (self.shouldBeOffensive()) and (not self.invulnerableFromRespawn()):
            return True
        return False
    def canGoForKill(self):
        isAtPercent = self.human.percent >= 110
        killstates = [Action.LYING_GROUND_UP, Action.LYING_GROUND_DOWN, Action.TECH_MISS_UP, Action.TECH_MISS_DOWN, \
                            Action.GROUND_ROLL_FORWARD_UP, Action.GROUND_ROLL_BACKWARD_UP, \
                            Action.GROUND_ROLL_BACKWARD_DOWN, Action.GROUND_ROLL_FORWARD_DOWN, Action.GROUND_ROLL_SPOT_DOWN]
        grabbableTech = [Action.GROUND_ROLL_FORWARD_UP, Action.GROUND_ROLL_BACKWARD_UP, \
                                     Action.GROUND_ROLL_BACKWARD_DOWN, Action.GROUND_ROLL_FORWARD_DOWN, Action.GROUND_ROLL_SPOT_DOWN, \
                                     Action.NEUTRAL_TECH, Action.BACKWARD_TECH, Action.FORWARD_TECH, Action.GROUND_GETUP]
        return (self.human.action in killstates or (self.human.action in grabbableTech and (self.human.action_frame >= 16))) and isAtPercent


    def shouldRecover(self):
        """
        returns true if we are not in hitstun and we are off stage
        """
        return (not self.isInHitStun()) and (not self.isOnStage())
    def shouldBeOffensive(self):
        """
        returns true if we are not being attacked by anything that will hit us, and both us and the AI are on stage
        """
        return (not self.shouldDefend()) and (not self.shouldRecover()) and (self.isHumanOnStage()) and (not self.isHumanDead()) 
    def shouldDefend(self):
        """
        returns true if we should be trying to defend (we are about to be attacked and are not currently in hitstun and can act on it)
        """
        return (self.beingAttacked()) and (not self.isInHitStun())

    def shouldNotShieldWhenShielding(self):
        """
        returns true if Shield is on and we shouldnt be defending
        """
        return (self.ai.action == Action.SHIELD) and (not self.shouldDefend())

    def invulnerableFromRespawn(self):
        return (not self.framedata.is_roll(self.human.character, self.human.action)) and self.human.invulnerable

    def shouldTechChase(self):
        techChaseStates = [Action.BACKWARD_TECH, Action.NEUTRAL_TECH, Action.FORWARD_TECH, Action.LYING_GROUND_UP, \
                                     Action.LYING_GROUND_DOWN, Action.TECH_MISS_UP, Action.TECH_MISS_DOWN, Action.GROUND_ROLL_FORWARD_UP, Action.GROUND_ROLL_BACKWARD_UP, \
                                     Action.GROUND_ROLL_BACKWARD_DOWN, Action.GROUND_ROLL_FORWARD_DOWN, Action.GROUND_ROLL_SPOT_DOWN]
        return self.human.action in techChaseStates

    def isOnGround(self):
        states = [Action.LYING_GROUND_UP, Action.LYING_GROUND_DOWN, Action.TECH_MISS_UP, Action.TECH_MISS_DOWN]
        return self.ai.action in states