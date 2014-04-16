
from gui_tool import GuiTool

class RotateTool(GuiTool):

    def __init__(self, name):
        super(RotateTool, self).__init__(name)

    def OnMouseMotion(self, x, y, lastx, lasty, event):

        if event.Dragging() and event.LeftIsDown():
            self.controller.viewport.theta += 0.1 * (y - lasty)
            self.controller.viewport.phi += - 0.1 * (x - lastx)
            self.controller.updateView()
            return True
        return False

