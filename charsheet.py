"""The class which manages displaying the Character sheet."""

class CharSheet:

    def __init__(self, window, character):
        self.window = window
        self.character = character

    def update_sheet(self):
        self.window.clear()
        self.window.addstr(1,1, self.character.name)
        line = 2
        for skillname, skill in self.character.fighter_comp.skills.items():
            if skill:
                self.window.addstr(line,1,str(skill))

        self.window.refresh()
