from decouple import config


ADMINS = config('ADMINS', cast=lambda v: set(int(x) for x in v.split()))
COINGECKO_API_URL = config('COINGECKO_API_URL','https://api.coingecko.com/api/v3')
DATABASE_URL = config('DATABASE_URL')
DATABASE_NAME = config('DATABASE_NAME')
