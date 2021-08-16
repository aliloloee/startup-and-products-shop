import redis as red


# For docker
redis = red.Redis(host='cache', port=6379, db=1, password='root')

## For normal use_case
# redis = red.Redis(host='localhost', port=6379, db=1)