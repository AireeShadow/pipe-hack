import sys
import yaml
from PyQt5.QtWidgets import QApplication, QWidget, QAbstractButton

def load_layout():
    with open('conf/layout.yaml') as layout:
        layout_list = yaml.safe_load(layout)
        return layout_list

class PipeWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.button_start_layout_list = load_layout()
        self.button_layout_list = self.button_start_layout_list
        
    def image_picker(self, button_type: str, directions: list) -> str:
        if button_type == 'half':
            if 'north' in directions:
                pic = 'pic/half_north.png'
            elif 'south' in directions:
                pic = 'pic/half_south.png'
            elif 'west' in directions:
                pic = 'pic/half_west.png'
            elif 'east' in directions:
                pic = 'pic/half_east.png'
        elif button_type == 'corner':
            if ('north' and 'east') in directions:
                pic = 'pic/corner_north_east.png'
            elif ('north' and 'west') in directions:
                pic = 'pic/corner_north_east.png'
            elif ('south' and 'west') in directions:
                pic = 'pic/corner_south_east.png'
            elif ('south' and 'east') in directions:
                pic = 'pic/corner_south_east.png'
        elif button_type == 'straight':
            if ('north' and 'south') in directions:
                pic = 'pic/straight_north_south.png'
            elif ('east' and 'west') in directions:
                pic = 'pic/straight_west_east.png' 
        elif button_type == 'three':
            if ('north' and 'south' and 'east') in directions:
                pic = 'pic/three_north_south_east.png'
            elif ('north' and 'south' and 'west') in directions:
                pic = 'pic/three_north_south_west.png'
            elif ('north' and 'east' and 'west') in directions:
                pic = 'pic/three_north_west_east.png'    
            elif ('south' and 'east' and 'west') in directions:
                pic = 'pic/three_south_west_east.png' 
        elif button_type == 'intersection':
            pic = 'pic/intersection.png'
        elif button_type == 'empty':
            pic = 'pic/empty.png'
        return pic
    
    def is_solved(self) -> bool:
        for row_list in self.button_layout_list:
            for col in row_list:
                for direction_dict in col['locations']:
                    if not direction_dict['connected']:
                        return False
        else:
            return True
    def get_neighbours_list(self, row: int, col: int) -> list:
        length = len(self.button_layout_list) - 1
        up_row = row - 1
        down_row = row + 1
        left_col = col - 1
        right_col = col + 1
        final_list = []
        if up_row >= 0:
            final_list.append((up_row, col))
        if down_row <= length:
            final_list.append((down_row, col))
        if left_col >= 0:
            final_list.append((row, left_col))
        if right_col <= length:
            final_list.append((row, right_col))
        return final_list
    
    def rotate_button(self, row: int, col: int) -> None:
        button_dict = self.button_layout_list[row][col]
        
    def initUI(self):
        grid = QGridLayout()
        self.setLayout(grid)
        