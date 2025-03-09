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
    CSV_PATH = os.path.join(os.getcwd(), './placementdata.csv')

    filter_ranges_query = f'''
    SELECT 
        MIN(CGPA) AS min_CGPA, MIN(Internships) AS min_Internships, MIN(Projects) AS min_Projects, 
        MIN("Workshops/Certifications") AS min_WC, MIN(AptitudeTestScore) AS min_ATS, MIN(SoftSkillsRating) AS min_SSR,
        MIN(SSC_Marks) AS min_SSC, MIN(HSC_Marks) AS min_HSC,
        MAX(CGPA) AS max_CGPA, MAX(Internships) AS max_Internships, MAX(Projects) AS max_Projects, 
        MAX("Workshops/Certifications") AS max_WC, MAX(AptitudeTestScore) AS max_ATS, MAX(SoftSkillsRating) AS max_SSR,
        MAX(SSC_Marks) AS max_SSC, MAX(HSC_Marks) AS max_HSC
    FROM '{CSV_PATH}'
    '''

    filter_ranges_results = duckdb.sql(filter_ranges_query).df().fillna(0)

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

    placement_count_query = '''
    SELECT PlacementStatus, COUNT(*) AS placement_count 
    FROM placementdata.csv 
    GROUP BY PlacementStatus 
    ORDER BY placement_count DESC
    '''
    
    placement_count_results = duckdb.sql(placement_count_query).df()
    max_placement_count = placement_count_results['placement_count'].max() if not placement_count_results.empty else 100

    return render_template(
        'index.html', 
        ExtracurricularActivities=ExtracurricularActivities, 
        PlacementTraining=PlacementTraining,
        PlacementStatus=PlacementStatus,
        filter_ranges=filter_ranges,
        placement_count=max_placement_count
    )

@app.route('/update', methods=["POST"])
def update():
    request_data = request.get_json()

    x_column = request_data.get('x', 'CGPA')  # 默认 X 轴变量
    y_column = request_data.get('y', 'AptitudeTestScore')  # 默认 Y 轴变量
    CSV_PATH = os.path.join(os.getcwd(), './placementdata.csv')

    # Filtering query based on user input
    filter_query = f'''
    SELECT CGPA, Internships, Projects, "Workshops/Certifications", 
           AptitudeTestScore, SoftSkillsRating, SSC_Marks, HSC_Marks, PlacementStatus
    FROM '{CSV_PATH}'
    WHERE CGPA BETWEEN {request_data['cgpa'][0]} AND {request_data['cgpa'][1]}
    AND Internships BETWEEN {request_data['internships'][0]} AND {request_data['internships'][1]}
    AND Projects BETWEEN {request_data['projects'][0]} AND {request_data['projects'][1]}
    AND "Workshops/Certifications" BETWEEN {request_data['wc'][0]} AND {request_data['wc'][1]}
    AND AptitudeTestScore BETWEEN {request_data['ats'][0]} AND {request_data['ats'][1]}
    AND SoftSkillsRating BETWEEN {request_data['ssr'][0]} AND {request_data['ssr'][1]}
    AND SSC_Marks BETWEEN {request_data['ssc'][0]} AND {request_data['ssc'][1]}
    AND HSC_Marks BETWEEN {request_data['hsc'][0]} AND {request_data['hsc'][1]}
    '''

    filtered_data = duckdb.sql(filter_query).df()

    x_min = filtered_data[x_column].min() 
    x_max = filtered_data[x_column].max() 
    y_min = filtered_data[y_column].min() 
    y_max = filtered_data[y_column].max()


    # default对比就是cgpa和ats，需要完成update_aggregate()
    #scatter_data = filtered_data[['CGPA', 'AptitudeTestScore']].rename(columns={'CGPA': 'X', 'AptitudeTestScore': 'Y'}).to_dict(orient='records')
    # scatter_data = filtered_data[[x_column, y_column]].rename(columns={x_column: 'X', y_column: 'Y'}).to_dict(orient='records')
    scatter_df = filtered_data[[x_column, y_column]].copy()
    # 如果两列名相同，则需要特殊处理
    if x_column == y_column:
        scatter_df.columns = ['X', 'Y']  # 强制改名
    else:
        scatter_df.rename(columns={x_column: 'X', y_column: 'Y'}, inplace=True)

    scatter_data = scatter_df.to_dict(orient='records')

    # bar_query = f'''
    # SELECT PlacementStatus, COUNT(*) AS count 
    # FROM '{CSV_PATH}' 
    # WHERE PlacementStatus IN ('Placed', 'NotPlaced')
    # GROUP BY PlacementStatus
    # '''
    # **更新 Bar Chart 数据（加入过滤条件）**
    bar_query = f'''
    SELECT PlacementStatus, COUNT(*) AS count 
    FROM '{CSV_PATH}'
    WHERE CGPA BETWEEN {request_data['cgpa'][0]} AND {request_data['cgpa'][1]}
    AND Internships BETWEEN {request_data['internships'][0]} AND {request_data['internships'][1]}
    AND Projects BETWEEN {request_data['projects'][0]} AND {request_data['projects'][1]}
    AND "Workshops/Certifications" BETWEEN {request_data['wc'][0]} AND {request_data['wc'][1]}
    AND AptitudeTestScore BETWEEN {request_data['ats'][0]} AND {request_data['ats'][1]}
    AND SoftSkillsRating BETWEEN {request_data['ssr'][0]} AND {request_data['ssr'][1]}
    AND SSC_Marks BETWEEN {request_data['ssc'][0]} AND {request_data['ssc'][1]}
    AND HSC_Marks BETWEEN {request_data['hsc'][0]} AND {request_data['hsc'][1]}
    GROUP BY PlacementStatus
    '''
    bar_data_df = duckdb.sql(bar_query).df()

    # Extract individual counts for each placement status
    if not bar_data_df.empty:
        # Create a dictionary mapping each status to its count
        counts = {row['PlacementStatus']: row['count'] for index, row in bar_data_df.iterrows()}
        placed_count = counts.get('Placed', 0)
        not_placed_count = counts.get('NotPlaced', 0)
    else:
        placed_count = 0
        not_placed_count = 0

    # Prepare bar chart data (renaming fields to X and Y for your front-end)
    bar_data = [
        {'X': 'Placed', 'Y': placed_count},
        {'X': 'Not Placed', 'Y': not_placed_count}
    ]

    # print(bar_data)
    return jsonify({
        "scatter1_data": scatter_data,
        "bar_data": bar_data,
        "scatter_x_range": [x_min, x_max], 
        "scatter_y_range": [y_min, y_max]
    })

if __name__ == "__main__":
    app.run(debug=True)
