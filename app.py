import os
from flask import Flask, request, render_template, redirect, url_for, flash
from werkzeug.utils import secure_filename
from openpyxl import load_workbook
from models import session as db_session, Order  # модель ниже покажу

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'xlsx'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/upload', methods=['GET', 'POST'])
def upload_excel():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            # Чтение Excel
            wb = load_workbook(filepath)
            ws = wb.active

            for row in ws.iter_rows(min_row=2):  # начинаем со 2-й строки
                track_code = row[0].value
                status = row[1].value
                flight = row[2].value

                if not track_code or status is None:
                    continue  # пропускаем пустые строки

                order = db_session.query(Order).filter_by(track_code=track_code).first()
                if order:
                    # Обновляем
                    order.status = status
                    order.flight = flight
                else:
                    # Добавляем новый
                    new_order = Order(track_code=track_code, status=status, flight=flight)
                    db_session.add(new_order)

            db_session.commit()
            flash("Файл успешно обработан!", "success")
            return redirect(url_for('upload_excel'))

        flash("Неверный формат файла. Загрузите .xlsx", "error")
    return render_template('upload.html')

