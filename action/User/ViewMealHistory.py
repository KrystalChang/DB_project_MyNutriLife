from action.Action import Action
from DB_utils import db_get_meal_records_by_date_range, db_delete_meal_record

class ViewMealHistory(Action):
    def __init__(self):
        super().__init__("ViewMealHistory")

    def exec(self, conn, u_id):
        # Step 1: Ask for start and end dates
        start_date = self.read_input(conn, "the start date (YYYY-MM-DD)")
        end_date = self.read_input(conn, "the end date (YYYY-MM-DD)")

        # Step 2: Fetch meal records
        records = db_get_meal_records_by_date_range(u_id, start_date, end_date)
        
        if not records:
            conn.send("[INFO] No meal records found for the specified period.\n".encode('utf-8'))
            return
        
        # Display meal records
        table = "Food ID | Food Name | Eaten Grams | Date | Time\n"
        for record in records:
            f_id, f_name, eaten_grams, date, time = record
            table += f"{f_id} | {f_name} | {eaten_grams} | {date} | {time}\n"
        
        self.send_table(conn, table)

        # Step 3: Ask if the user wants to delete any records
        delete_choice = self.read_input(conn, "Would you like to delete any records? (yes/no)").lower()
        
        if delete_choice == "yes":
            # Collect primary key parts
            f_id_to_delete = self.read_input(conn, "the Food ID of the record to delete")
            date_to_delete = self.read_input(conn, "the Date of the record to delete (YYYY-MM-DD)")
            time_to_delete = self.read_input(conn, "the Time of the record to delete (HH:MM:SS)")

            # Step 4: Delete the selected meal record
            try:
                db_delete_meal_record(u_id, f_id_to_delete, date_to_delete, time_to_delete)
                conn.send("[INFO] Meal record deleted successfully.\n".encode('utf-8'))
            except Exception as e:
                conn.send(f"[ERROR] Failed to delete the record: {str(e)}\n".encode('utf-8'))
        else:
            conn.send("[INFO] No records were deleted.\n".encode('utf-8'))
