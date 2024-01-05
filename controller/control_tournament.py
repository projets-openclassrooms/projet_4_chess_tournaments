class Tournament:
    def __init__(self, tournament_name, location, tournament_date, number_of_tours, description, players_ids, list_of_tours, etat_tournoi, tournament_id):
        self.tournament_name = tournament_name
        self.location = location
        self.tournament_date = tournament_date
        self.number_of_tours = number_of_tours
        self.description = description
        self.players_ids = players_ids
        self.list_of_tours = list_of_tours
        self.etat_tournoi = etat_tournoi
        self.tournament_id = tournament_id

    def __str__(self):
        return f"{self.tournament_name} - {self.location} - {self.tournament_date} - {self.number_of_tours} - {self.description} - {self.players_ids} - {self.list_of_tours} - {self.etat_tournoi} - {self.tournament_id}"

tournament_data = [
    {
        "tournament_name": "test",
        "location": "treg",
        "tournament_date": "11/12/2023",
        "number_of_tours": 8,
        "description": "test",
        "players_ids": ["35cf4d83-578e-4a46-9dc1-bd3285b0845f"],
        "list_of_tours": [],
        "etat_tournoi": "IN PROGRESS",
        "tournament_id": "35cf4d83-578e-4a46-9dc1-bd3285b0845f"
    },
    {
        "tournament_name": "peste",
        "location": "Est",
        "tournament_date": "14/01/1980",
        "number_of_tours": 9,
        "description": "pestez",
        "players_ids": ["9651d872-f5a0-4613-91e0-10e54d504eaa", "5d0fc995-ddad-4798-a50a-026acec5d8f0"],
        "list_of_tours": [],
        "etat_tournoi": "TO LAUNCH",
        "tournament_id": "00635d70-b643-4d36-abd6-6e1237d76603"
    }
]

tournaments = []

for tournament_data in tournament_data:
    tournaments.append(Tournament(**tournament_data))

for tournament in tournaments:
    print(tournament)
