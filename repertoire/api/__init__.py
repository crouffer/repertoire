from flask_restplus import Api

api = Api(
    version='0.1',
    title='Repertoire Song Catalogue',
    description='API For the Repertoire Song Catalogue',
    catch_all_404s=True,
    default_mediatype='application/json'
    )
