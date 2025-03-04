from flask import Flask, render_template, request
import duckdb

app = Flask(__name__)

continuous_columns = ['Internships', 'Projects',
       'Workshops/Certifications', 'AptitudeTestScore', 'SoftSkillsRating',
        'SSC_Marks',
       'HSC_Marks']

@app.route('/')
def index():
    return True