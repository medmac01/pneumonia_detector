
from flask import Flask, message_flashed
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from wtforms.validators import DataRequired

class uploadScanForm(FlaskForm):
    uploadedFile = FileField(validators=[])
    submit = SubmitField()

