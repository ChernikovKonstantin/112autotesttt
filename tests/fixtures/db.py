__all__ = [
    'delete_test_polygons_after_test',
    'add_test_gos_service',
]

import pytest

from data.gos_services import GosServices
from database import mchs_112_db_connect


@pytest.fixture
def delete_test_polygons_after_test():
    polygons = []

    def _method(*polygon_names):
        for polygon in polygon_names:
            polygons.append(polygon)

    yield _method
    for polygon in polygons:
        mchs_112_db_connect.delete_polygon_history_by_old_name(polygon_name=polygon)
        mchs_112_db_connect.delete_gos_service_to_polygon_binding(polygon_name=polygon)
        mchs_112_db_connect.delete_polygon_by_name(polygon_name=polygon)


@pytest.fixture
def add_test_gos_service():
    mchs_112_db_connect.add_gos_service(GosServices.AUTO_TEST_SERVICE)
    yield
    mchs_112_db_connect.delete_cl_service_apply_condition_by_gos_service(GosServices.AUTO_TEST_SERVICE)
    mchs_112_db_connect.delete_cl_service_event_by_gos_service(GosServices.AUTO_TEST_SERVICE)
    mchs_112_db_connect.delete_departure_district_by_gos_service(GosServices.AUTO_TEST_SERVICE)
    mchs_112_db_connect.delete_incident_by_gos_service(GosServices.AUTO_TEST_SERVICE)
    mchs_112_db_connect.delete_gos_service_by_gos_service(GosServices.AUTO_TEST_SERVICE)
