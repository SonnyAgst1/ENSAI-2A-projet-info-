from typing import Dict, List
from datetime import date, datetime, timedelta
from collections import defaultdict
from sqlalchemy import func, and_

from database import SessionLocal
from business_objects.models import Activite

class StatistiquesService:
    """Service pour gérer les statistiques utilisateur"""