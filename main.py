import emoji
from flask import Flask, render_template
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, URL
import csv
import emoji

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap5(app)


class CafeForm(FlaskForm):
    choices_coffee = [('☕️', '☕️'), ('☕️☕️', '☕️☕️'), ('☕️☕️☕️', '☕️☕️☕️'), ('☕️☕️☕️☕️', '☕️☕️☕️☕️'), ('☕️☕️☕️☕️☕️', '☕️☕️☕️☕️☕️')]
    choices_wifi = [('✘', '✘'), ('💪️', '💪️'), ('💪💪', '💪💪'), ('💪💪💪', '💪💪💪'), ('💪💪💪💪️', '💪💪💪💪️'), ('💪💪💪💪💪', '💪💪💪💪💪')]
    # choices_power = [('✘', '✘'), ('🔌️', '🔌️'), ('🔌🔌', '🔌🔌'), ('🔌🔌🔌', '🔌🔌🔌'), ('🔌🔌🔌🔌', '🔌🔌🔌🔌'), ('🔌🔌🔌🔌🔌', '🔌🔌🔌🔌🔌')]

    cafe = StringField('Cafe name', validators=[DataRequired()])
    url = StringField('Cafe Location on Google Maps (URL)', validators=[DataRequired(), URL(require_tld=True)])
    open_time = StringField('Opening Time e.g. 8AM', validators=[DataRequired()])
    close_time = StringField('Closing Time e.g. 5:30PM', validators=[DataRequired()])
    rating = SelectField('Coffee Rating', validators=[DataRequired()], choices=choices_coffee)
    wifi = SelectField('Wifi Strength Rating', validators=[DataRequired()], choices=choices_wifi)
    # power = SelectField('Power Socket Availability', validators=[DataRequired()], choices=choices_power)
    submit = SubmitField('Submit')

# Exercise:
# add: Location URL, open time, closing time, coffee rating, wifi rating, power outlet rating fields
# make coffee/wifi/power a select element with choice of 0 to 5.
#e.g. You could use emojis ☕️/💪/✘/🔌
# make all fields required except submit
# use a validator to check that the URL field has a URL entered.
# ---------------------------------------------------------------------------

def get_csv_data():
    with open('cafe-data.csv', newline='', encoding='utf-8') as csv_file:
        csv_data = csv.reader(csv_file, delimiter=',')
        list_of_rows = []
        for row in csv_data:
            list_of_rows.append(row)
        return list_of_rows

# all Flask routes below
@app.route("/")
def home():
    return render_template("index.html")


@app.route('/add', methods=['GET', 'POST'])
def add_cafe():
    form = CafeForm()

    if form.validate_on_submit():
        cafe = form.cafe.data
        url = form.url.data
        open_time = form.open_time.data
        close_time = form.close_time.data
        rating = form.rating.data
        wifi = form.wifi.data
        # power = form.power.data

        data_row = [cafe, url, open_time, close_time, rating, wifi]
        print(data_row)

        with open("cafe-data.csv", "a", encoding='utf-8', newline='') as file:
            add_data = csv.writer(file, lineterminator='\n')
            add_data.writerow(data_row)

        return render_template('success.html', cafe=cafe)

    # Exercise:
    # Make the form write a new row into cafe-data.csv
    # with   if form.validate_on_submit()
    return render_template('add.html', form=form)


@app.route('/cafes')
def cafes():
    list_of_rows = get_csv_data()
    return render_template('cafes.html', cafes=list_of_rows)


@app.route('/success')
def success(cafe):
    return render_template('success.html', cafe=cafe)

if __name__ == '__main__':
    app.run(debug=True)
