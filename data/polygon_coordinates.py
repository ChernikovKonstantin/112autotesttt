import allure


class PolygonCoordinates:
    POLYGON_DISTRICT_COORD = ['MULTIPOLYGON', '37.6205', '55.75721', '37.6202', '55.7570', '37.6198']
    HISTORY_OLD_COORD = ['MULTIPOLYGON', '37.6205', '55.75721', '37.6202', '55.75703', '55.75739']
    HISTORY_NEW_COORD = ['MULTIPOLYGON', '37.6205', '55.75721', '37.6202', '55.75703', '37.6198']

    @staticmethod
    @allure.step('Получить три координаты точек для полигона')
    def get_offset_coordinates_for_triangle_polygon(map_coord):
        first_dot = map_coord
        second_dot = (first_dot[0] + 60, first_dot[1] - 60)
        third_dot = (second_dot[0] - 60, second_dot[1] - 60)
        return first_dot, second_dot, third_dot

    @staticmethod
    @allure.step('Получить три координаты точек для полигона со зданием')
    def get_offset_coordinates_for_triangle_polygon_with_building(map_coord):
        first_dot = (map_coord[0] + 206, map_coord[1] - 100)
        second_dot = (map_coord[0] + 60, map_coord[1] - 60)
        third_dot = (second_dot[0] - 60, second_dot[1] - 60)
        return first_dot, second_dot, third_dot

    @staticmethod
    @allure.step('Получить координату точки полигона для редактирования полигона')
    def get_offset_dot_coordinates_for_edit_triangle_polygon(map_coord):
        x = map_coord[0] - (map_coord[0] // 100 * 53)
        y = map_coord[1] - (map_coord[1] // 100 * 111)
        return x, y

    @staticmethod
    @allure.step('Получить координату точки полигона для продолжения редактирования')
    def get_offset_dot_coordinates_for_continue_edit_triangle_polygon(map_coord):
        x = map_coord[0] - (map_coord[0] // 100 * 53)
        y = map_coord[1] + (map_coord[1] // 100 * 126)
        return x, y

    @staticmethod
    @allure.step('Получить координату новой точки полигона для редактирования')
    def get_offset_new_dot_coordinates_for_edit_triangle_polygon(map_coord):
        x = map_coord[0] - (map_coord[0] // 100 * 95)
        y = map_coord[1] + (map_coord[1] // 100 * 104)
        return x, y
