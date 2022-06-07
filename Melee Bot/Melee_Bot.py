import melee
import tech

console = melee.Console(
                is_dolphin=True,
                path="/Users/Tom/Desktop/Slippi",
                slippi_address="127.0.0.1",
                logger=None)
ai_port = 1
human_port = 2
controller = melee.Controller(console=console, port=ai_port)
controller_human = melee.Controller(console=console,
                                    port=2,
                                    type=melee.ControllerType.GCN_ADAPTER)
console.run()
console.connect()
controller.connect()
controller_human.connect()
framedata = melee.FrameData(write=False)

while True:
    gamestate = console.step()
    if gamestate.menu_state in [melee.Menu.IN_GAME, melee.Menu.SUDDEN_DEATH]:
        #We are in game here
        #print(gamestate.players[ai_port].action) # Prints the animation that player 2 is in
        #Detects incoming attacks
        tech.fox_multishine(ai_state = gamestate.players[ai_port],controller = controller)
        '''
        if gamestate.players[ai_port].action == melee.enums.Action.MARTH_COUNTER or gamestate.players[ai_port].action == melee.enums.Action.MARTH_COUNTER_FALLING or gamestate.players[ai_port].action == melee.enums.Action.PARASOL_FALLING:
            print("detecting counter state, entering tech.marth_counter")
            tech.marth_counter(ai_state = gamestate.players[ai_port], controller = controller)
        if framedata.is_attack(22 , gamestate.players[human_port].action):
            hitframe = framedata.in_range(gamestate.players[human_port], gamestate.players[ai_port], melee.enums.Stage.POKEMON_STADIUM)
            framesuntilhit = hitframe - gamestate.players[human_port].action_frame
            print(framesuntilhit, " - ", hitframe, " - ", gamestate.players[human_port].action_frame)
            if framesuntilhit <=  6:
                print("Detecting hit, starting counter")
                tech.marth_counter(ai_state = gamestate.players[ai_port],controller = controller)
        '''
           
        #    print(hitframe)
    else:
       #Here we are in the main menu or menu select
       melee.menuhelper.MenuHelper.menu_helper_simple(gamestate,controller,melee.enums.Character.FOX,melee.enums.Stage.FINAL_DESTINATION,connect_code="",autostart=False,swag=False)
