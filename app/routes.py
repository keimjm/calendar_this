import psycopg2
import os
from flask import Blueprint, render_template, redirect, url_for
from .forms import AppointmentForm
from datetime import datetime, timedelta


bp = Blueprint("main", __name__, url_prefix="/")

CONNECTION_PARAMETERS = {
    "user": os.environ.get("DB_USER"),
    "password": os.environ.get("DB_PASS"),
    "dbname": os.environ.get("DB_NAME"),
    "host": os.environ.get("DB_HOST"),
}

@bp.route("/", methods=["GET", "POST"])
def main():
    d = datetime.now()
    return redirect(url_for(".daily", year=d.year, month=d.month, day=d.day))



@bp.route("/<int:year>/<int:month>/<int:day>", methods=["GET", "POST"])
def daily(year, month, day):
  form = AppointmentForm()
  if form.validate_on_submit():
    with psycopg2.connect(**CONNECTION_PARAMETERS) as conn:
      with conn.cursor() as curs:
        params = {
          'name': form.name.data,
          'start_datetime': datetime.combine(form.start_date.data, form.start_time.data),
          'end_datetime': datetime.combine(form.end_date.data, form.end_time.data),
          'description': form.description.data,
          'private': form.private.data
        }
        curs.execute(f"""INSERT INTO appointments 
        (name, start_datetime, end_datetime, description, private)
        VALUES (%s, %s, %s, %s, %s)
        """, (params['name'], params['start_datetime'], params['end_datetime'], params['description'], params['private']))
    return redirect('/')
  with psycopg2.connect(**CONNECTION_PARAMETERS) as conn:
    with conn.cursor() as curs:
      day = datetime(year, month, day)
      next_day = day + timedelta(days=1)
      curs.execute("SELECT id, name, start_datetime, end_datetime FROM appointments WHERE start_datetime BETWEEN %(day)s AND %(next_day)s ORDER BY start_datetime;", {"day": day, "next_day":next_day})
      rows = curs.fetchall()
      return render_template("main.html", rows=rows, form=form)
