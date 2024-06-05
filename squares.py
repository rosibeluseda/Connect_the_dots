class Square:
    def __init__(self, left=0, bottom=0, right=0, top=0, bg=0):
        self.left = left
        self.bottom = bottom
        self.right = right
        self.top = top
        self.bg = bg

    def update_side(self, side, new_value):
        if hasattr(self, side):
            setattr(self, side, new_value)

    def update_bg(self, new_value):
        self.bg = new_value

    def grey_sides(self):
        return [side for side in ['left', 'bottom', 'right', 'top'] if getattr(self, side) == 0]

    def is_complete(self):
        return all(getattr(self, side) != 0 for side in ['left', 'bottom', 'right', 'top'])
