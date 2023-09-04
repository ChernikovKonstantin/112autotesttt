import allure
from assertpy import assert_that, soft_assertions
from selene import be
from selene.support.shared import browser
from selene.support.shared.jquery_style import s
from selenium.webdriver import ActionChains

from data.color_data import Color
from data.polygon_coordinates import PolygonCoordinates
from pages.classifiers_manager.custom_elements.modal_windows.delete_error_dialog import DeleteErrorDialog
from pages.common_page import BaseAppPage
from utils.service_utils import get_background_color, get_text_color


class PolygonReactionPage(BaseAppPage):

    def __init__(self):
        super().__init__()
        self._add_polygon_btn = s('//button[contains (., "Добавить полигон реагирования")]')
        self._polygon_name_draft_input = s('//input[contains (@ng-model, "polygonNameDraft")]')
        self._polygon_draft_buttons = lambda btn_title: self._polygon_name_draft_input.s(
            f'./ancestor::td/following-sibling::td/button[@title="{btn_title}" ]')
        self._map = s('//ymaps')
        self._map_dot_option_text = lambda option_text: self._map.s(f'//*[.="{option_text}"]')
        self._finish_creating_polygon_map_btn = s('//button[contains (., "Завершить создание полигона")]')
        self._polygon_button_with_title = lambda polygon_name, title: s(
            f'//td[contains (., "{polygon_name}")]/following-sibling::*/*[@title="{title}"]')

        self.wait_for_loading()

    @allure.step('Удалить точку на карте')
    def delete_dot_on_map(self):
        action = ActionChains(browser.driver)
        dot_coord = PolygonCoordinates.get_offset_dot_coordinates_for_edit_triangle_polygon((self._map().location['x'],
                                                                                             self._map().location['y']))
        action.move_to_element_with_offset(self._map(), xoffset=dot_coord[0], yoffset=dot_coord[1]).click()
        action.perform()
        self._map_dot_option_text('Удалить точку').click()
        return self

    @allure.step('Добавить полигон')
    def add_polygon(self, name: str, polygon_with_building: bool = False):
        self._add_polygon_btn.should(be.clickable, timeout=6).click()
        self.set_polygon_name(name)
        self._polygon_draft_buttons(btn_title='Добавить полигон').click()
        if polygon_with_building:
            coordinates = PolygonCoordinates.get_offset_coordinates_for_triangle_polygon_with_building(
                (self._map().location['x'],
                 self._map().location['y']))
        else:
            coordinates = PolygonCoordinates.get_offset_coordinates_for_triangle_polygon((self._map().location['x'],
                                                                                          self._map().location['y']))
        action = ActionChains(browser.driver)
        for dot in coordinates:
            action.move_to_element_with_offset(self._map(), xoffset=dot[0], yoffset=dot[1]).click()
        action.perform()
        self._finish_creating_polygon_map_btn.should(be.clickable, timeout=5).click()
        self.click_edit_mode_polygon_button_with_text(text='Сохранить')
        return self

    @allure.step('Клик по кнопке редактировать полигон')
    def click_edit_button_polygon_with_name(self, name: str):
        self._polygon_button_with_title(polygon_name=name, title='Редактировать').click()
        return self

    @allure.step('Клик по кнопке в режиме редактирования полигона')
    def click_edit_mode_polygon_button_with_text(self, text):
        self._polygon_draft_buttons(btn_title=text).click()
        self._polygon_draft_buttons(btn_title=text).with_(timeout=5).should(be.not_.enabled)
        return self

    @allure.step('Добавить точку полигона')
    def add_polygon_dot(self):
        action = ActionChains(browser.driver)
        old_dot_coordinates = PolygonCoordinates.get_offset_dot_coordinates_for_continue_edit_triangle_polygon(
            (self._map().location['x'], self._map().location['y']))
        action.move_to_element_with_offset(self._map(), xoffset=old_dot_coordinates[0],
                                           yoffset=old_dot_coordinates[1]).click()
        action.perform()
        self._map_dot_option_text('Продолжить').click()
        new_dot_coordinates = PolygonCoordinates.get_offset_new_dot_coordinates_for_edit_triangle_polygon(
            (self._map().location['x'], self._map().location['y']))
        action.move_to_element_with_offset(self._map(),
                                           xoffset=new_dot_coordinates[0],
                                           yoffset=new_dot_coordinates[1]
                                           ).click()
        action.perform()
        self._finish_creating_polygon_map_btn.should(be.clickable, timeout=5).click()
        return self

    @allure.step('Ввести название полигона')
    def set_polygon_name(self, name: str):
        self._polygon_name_draft_input.set_value(name)
        return self

    @allure.step("Проверка кнопок")
    def assure_buttons(self, polygon_name):
        with soft_assertions():
            with allure.step('Проверка цвета кнопок'):
                assert_that(get_background_color(
                    self._polygon_button_with_title(polygon_name=polygon_name, title='Редактировать'))).is_equal_to(
                    Color.WHITE)
                assert_that(get_background_color(
                    self._polygon_button_with_title(polygon_name=polygon_name, title='Показать полигон'))).is_equal_to(
                    Color.WHITE)
        return self

    @allure.step("Проверка цвета кнопки Обновить полигон")
    def assure_color_update_polygon_button(self):
        s('//body').click()  # костыль для снятия фокуса с кнопки
        assert_that(get_text_color(self._polygon_draft_buttons(btn_title='Обновить полигон'))).is_equal_to(Color.BLUE)

    @allure.step('Клик по кнопке Удалить для привязанного к службюе полигона')
    def click_delete_binding_polygon_button_with_text(self):
        self._polygon_draft_buttons(btn_title='Удалить полигон').click()
        return DeleteErrorDialog(xpath='//h2[.="Ошибка получения данных"]/ancestor::md-dialog')
