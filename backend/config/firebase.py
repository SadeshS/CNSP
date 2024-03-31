import firebase_admin
from firebase_admin import credentials, auth, firestore
from config.config import settings

cred = credentials.Certificate({
    "type": "service_account",
    "project_id": settings.FIREBASE_PROJECTID,
    "private_key_id": settings.FIREBASE_PRIVATEKEYID,
    "private_key": settings.FIREBASE_PRIVATEKEY.replace(r'\n', '\n'),
    "client_email": settings.FIREBASE_CLIENTEMAIL,
    "client_id": settings.FIREBASE_CLIENTID,
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": settings.FIREBASE_CLIENTx509CERTURL,
    "universe_domain": "googleapis.com"
})
firebase = firebase_admin.initialize_app(cred)

firebase_auth = auth

db = firestore.client()