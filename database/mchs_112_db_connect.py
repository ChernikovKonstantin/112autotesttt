import conf.db
from data.gos_services import GosService
from database.db_connect import DBConnect

__all__ = ["mchs_112_db_connect"]


class _DbConnect(DBConnect):

    def __init__(self, config=conf.db.DB_CONFIG):
        super().__init__(config)

    def select_all_from_departure_districts_by_name(self, name):
        result = self.select(
            f'''SELECT * FROM departure_districts  WHERE "name" = '{name}';'''
        )
        return result

    def get_gos_service_by_polygon_name(self, polygon_name):
        result = self.select(
            f'''select gdd.gov_service_id,gs.short_title,gdd.departure_district_id,dd.name
            from gov_services_to_departure_districts gdd
            join departure_districts dd
            on dd.id=gdd.departure_district_id
            join gos_service gs
            on gs.id=gdd.gov_service_id
            where "name" = '{polygon_name}';'''
        )
        return result[0] if result else None

    def delete_polygon_by_name(self, polygon_name):
        self.delete(
            f'''DELETE FROM departure_districts  WHERE "name" = '{polygon_name}';'''
        )

    def delete_polygon_history_by_old_name(self, polygon_name):
        self.delete(
            f'''DELETE FROM polygon_change_history  WHERE "old_polygon_name" = '{polygon_name}';'''
        )

    def delete_gos_service_to_polygon_binding(self, polygon_name):
        polygon = self.get_gos_service_by_polygon_name(polygon_name=polygon_name)
        if polygon:
            self.delete(
                f'''DELETE FROM gov_services_to_departure_districts  WHERE "departure_district_id" = '{polygon[2]}';'''
            )

    def get_incidents_with_status(self, incident_status_id):
        result = self.select(
            f'''SELECT * FROM public.incident WHERE incident_status = {incident_status_id} 
            ORDER BY "id" DESC LIMIT 20;''')
        return result if result else None

    def get_last_incident_id_with_gos_service_id_and_incident_status_id(self, service_id, incident_status_id):
        incidents = self.get_incidents_with_status(incident_status_id=incident_status_id)
        incident_ids = tuple([incident[0] for incident in incidents])
        if incident_ids:
            result = self.select(
                f'''SELECT * FROM public.incident_gos_service WHERE gos_service = '{service_id}'
                 and incident in {incident_ids} ORDER BY "id" DESC LIMIT 1;'''
            )
            return result[0][2] if result else None

    def get_polygon_coords_by_name(self, polygon_name):
        result = self.select(
            f"""SELECT st_astext(polygon) FROM public.departure_districts WHERE name = '{polygon_name}'""")
        return result if result else None

    def get_value_from_polygon_history_by_old_name(self, value, polygon_name):
        result = self.select(
            f"""SELECT {value} FROM public.polygon_change_history WHERE old_polygon_name = '{polygon_name}'""")
        return result if result else None

    def get_value_from_staff_work_shift_group_by_employee_id(self, value, employee_id):
        result = self.select(
            f"""SELECT {value} FROM public.staff_work_shift_group WHERE employee_id = '{employee_id}' 
            and dt_delete is null""")
        return result[0][0] if result else None

    def add_gos_service(self, gos_service: GosService):
        self.insert(
            f"""INSERT INTO public.gos_service VALUES ({gos_service.id},
                                                        '{gos_service.title}',
                                                        '9876',
                                                        '{gos_service.title}',
                                                        true,
                                                        null,
                                                        null,
                                                        null,
                                                        1,
                                                        false,
                                                         null,
                                                        false,
                                                        null,
                                                        null,
                                                        null,
                                                        null)""")

    def delete_cl_service_apply_condition_by_gos_service(self, gos_service: GosService):
        self.delete(
            f'''DELETE FROM public.cl_service_apply_condition WHERE "gov_service" = '{gos_service.id}';'''
        )

    def delete_cl_service_event_by_gos_service(self, gos_service: GosService):
        self.delete(
            f'''DELETE FROM public.cl_service_event WHERE "gov_service" = '{gos_service.id}';'''
        )

    def delete_gos_service_by_gos_service(self, gos_service: GosService):
        self.delete(
            f'''DELETE FROM public.gos_service WHERE "id" = '{gos_service.id}';'''
        )

    def delete_departure_district_by_gos_service(self, gos_service: GosService):
        self.delete(
            f'''DELETE FROM public.gov_services_to_departure_districts WHERE "gov_service_id" = '{gos_service.id}';'''
        )

    def delete_incident_by_gos_service(self, gos_service: GosService):
        self.delete(
            f'''DELETE FROM public.incident_gos_service WHERE "gos_service" = '{gos_service.id}';'''
        )


# один инстанс на ноду
mchs_112_db_connect = _DbConnect()

if __name__ == '__main__':
    pass
