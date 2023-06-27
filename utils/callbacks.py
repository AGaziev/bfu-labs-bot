from aiogram.utils.callback_data import CallbackData

group_callback = CallbackData("group", "group_id", "role")
show_callback = CallbackData("show", "data_type", "user_role")
add_lab_callback = CallbackData("add_lab", "group_id", "user_role")
check_lab_callback = CallbackData("lab_id", "status")
