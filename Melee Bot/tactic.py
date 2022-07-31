import melee
import tech

def beingAttacked(framedata, opponent, ai, stage):
    """
    returns true if the opponent throws an attack that will hit us

    Arguments 
    framedata object (melee.FrameData),
    opponent state (gamestate.players[human_port]),
    ai state (gamestate.players[ai_port])
    stage (melee.enums.Stage)
    """
    if framedata.is_attack(opponent.character, opponent.action):
        hitframe = framedata.in_range(opponent, ai, stage)
        if(hitframe != 0):
            return True
    return False

def framesUntilHit(framedata, opponent, ai, stage):
    """
    returns the number of frames until the opponent will hit our ai

    Arguments :  
    framedata object (melee.FrameData instance),
    opponent state (gamestate.players[human_port],
    ai state (gamestate.players[ai_port])
    """
    hitframe = framedata.in_range(opponent, ai, stage)
    if(hitframe == 0):
        #if hitframe is zero, then that means they wont hit
        return hitframe
    framesuntilhit = hitframe - opponent.action_frame
    return framesuntilhit