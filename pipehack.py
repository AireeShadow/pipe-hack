import PySimpleGUI as sg
import yaml

def load_layout() -> list:
    with open('conf/layout.yaml') as layout:
        layout_list = yaml.safe_load(layout)
        return layout_list


class PipeWindow():
    def __init__(self):
        self.button_start_layout_list = load_layout()
        self.button_layout_list = self.button_start_layout_list
        self.win_message = '''
        Предварительная договоренность, достигнутая в результате переговоров между дипломатическим представителем 
        Королевства Латверия Кристиной Лис и м-ром Оливером Гилмором [засекречено].

        Если в результате переговоров между дипломатическим корпусом Королевства Латверия и 
        представителем повстанческой группировки «Солнцестояние» не будет достигнуто мирное решение,
        Королевство Латверия в лице официального ведомства по военным конфликтам обязуется заключить 
        м-ром Оливером Гилмором, гражданином Великобритании, либо указанной им организацией, договор 
        на поставку огнестрельного, химического, газового и/или иного согласованного сторонами оружия 
        для ведения боевых действий.
        '''
        

    def generate_sg_layout(self) -> list:
        layout_list = []
        for row in range(len(self.button_layout_list)):
            col_list = []
            for col in range(len(self.button_layout_list[0])):
                generic_button = sg.Button(
                button_text=f'{row}:{col}',
                button_color=sg.TRANSPARENT_BUTTON,
                image_filename=self.button_layout_list[row][col]['image'],
                image_size=(64, 64),
                size=(64, 64), 
                border_width=0,
                font=("Helvetica", 1)
                )
                col_list.insert(col, generic_button)
            layout_list.insert(row, col_list)
        return layout_list

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
            if all(x in directions for x in ['north', 'east']):
                pic = 'pic/corner_north_east.png'
            elif all(x in directions for x in ['north', 'west']):
                pic = 'pic/corner_north_west.png'
            elif all(x in directions for x in ['south', 'east']):
                pic = 'pic/corner_south_east.png'
            elif all(x in directions for x in ['south', 'west']):
                pic = 'pic/corner_south_west.png'
        elif button_type == 'straight':
            if all(x in directions for x in ['south', 'north']):
                pic = 'pic/straight_north_south.png'
            elif all(x in directions for x in ['east', 'west']):
                pic = 'pic/straight_west_east.png' 
        elif button_type == 'three':
            if all(x in directions for x in ['south', 'east', 'north']):
                pic = 'pic/three_north_south_east.png'
            elif all(x in directions for x in ['south', 'west', 'north']):
                pic = 'pic/three_north_south_west.png'
            elif all(x in directions for x in ['west', 'east', 'north']):
                pic = 'pic/three_north_west_east.png'    
            elif all(x in directions for x in ['south', 'east', 'west']):
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
    
    def set_connections(self) -> None:
        for row_index, row_list in enumerate(self.button_layout_list):
            for col_index, col_dict in enumerate(row_list):
                neighbours_list = self.get_neighbours_list(row=row_index, col=col_index)
                current_button_directions_list = []
                for direction_dict in col_dict['locations']:
                    direction = direction_dict['direction']
                    current_button_directions_list.append(direction)
                for neighbour_coords_tuple in neighbours_list:
                    neighbour_button_directions_list = []
                    neighbour_row = neighbour_coords_tuple[0]
                    neighbour_col = neighbour_coords_tuple[1]
                    for neighbour_directions_dict in self.button_layout_list[neighbour_row][neighbour_col]['locations']:
                        neighbour_button_directions_list.append(neighbour_directions_dict['direction'])
                    if self.button_layout_list[neighbour_row][neighbour_col]['type'] != 'empty':
                        if neighbour_row < row_index:
                            #up
                            if 'north' in current_button_directions_list and 'south' in neighbour_button_directions_list:
                                for direction_index, direction_dict in enumerate(self.button_layout_list[row_index][col_index]['locations']):
                                    if direction_dict['direction'] == 'north':
                                        self.button_layout_list[row_index][col_index]['locations'][direction_index]['connected'] = True
                            else:
                                for direction_index, direction_dict in enumerate(self.button_layout_list[row_index][col_index]['locations']):
                                    if direction_dict['direction'] == 'north':
                                        self.button_layout_list[row_index][col_index]['locations'][direction_index]['connected'] = False
                        elif neighbour_row > row_index:
                            #down
                            if 'south' in current_button_directions_list and 'north' in neighbour_button_directions_list:
                                for direction_index, direction_dict in enumerate(self.button_layout_list[row_index][col_index]['locations']):
                                    if direction_dict['direction'] == 'south':
                                        self.button_layout_list[row_index][col_index]['locations'][direction_index]['connected'] = True
                            else:
                                for direction_index, direction_dict in enumerate(self.button_layout_list[row_index][col_index]['locations']):
                                    if direction_dict['direction'] == 'south':
                                        self.button_layout_list[row_index][col_index]['locations'][direction_index]['connected'] = False
                        elif neighbour_col < col_index:
                            #left
                            if 'west' in current_button_directions_list and 'east' in neighbour_button_directions_list:
                                for direction_index, direction_dict in enumerate(self.button_layout_list[row_index][col_index]['locations']):
                                    if direction_dict['direction'] == 'west':
                                        self.button_layout_list[row_index][col_index]['locations'][direction_index]['connected'] = True
                            else:
                                for direction_index, direction_dict in enumerate(self.button_layout_list[row_index][col_index]['locations']):
                                    if direction_dict['direction'] == 'west':
                                        self.button_layout_list[row_index][col_index]['locations'][direction_index]['connected'] = False
                        elif neighbour_col > col_index:
                            #right
                            if 'east' in current_button_directions_list and 'west' in neighbour_button_directions_list:
                                for direction_index, direction_dict in enumerate(self.button_layout_list[row_index][col_index]['locations']):
                                    if direction_dict['direction'] == 'east':
                                        self.button_layout_list[row_index][col_index]['locations'][direction_index]['connected'] = True
                            else:
                                for direction_index, direction_dict in enumerate(self.button_layout_list[row_index][col_index]['locations']):
                                    if direction_dict['direction'] == 'east':
                                        self.button_layout_list[row_index][col_index]['locations'][direction_index]['connected'] = False
    
    def rotate_button(self, row: int, col: int) -> None:
        button_dict = self.button_layout_list[row][col]
        if self.button_layout_list[row][col]['type'] == 'half':
            if self.button_layout_list[row][col]['locations'][0]['direction'] == 'north':
                self.button_layout_list[row][col]['locations'][0]['direction'] = 'east'
                pic = 'pic/half_east.png'
            elif self.button_layout_list[row][col]['locations'][0]['direction'] == 'east':
                self.button_layout_list[row][col]['locations'][0]['direction'] = 'south'
                pic = 'pic/half_south.png'
            elif self.button_layout_list[row][col]['locations'][0]['direction'] == 'south':
                self.button_layout_list[row][col]['locations'][0]['direction'] = 'west'
                pic = 'pic/half_west.png'
            elif self.button_layout_list[row][col]['locations'][0]['direction'] == 'west':
                self.button_layout_list[row][col]['locations'][0]['direction'] = 'north'
                pic = 'pic/half_north.png'
        elif self.button_layout_list[row][col]['type'] == 'corner':
            if self.button_layout_list[row][col]['locations'][0]['direction'] == 'north' and self.button_layout_list[row][col]['locations'][1]['direction'] == 'east':
                self.button_layout_list[row][col]['locations'][0]['direction'] = 'east'
                self.button_layout_list[row][col]['locations'][1]['direction'] = 'south'
                pic = 'pic/corner_south_east.png'
            elif self.button_layout_list[row][col]['locations'][0]['direction'] == 'east' and self.button_layout_list[row][col]['locations'][1]['direction'] == 'south':
                self.button_layout_list[row][col]['locations'][0]['direction'] = 'south'
                self.button_layout_list[row][col]['locations'][1]['direction'] = 'west'
                pic = 'pic/corner_south_west.png'
            elif self.button_layout_list[row][col]['locations'][0]['direction'] == 'south' and self.button_layout_list[row][col]['locations'][1]['direction'] == 'west':
                self.button_layout_list[row][col]['locations'][0]['direction'] = 'west'
                self.button_layout_list[row][col]['locations'][1]['direction'] = 'north'
                pic = 'pic/corner_north_west.png'
            elif self.button_layout_list[row][col]['locations'][0]['direction'] == 'west' and self.button_layout_list[row][col]['locations'][1]['direction'] == 'north':
                self.button_layout_list[row][col]['locations'][0]['direction'] = 'north'
                self.button_layout_list[row][col]['locations'][1]['direction'] = 'east'
                pic = 'pic/corner_north_east.png'
        elif self.button_layout_list[row][col]['type'] == 'straight':
            if self.button_layout_list[row][col]['locations'][0]['direction'] == 'north' and self.button_layout_list[row][col]['locations'][1]['direction'] == 'south':
                self.button_layout_list[row][col]['locations'][0]['direction'] = 'west'
                self.button_layout_list[row][col]['locations'][1]['direction'] = 'east'
                pic = 'pic/straight_west_east.png' 
            elif self.button_layout_list[row][col]['locations'][0]['direction'] == 'west' and self.button_layout_list[row][col]['locations'][1]['direction'] == 'east':
                self.button_layout_list[row][col]['locations'][0]['direction'] = 'north'
                self.button_layout_list[row][col]['locations'][1]['direction'] = 'south'
                pic ='pic/straight_north_south.png'
        elif self.button_layout_list[row][col]['type'] == 'three':
            if self.button_layout_list[row][col]['locations'][0]['direction'] == 'north' and self.button_layout_list[row][col]['locations'][1]['direction'] == 'east' and self.button_layout_list[row][col]['locations'][2]['direction'] == 'south':
                self.button_layout_list[row][col]['locations'][0]['direction'] = 'west'
                self.button_layout_list[row][col]['locations'][1]['direction'] = 'east'
                self.button_layout_list[row][col]['locations'][2]['direction'] = 'south'
                pic = 'pic/three_south_west_east.png' 
            elif self.button_layout_list[row][col]['locations'][0]['direction'] == 'west' and self.button_layout_list[row][col]['locations'][1]['direction'] == 'east' and self.button_layout_list[row][col]['locations'][2]['direction'] == 'south':
                self.button_layout_list[row][col]['locations'][0]['direction'] = 'west'
                self.button_layout_list[row][col]['locations'][1]['direction'] = 'north'
                self.button_layout_list[row][col]['locations'][2]['direction'] = 'south'
                pic = 'pic/three_north_south_west.png'
            elif self.button_layout_list[row][col]['locations'][0]['direction'] == 'west' and self.button_layout_list[row][col]['locations'][1]['direction'] == 'north' and self.button_layout_list[row][col]['locations'][2]['direction'] == 'south':
                self.button_layout_list[row][col]['locations'][0]['direction'] = 'west'
                self.button_layout_list[row][col]['locations'][1]['direction'] = 'east'
                self.button_layout_list[row][col]['locations'][2]['direction'] = 'north'
                pic = 'pic/three_north_west_east.png'
            elif self.button_layout_list[row][col]['locations'][0]['direction'] == 'west' and self.button_layout_list[row][col]['locations'][1]['direction'] == 'east' and self.button_layout_list[row][col]['locations'][2]['direction'] == 'north':
                self.button_layout_list[row][col]['locations'][0]['direction'] = 'north'
                self.button_layout_list[row][col]['locations'][1]['direction'] = 'east'
                self.button_layout_list[row][col]['locations'][2]['direction'] = 'south'
                pic = 'pic/three_north_south_east.png'
        elif self.button_layout_list[row][col]['type'] == 'intersection':
                pic = 'pic/intersection.png'
        elif self.button_layout_list[row][col]['type'] == 'empty':
                pic = 'pic/empty.png'
        self.button_layout_list[row][col]['image'] = pic
    
    def click_button(self, row: int, col: int):
        self.rotate_button(row=row, col=col)
        self.set_connections()
        solved_bool = self.is_solved()
        if solved_bool:
            sg.popup_ok(self.win_message, title='Важная информация')
    
    def main(self):
        pos_list = [f'{r}:{c}' for r in range(len(self.button_layout_list)) for c in range(len(self.button_layout_list[0]))]
        sg_layout = self.generate_sg_layout()
        window = sg.Window('Интерфейс взлома', sg_layout)
        while True:
            event, values = window.read()
            if event in (None, 'Exit'):
                break
            for pos in pos_list:
                if event == pos:
                    row = int(pos[0])
                    col = int(pos[2])
                    self.click_button(row=row, col=col)
                    print(f'button {row} {col} clicked')
                    #sg_layout = self.generate_sg_layout()
                    window[event].update(image_filename=self.button_layout_list[row][col]['image'])
        self.window.Close()

pw = PipeWindow()
pw.main()
