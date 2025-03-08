from flask import Flask, render_template, request, jsonify
import duckdb
import os

app = Flask(__name__)

xy_columns = ['CGPA', 'Internships', 'Projects', 'Workshops/Certifications', 'AptitudeTestScore', 'SoftSkillsRating','SSC_Marks','HSC_Marks']
ExtracurricularActivities = ['Yes', 'No']
PlacementTraining = ['Yes', 'No']
PlacementStatus = ['Placed', 'Not Placed']

@app.route('/')
def index():
    # Ensure correct path for DuckDB CSV
    CSV_PATH = os.path.join(os.getcwd(), './placementdata.csv')

    # SQL Query to get filter ranges
    filter_ranges_query = f'''
    SELECT 
        MIN(CGPA) AS min_CGPA, MIN(Internships) AS min_Internships, MIN(Projects) AS min_Projects, 
        MIN("Workshops/Certifications") AS min_WC, MIN(AptitudeTestScore) AS min_ATS, MIN(SoftSkillsRating) AS min_SSR,
        MIN(SSC_Marks) AS min_SSC, MIN(HSC_Marks) AS min_HSC,
        MAX(CGPA) AS max_CGPA, MAX(Internships) AS max_Internships, MAX(Projects) AS max_Projects, 
        MAX("Workshops/Certifications") AS max_WC, MAX(AptitudeTestScore) AS max_ATS, MAX(SoftSkillsRating) AS max_SSR,
        MAX(SSC_Marks) AS max_SSC, MAX(HSC_Marks) AS max_H
    FROM '{CSV_PATH}'
    '''
    
    # Execute Query and Handle Missing Values
    filter_ranges_results = duckdb.sql(filter_ranges_query).df().fillna(0)

    # Store filter values
    filter_ranges = {
        "CGPA": (filter_ranges_results["min_CGPA"][0], filter_ranges_results["max_CGPA"][0]),
        "Internships": (filter_ranges_results["min_Internships"][0], filter_ranges_results["max_Internships"][0]),
        "Projects": (filter_ranges_results["min_Projects"][0], filter_ranges_results["max_Projects"][0]),
        "Workshops/Certifications": (filter_ranges_results["min_WC"][0], filter_ranges_results["max_WC"][0]),
        "AptitudeTestScore": (filter_ranges_results["min_ATS"][0], filter_ranges_results["max_ATS"][0]),
        "SoftSkillsRating": (filter_ranges_results["min_SSR"][0], filter_ranges_results["max_SSR"][0]),
        "SSC_Marks": (filter_ranges_results["min_SSC"][0], filter_ranges_results["max_SSC"][0]),
        "HSC_Marks": (filter_ranges_results["min_HSC"][0], filter_ranges_results["max_HSC"][0])
    }

    return render_template(
        'index.html', 
        ExtracurricularActivities=ExtracurricularActivities, 
        PlacementTraining=PlacementTraining,
        PlacementStatus=PlacementStatus,
        filter_ranges=filter_ranges
    )

@app.route('/update', methods=["POST"])
def update():
    request_data = request.get_json()
    print("Received Data:", request_data)  # Debugging

    # Dummy scatter plot data (replace with filtering logic)
    scatter_data = [
        {"X": 7.5, "Y": 65},
        {"X": 8.9, "Y": 90},
        {"X": 7.3, "Y": 82},
        {"X": 7.5, "Y": 85},
        {"X": 8.3, "Y": 86},
        {"X": 7.0, "Y": 71},
        {"X": 7.7, "Y": 76}
    ]
    
    bar_data = [
        { "X": "Yes", "Y": 50 },
        { "X": "No", "Y": 40 },
    ]

    return jsonify({
        "scatter1_data": scatter_data,
        "bar_data": bar_data  
    })

if __name__ == "__main__":
    app.run(debug=True)
