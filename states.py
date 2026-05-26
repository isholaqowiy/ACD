from aiogram.fsm.state import State, StatesGroup

class ScanStates(StatesGroup):
    waiting_for_content = State()
    waiting_for_file = State()

class AdminStates(StatesGroup):
    waiting_for_broadcast = State()
