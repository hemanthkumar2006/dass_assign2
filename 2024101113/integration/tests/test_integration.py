import pytest
from registration import RegistrationModule
from crew import CrewManagementModule
from inventory import InventoryModule
from race import RaceManagementModule
from results import ResultsModule
from mission import MissionPlanningModule
from weather import WeatherModule
from blackmarket import BlackMarketModule

def setup_system():
    reg = RegistrationModule()
    crew = CrewManagementModule(reg)
    inv = InventoryModule(cash=1000)
    race_mgr = RaceManagementModule(crew, inv)
    results = ResultsModule(inv)
    mission_planner = MissionPlanningModule(crew, inv)
    weather = WeatherModule()
    black_market = BlackMarketModule(inv)
    return reg, crew, inv, race_mgr, results, mission_planner, weather, black_market

def test_register_driver_and_enter_race():
    reg, crew, inv, race_mgr, results, mission_planner, weather, black_market = setup_system()
    
    reg.register("Dominic")
    crew.assign_role("Dominic", "driver", 100)
    inv.add_car("Charger", 100)
    
    race = race_mgr.create_race("Dominic", "Charger")
    
    assert race["driver"] == "Dominic"
    assert race["car"] == "Charger"
    assert race["status"] == "Ready"

def test_enter_race_without_registered_driver():
    reg, crew, inv, race_mgr, results, mission_planner, weather, black_market = setup_system()
    
    inv.add_car("Charger", 100)
    
    # "Brian" is not registered at all
    with pytest.raises(ValueError, match="Brian is not a valid driver for a race."):
        race_mgr.create_race("Brian", "Charger")

def test_complete_race_updates_inventory():
    reg, crew, inv, race_mgr, results, mission_planner, weather, black_market = setup_system()
    
    reg.register("Dominic")
    crew.assign_role("Dominic", "driver", 100)
    inv.add_car("Charger", 100)
    inv.update_cash(-1000) # Reset cash to 0 for assert clarity
    
    race = race_mgr.create_race("Dominic", "Charger")
    results.complete_race(race, position=1, prize_money=5000)
    
    assert inv.cash == 5000
    assert inv.get_car_condition("Charger") == 90 # 100 - 10 damage for 1st place
    assert race["status"] == "Completed"

def test_assign_mission_validates_crew_roles():
    reg, crew, inv, race_mgr, results, mission_planner, weather, black_market = setup_system()
    
    reg.register("Tej")
    crew.assign_role("Tej", "mechanic", 80)
    inv.add_car("RX7", 40) # Damaged car
    
    # Mission requires mechanic since car is < 50 condition
    result = mission_planner.assign_mission("FixCar", "mechanic", "RX7")
    assert "started with Tej and RX7" in result
    
    # Try driver
    reg.register("Mia")
    crew.assign_role("Mia", "driver", 70)
    with pytest.raises(ValueError, match="Car RX7 is damaged. Requires a mechanic."):
        mission_planner.assign_mission("DriveDamagedCar", "driver", "RX7")

def test_extra_modules_integration():
    reg, crew, inv, race_mgr, results, mission_planner, weather, black_market = setup_system()
    
    # Weather module sets condition
    weather.set_weather("Rainy")
    assert weather.current_weather == "Rainy"
    
    # Black Market buys a part
    initial_cash = inv.cash
    black_market.buy_part("Turbo", 500)
    
    assert inv.cash == initial_cash - 500
    assert inv.parts.get("Turbo") == 1
