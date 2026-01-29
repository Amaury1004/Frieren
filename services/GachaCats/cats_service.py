from config import config
from services.GachaCats.Cats_networck import CatsNetwork

cats = CatsNetwork(api_key=config.CAT_API_KEY)