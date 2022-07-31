import melee
import tech

class Tactic:
    def __init__(self, framedata, human, ai, stage):
        self.framedata = framedata
        self.human = human
        self.stage = stage

def beingAttacked(self):
    """
    returns true if the opponent throws an attack that will hit us

    Arguments 
    framedata object (melee.FrameData),
    opponent state (gamestate.players[human_port]),
    ai state (gamestate.players[ai_port])
    stage (melee.enums.Stage)
    """
    if self.framedata.is_attack(self.human.character, self.human.action):
        hitframe = framedata.in_range(self.human, self.ai, self.stage)
        if(hitframe != 0):
            return True
    return False

def framesUntilHit(self):
    """
    returns the number of frames until the opponent will hit our ai

    Arguments :  
    framedata object (melee.FrameData instance),
    opponent state (gamestate.players[human_port],
    ai state (gamestate.players[ai_port])
    """
    hitframe = framedata.in_range(self.human, self.ai, self.stage)
    if(hitframe == 0):
        #if hitframe is zero, then that means they wont hit
        return hitframe
    framesuntilhit = hitframe - self.human.action_frame
    return framesuntilhit