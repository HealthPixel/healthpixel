from flask import Blueprint

auth = Blueprint('auth', __name__, url_prefix='/auth')

from auth.doc_auth import *
from auth.patient_auth import *
