from action.Action import Action  # 確保正確導入 Action
from DB_utils import db_search_food_by_name_partial, db_get_nutrients_of_food

class SearchNutrientofFood(Action):
    def __init__(self):
        super().__init__("SearchNutrientofFood")  # 初始化 Action 名稱

    def exec(self, conn, operator_id):
        # Step 1: 提示使用者輸入食物名稱
        f_name_partial = self.read_input(conn, "the name of the food you want to search for")
        
        # Step 2: 查詢模糊比對結果
        matching_foods = db_search_food_by_name_partial(f_name_partial)
        
        if not matching_foods:
            conn.send(f"No food found matching '{f_name_partial}'.\n".encode('utf-8'))
            return
        
        # Step 3: 顯示所有匹配的食物
        table = "Food ID | Food Name\n"
        for food in matching_foods:
            table += f"{food[0]} | {food[1]}\n"
        self.send_table(conn, table)
        
        # Step 4: 要求使用者選擇其中一個食物的 F_id
        f_id = self.read_input(conn, "the Food ID you want to view nutrients for")
        
        # Step 5: 查詢所選食物的營養素
        nutrients = db_get_nutrients_of_food(f_id)
        
        if not nutrients:
            conn.send(f"No nutrients found for Food ID {f_id}.\n".encode('utf-8'))
            return
        
        # Step 6: 顯示營養素資料（包括單位）
        table = "Nutrient Name | Amount per 100g | Unit\n"
        for nutrient in nutrients:
            table += f"{nutrient[0]} | {nutrient[1]} | {nutrient[2]}\n"
        self.send_table(conn, table)
