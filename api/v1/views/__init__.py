from flask import Blueprint

app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')

from api.v1.views.doctors import *
from api.v1.views.patients import *
from api.v1.views.access_logs import *
from api.v1.views.medications import *
from api.v1.views.medical_records import *