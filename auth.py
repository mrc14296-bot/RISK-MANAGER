from flask import request, session, redirect, url_for, flash
from flask_login import login_user, logout_user
from werkzeug.security import check_password_hash
from datetime import datetime
import uuid

from models import db, User
from app import get_month_end