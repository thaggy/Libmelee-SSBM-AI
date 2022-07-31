import melee
import tech

class Tactic:
    """
    Checks to see what Human Player is doing,
    """
    def __init__(self, framedata, human, ai, stage):
        self.framedata = framedata
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