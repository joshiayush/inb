from firebase_admin import get_app
from firebase_admin import firestore
from firebase_admin import credentials
from firebase_admin import initialize_app


def initialize_firebase() -> object:
    """Function initialize_firebase() initializes the firebase app, it also checks if 
    the app is being initialized more than once if yes then it catches the error returned 
    by the firebase_admin.initialize_app() function and hits another try for the get_app() 
    function if there is already an app then it returns it if not the it just return None.

    :Args:
        - {None}

    :Returns:
        - {object} Firebase app object if present, otherwise None.
    """
    try:
        return initialize_app(credentials.Certificate(
            "inb/inb/database/firebase/firebaseCreds/serviceAccountKey.json"))
    except ValueError:
        try:
            return get_app()
        except ValueError:
            return


def get_firestore_client() -> object:
    """Returns a client that can be used to interact with Google Cloud Firestore.

    :Args:
        - {None}

    :Returns:
        - {object} google.cloud.firestore.Firestore: A `Firestore Client`_.
    """
    try:
        return firestore.client()
    except ValueError:
        return
