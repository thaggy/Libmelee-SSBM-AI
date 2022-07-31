import melee
import tech as te
import tactic as ta

class Manager:
    framedata = melee.FrameData(write=False)
    tech = None
    tactic = None

    def __init__(self, console, ai_port, human_port):
        self.ai_port = ai_port
        self.human_port = human_port
        self.console = console
        self.ai_controller = melee.Controller(console=console, port=self.ai_port)
        self.human_controller = melee.Controller(console=console, port=self.human_port, type=melee.ControllerType.GCN_ADAPTER)
        self.console.run()
        self.console.connect()
        self.ai_controller.connect()
        self.human_controller.connect()

    def initAI(self, ai_state, human_state, controller, stage):
        self.tech = te.Tech(ai_state, human_state, controller)
        self.tactic = ta.Tactic(self.framedata, human_state, ai_state, stage)