"""
save.py — Gestión de guardado y carga de partidas de Click & Hide.

Incluye funciones para:
  - Guardar automáticamente el estado del jugador y la tienda.
  - Cargar partidas existentes al iniciar el juego.
El archivo de guardado será `savegame.json` en la carpeta raíz del proyecto.
"""

import json
import os

# Archivo de guardado en la carpeta donde se ejecuta el juego
SAVE_FILE = os.path.join(os.getcwd(), "savegame.json")


def save_game(player, shop):
    """
    Guarda automáticamente el estado actual del jugador y la tienda en disco.

    Args:
        player (Player): Instancia del jugador con dinero, clics e ingresos.
        shop (Shop): Instancia de la tienda con los ítems y sus cantidades.
    """
    data = {
        "player": {
            "money": player.money,
            "total_clicks": player.total_clicks,
            "click_income": player.click_income,
            "auto_income": player.auto_income,
            "total_money": player.money,  # 🔹 guarda el dinero actual también como total
        },
        "shop": [
            {
                "name": getattr(item, "name", ""),
                "cost": getattr(item, "cost", 0),
                "base_income": getattr(item, "base_income", 0),
                "tipo": getattr(item, "tipo", ""),
                "amount": getattr(item, "amount", 0),
            }
            for item in getattr(shop, "items", [])
        ],
    }

    try:
        with open(SAVE_FILE, "w") as f:
            json.dump(data, f, indent=4)
    except Exception as e:
        print(f"[ERROR] No se pudo guardar la partida: {e}")


def load_game(player, shop):
    """
    Carga la partida guardada si existe y actualiza el jugador y la tienda.

    Args:
        player (Player): Instancia del jugador que se actualizará con los datos guardados.
        shop (Shop): Instancia de la tienda cuyos ítems se actualizarán según la partida guardada.
    """
    if not os.path.exists(SAVE_FILE):
        print(f"[LOAD] No se encontró partida guardada en: {SAVE_FILE}")
        return

    try:
        with open(SAVE_FILE, "r") as f:
            data = json.load(f)

        player_data = data.get("player", {})

        # Restaurar datos básicos
        player.money = player_data.get("money", getattr(player, "money", 0))
        player.total_clicks = player_data.get(
            "total_clicks", getattr(player, "total_clicks", 0)
        )
        player.click_income = player_data.get(
            "click_income", getattr(player, "click_income", 0)
        )
        player.auto_income = player_data.get(
            "auto_income", getattr(player, "auto_income", 0)
        )

        # 🔹 Guardar también el dinero total dinámicamente
        player.total_money = player_data.get("total_money", player.money)

        # Restaurar datos de la tienda
        shop_data = data.get("shop", [])
        for item, saved_item in zip(getattr(shop, "items", []), shop_data):
            item.amount = saved_item.get("amount", getattr(item, "amount", 0))
            item.cost = saved_item.get("cost", getattr(item, "cost", 0))

        print(f"[LOAD] Partida cargada correctamente desde: {SAVE_FILE}")

    except Exception as e:
        print(f"[ERROR] No se pudo cargar la partida: {e}")
