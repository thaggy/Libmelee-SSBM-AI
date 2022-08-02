import melee
from melee.enums import Action
import tech

class Tactic:
    """
    Checks to see what Human Player is doing,
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
            hitframe = framedata.in_range(self.human, self.ai, self.stage)
            if(hitframe != 0):
                return True
        return False

    def framesUntilHit(self):
        """
        returns the number of frames until the opponent will hit our ai
        """
        hitframe = framedata.in_range(self.human, self.ai, self.stage)
        if(hitframe == 0):
            #if hitframe is zero, then that means they wont hit
            return hitframe
        framesuntilhit = hitframe - self.human.action_frame
        return framesuntilhit

    def isInHitStun(self):
        if self.ai.hitstun_frames_left > 0:
            return True
        return False

    def isHumanInHitStun(self):
        if self.human.hitstun_frames_left > 0:
            return True
        return False

    def howManyFramesOfHitStun(self):
        return self.human.hitstun_frames_left

    def isDead(self):
        if self.ai.action in [Action.ON_HALO_DESCENT, Action.DEAD_DOWN]:
            return True
        return False

    def isHumanDead(self):
        if self.human.action in [Action.ON_HALO_DESCENT, Action.DEAD_DOWN]:
            return True
        return False

    def isOnStage(self):
        print(self.ai.off_stage)
        return not self.ai.off_stage

    def isHumanOnStage(self):
        if not self.Human.off_stage:
            return True
        return False

    def canGrab(self):
        distance_away_x = abs(self.ai.position.x - self.human.position.x)
        distance_away_y = abs(self.ai.position.y - self.human.position.y)
        onLeft = self.ai.position.x < self.human.position.x
        facingRightDirection = onLeft == self.ai.facing
        if not self.isInHitStun() and distance_away_x < 15 and self.isOnStage and facingRightDirection and distance_away_y < 1.5:
            return True
        return False
    def shouldRecover(self):
        return (not self.isInHitStun()) and (not self.isOnStage())