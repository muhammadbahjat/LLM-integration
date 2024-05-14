from flask import Flask, jsonify, request, render_template
import json
import io
import csv
import logging
import cohere

app = Flask(__name__)
# Set up logging
logging.basicConfig(level=logging.DEBUG)

#My Cohere API key & initializing 
COHERE_API_KEY = '2s82belHdvmun8Yyvyqm8anu7w0jm0xOlG15Xm2V' 
co = cohere.Client(COHERE_API_KEY)

uploaded_data = None #global for uploaded data 

#type json 
def process_json_data(json_data):
    try:
        data = json.loads(json_data)
        return data
    except json.JSONDecodeError as e:
        return {'error': 'Invalid JSON format'}

#converting json to CSV function
def json_to_csv(json_data):
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=json_data[0].keys())
    writer.writeheader()
    writer.writerows(json_data)
    output.seek(0)
    return output

#endpoint for uploading linked with home.html 
@app.route('/upload', methods=['POST'])
def upload_file():
    global uploaded_data
    if request.method == 'POST':
        if 'file' not in request.files:
            return jsonify({'error': 'No file part in the request'}), 400
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400

        if file.filename.endswith('.json'):
            file_content = file.read().decode('utf-8')
            uploaded_data = process_json_data(file_content)
            return jsonify({'message': 'File uploaded successfully!', 'data': uploaded_data}) #if the file is uploaded successfully it will display the data and also msge that file uploaded.
                                        #remove upload if dont wanna see file uploaded data 
        else:
            return jsonify({'error': 'Unsupported file format'}), 400

    return render_template('home.html')

#function for analyzing data using cohere 
def analyze_data(prompt):
    logging.debug(f"Sending prompt to Cohere: {prompt}")
    try:
        stream = co.chat_stream(
            model='command-r-plus', 
            message=prompt,
            temperature=0.3,
            chat_history=[]
        )
        generated_text = ""
        for event in stream:
            if event.event_type == "text-generation":
                generated_text += event.text
        logging.debug(f"Cohere API response: {generated_text.strip()}")
        return generated_text.strip()
    except Exception as e:
        logging.error(f"Error from Cohere API: {str(e)}")
        return f"Error: {str(e)}"

#Prompt to get the desired requirement for each api endpoints
def create_detailed_prompt(data, analysis_type):
    if analysis_type == 'top_unit':
        prompt = "Analyze the following units and provide detailed feedback on which unit is the best:\n"
    elif analysis_type == 'unit_price_history':
        prompt = "Analyze the following units and provide feedback on which units have had the biggest price changes downwards. write to the point answer only:\n"
    elif analysis_type == 'building_deals':
        neighborhood = request.args.get('neighborhood')
        prompt = f"Analyze the following units in the {neighborhood} neighborhood and provide to the point feedback on which buildings are the best deals:\n"
    elif analysis_type == 'sales_rep_feedback':
        prompt = "Analyze the performance of the sales representative and provide a short feedback:\n"
    elif analysis_type == 'team_performance':
        prompt = "Analyze the overall performance of the sales team based on the following data and provide a short feedback:\n"
    else:
        prompt = "Analyze the following units:\n"

    for unit in data:
        unit_info = (
            f"Unit ID: {unit['id']}\n"
            f"Name: {unit['name']}\n"
            f"Address: {unit['address']}\n"
            f"City: {unit['city']}\n"
            f"Description: {unit['description']}\n"
            f"Neighborhood: {unit['neighborhood']}\n"
            f"Parking: {unit['parking']}\n"
            f"Washer Dryer: {unit['washer dryer']}\n"
            f"Balcony: {unit['balcony']}\n"
            f"Pet Policy: {unit['pet policy']}\n\n"
        )
        prompt += unit_info
    logging.debug(f"Created prompt: {prompt}")
    return prompt

#endpoints for top unit function 
@app.route('/api/top_unit', methods=['GET'])
def top_unit():
    global uploaded_data
    if not uploaded_data:
        return jsonify({'error': 'No data uploaded yet. Please upload data first.'}), 400
    prompt = create_detailed_prompt(uploaded_data, 'top_unit')
    feedback = analyze_data(prompt)
    return jsonify({'feedback': feedback})

#endpoint to find units with the biggest price changes downwards
@app.route('/api/unit_price_history', methods=['GET'])
def unit_price_history():
    global uploaded_data
    if not uploaded_data:
        return jsonify({'error': 'No data uploaded yet. Please upload data first.'}), 400
    prompt = create_detailed_prompt(uploaded_data, 'unit_price_history')
    feedback = analyze_data(prompt)
    return jsonify({'feedback': feedback})

#endpoint to find the best building deals in a particular neighborhood
@app.route('/api/building_deals', methods=['GET'])
def building_deals():
    global uploaded_data
    if not uploaded_data:
        return jsonify({'error': 'No data uploaded yet. Please upload data first.'}), 400
    neighborhood = request.args.get('neighborhood')
    if not neighborhood:
        return jsonify({'error': 'Missing neighborhood parameter'}), 400
    prompt = create_detailed_prompt(uploaded_data, 'building_deals')
    feedback = analyze_data(prompt)
    return jsonify({'feedback': feedback})

#endpoint for specific sales rep feedback
@app.route('/api/sales_rep_feedback', methods=['GET'])
def sales_rep_feedback():
    global uploaded_data
    if not uploaded_data:
        return jsonify({'error': 'No data uploaded yet. Please upload data first.'}), 400
    
    prompt = create_detailed_prompt(uploaded_data, 'sales_rep_feedback')
    feedback = analyze_data(prompt)
    return jsonify({'feedback': feedback})

#endpoint for getting team performance
@app.route('/api/team_performance', methods=['GET'])
def team_performance():
    global uploaded_data
    if not uploaded_data:
        return jsonify({'error': 'No data uploaded yet. Please upload data first.'}), 400
    
    prompt = create_detailed_prompt(uploaded_data, 'team_performance')
    feedback = analyze_data(prompt)
    return jsonify({'feedback': feedback})


if __name__ == '__main__':
    app.run(debug=True)
