import os

from flask import Flask, url_for, render_template
from flask_wtf import FlaskForm
from werkzeug.utils import redirect, secure_filename
from wtforms import FileField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config['SECRET_KEY'] = "yandex_lyceum"
app.config['IMAGES'] = 4


class ImageForm(FlaskForm):
    image = FileField('Новое фото', validators=[DataRequired()])

    submit = SubmitField('Добавить')


@app.route('/carousel', methods=['POST', 'GET'])
def carousel():
    form = ImageForm()
    if form.validate_on_submit():
        i = form.image.data
        filename = secure_filename(i.filename)
        with open('static/img/car/' + filename, 'wb') as f:
            f.write(i.read())
        app.config['IMAGES'] += 1
        return redirect('carousel')
    images = os.listdir('static/img/car/')
    return render_template('carousel.html', images=[url_for('static', filename='img/car/' + image) for image in images],
                           form=form)


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
