from typing import Optional, List, Dict
from datetime import date, datetime, time, timedelta
from sqlalchemy import and_, or_, func
from sqlalchemy.exc import IntegrityError
import gpxpy
import gpxpy.gpx

from database import SessionLocal
from business_objects.models import Utilisateur, Activite, Commentaire, likes


class ActiviteService:
    """Service pour gérer toutes les opérations liées aux activités"""