# ENSAI-2A-projet-info

pour executer test service PYTHONPATH=src python -m pytest src/tests_service/ -v

$env:PYTHONPATH = "$PWD\src"
>> pytest src/tests_service/ -v

commande lancer api : python -m uvicorn src.main_api:app --reload --host 0.0.0.0 --port 9000 --app-dir src