from flask import Flask, request, render_template, jsonify
from werkzeug.utils import secure_filename
import os
from classification import classify_image, get_label
from search import find_cheapest_car

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' not in request.files:
            return jsonify({'error': 'No file part'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400
        
        if file:
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            class_index, confidence = classify_image(filepath)
            model_name = get_label(class_index)
            cheapest_cars = find_cheapest_car(model_name)
            
            return jsonify({
                'model_name': model_name,
                'cheapest_cars': cheapest_cars,  # Send back the list of cheapest cars
                'confidence': confidence,  # Include the confidence score
                'filepath': filepath
            })
    
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)