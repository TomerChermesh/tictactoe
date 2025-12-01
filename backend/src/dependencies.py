from fastapi import Depends
from src.dal.users import UsersDAL
from src.dal.matchups import MatchupsDAL
from src.dal.games import GamesDAL
from src.services.game import GameService


def get_users_dal() -> UsersDAL:
    return UsersDAL()


def get_matchups_dal() -> MatchupsDAL:
    return MatchupsDAL()


def get_games_dal() -> GamesDAL:
    return GamesDAL()


def get_game_service(
    matchups_dal: MatchupsDAL = Depends(get_matchups_dal),
    games_dal: GamesDAL = Depends(get_games_dal)
) -> GameService:
    return GameService(matchups_dal=matchups_dal, games_dal=games_dal)
