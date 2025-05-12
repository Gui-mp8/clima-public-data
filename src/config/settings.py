#config/settings.py

SETTINGS: dict[str, type] = {
    "app":{
        "cores": 4,
        "inmet": {
            "strategy": {
                "year": 2024,
                "cities": [
                    "Barra do Ribeiro",
                    "Guaíba",
                    "Porto Alegre",
                    "Eldorado do Sul",
                    "Tapes",
                    "Arambare",
                    "Camaqua",
                    "Sao Lourenço",
                    "Canoas",
                    "Sao Leopoldo"
                ],
                "url": "https://portal.inmet.gov.br/uploads/dadoshistoricos/{year}.zip",
                # "years": range(2000, 2025+1),
            },
            "repository": {
                "year": 2024,
                "path": "data/inmet/{year}",
            },
        }
    }
}