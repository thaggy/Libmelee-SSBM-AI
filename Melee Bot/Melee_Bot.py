import melee
import tech
import manager
import tactic

ai_port = 1
human_port = 2
path = "/Users/Tom/Desktop/Slippi"
meleeManager = manager.Manager(melee.Console(
                is_dolphin=True,
                path=path,
                slippi_address="127.0.0.1",
                logger=None), ai_port, human_port)

framedata = meleeManager.framedata

while True:
    gamestate = meleeManager.console.step()
    #Here are we in game
    if gamestate.menu_state in [melee.Menu.IN_GAME, melee.Menu.SUDDEN_DEATH]:
        meleeManager.initAI(gamestate.players[ai_port], gamestate.players[human_port], meleeManager.ai_controller, gamestate.stage)
        print(gamestate.players[human_port].invulnerable)
        print(framedata.is_roll(gamestate.players[human_port].character, gamestate.players[human_port].action))
        if meleeManager.tactic.isDead() or gamestate.players[human_port].action == melee.Action.TAUNT_RIGHT:
            meleeManager.tech.hardReset()
        
        if meleeManager.tactic.shouldNotShieldWhenShielding():
            meleeManager.tech.releaseLandZ()
        if meleeManager.tactic.shouldTechChase():
            meleeManager.tech.techChase()
        if meleeManager.tactic.canGrab():
            meleeManager.tech.grab()

        if meleeManager.tactic.shouldRecover():
            meleeManager.tech.recover()

        #print("HUMAN -> x - " + str(gamestate.players[human_port].position.x)+ ": y - "+ str(gamestate.players[human_port].position.y) + ": state - " + str(gamestate.players[human_port].action))
        #print("AI -> x - " + str(gamestate.players[ai_port].position.x)+ ": y - "+ str(gamestate.players[ai_port].position.y) + ": state - " + str(gamestate.players[ai_port].action))
    else:
       #Here we are in the main menu or menu select
       melee.MenuHelper.menu_helper_simple(gamestate,meleeManager.ai_controller,melee.enums.Character.FOX,melee.enums.Stage.FINAL_DESTINATION,"",0,0,False,False)