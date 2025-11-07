# save.py
import json
import os

SAVE_FILE = os.path.join(os.path.dirname(__file__), "savegame.json")

def save_game(player, shop):
    """Guarda automáticamente el estado del jugador y la tienda."""
    data = {
        "player": {
            "money": player.money,
            "total_clicks": player.total_clicks,
            "click_income": player.click_income,
            "auto_income": player.auto_income
        },
        "shop": [
            {
                "name": item.name,
                "cost": item.cost,
                "base_income": item.base_income,
                "tipo": item.tipo,
                "amount": item.amount
            }
            for item in shop.items
        ]
    }
    with open(SAVE_FILE, "w") as f:
        json.dump(data, f, indent=4)

def load_game(player, shop):
    """Carga automáticamente el estado del jugador y la tienda si existe."""
    if not os.path.exists(SAVE_FILE):
        return
    try:
        with open(SAVE_FILE, "r") as f:
            data = json.load(f)
        player_data = data.get("player", {})
        player.money = player_data.get("money", player.money)
        player.total_clicks = player_data.get("total_clicks", player.total_clicks)
        player.click_income = player_data.get("click_income", player.click_income)
        player.auto_income = player_data.get("auto_income", player.auto_income)

        shop_data = data.get("shop", [])
        for item, saved_item in zip(shop.items, shop_data):
            item.amount = saved_item.get("amount", item.amount)
            item.cost = saved_item.get("cost", item.cost)
    except Exception as e:
        print(f"No se pudo cargar la partida: {e}")
