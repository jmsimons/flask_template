from webapp import login_manager, mail, db_manager

def compile_expense_miles():
    pass

def prep_expense_summary(user_id, year):
    expense_miles = db_manager.get_user_expense_miles(user_id)
    cash_expenses = 0
    user_vehicles = db_manager.get_user_vehicles(user_id = user_id)
    for vehicle in user_vehicles:
        vehicle_expenses = db_manager.get_vehicle_expenses(vehicle["id"])
        if vehicle_expenses:
            cash_expenses += sum([i["amount"] for i in vehicle_expenses])
    return {"total_cash": cash_expenses, "total_miles": expense_miles}