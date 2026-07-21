import pickle
import numpy as np
from flask import Flask, render_template_string, request

app = Flask(__name__)

# Load the trained linear regression model
with open('linear_model.pkl', 'rb') as f:
    model = pickle.load(f)

# HTML Template with Embedded CSS Styling and CSS Animations
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dream Home Price Predictor 🏡✨</title>
    <link href="https://fonts.googleapis.com/css2?family=Fredoka:wght@400;500;600&family=Poppins:wght@300;400;600&display=swap" rel="stylesheet">
    <style>
        :root {
            --primary: #ff85a2;
            --primary-hover: #ff6086;
            --bg-gradient: linear-gradient(135deg, #ffdde1 0%, #ee9ca7 50%, #a1c4fd 100%);
            --card-bg: rgba(255, 255, 255, 0.92);
            --text-color: #4a4a4a;
            --accent: #70a1ff;
        }

        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }

        body {
            font-family: 'Poppins', sans-serif;
            background: var(--bg-gradient);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 30px 15px;
            color: var(--text-color);
        }

        .container {
            background: var(--card-bg);
            backdrop-filter: blur(10px);
            border-radius: 24px;
            padding: 35px 30px;
            max-width: 850px;
            width: 100%;
            box-shadow: 0 15px 35px rgba(0, 0, 0, 0.1);
            animation: floatIn 0.8s ease-out;
        }

        @keyframes floatIn {
            from {
                opacity: 0;
                transform: translateY(30px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }

        .header {
            text-align: center;
            margin-bottom: 30px;
        }

        .header h1 {
            font-family: 'Fredoka', cursive;
            font-size: 2.2rem;
            color: #ff527b;
            margin-bottom: 8px;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 10px;
        }

        .header p {
            font-size: 0.95rem;
            color: #666;
        }

        .grid-form {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
            gap: 18px;
        }

        .form-group {
            display: flex;
            flex-direction: column;
        }

        .form-group label {
            font-size: 0.88rem;
            font-weight: 600;
            margin-bottom: 6px;
            color: #555;
            display: flex;
            align-items: center;
            gap: 6px;
        }

        .form-group input, .form-group select {
            padding: 10px 14px;
            border-radius: 12px;
            border: 2px solid #e0e0e0;
            outline: none;
            font-size: 0.9rem;
            transition: all 0.3s ease;
            background: #fff;
        }

        .form-group input:focus, .form-group select:focus {
            border-color: var(--primary);
            box-shadow: 0 0 10px rgba(255, 133, 162, 0.3);
            transform: scale(1.02);
        }

        .submit-btn {
            grid-column: 1 / -1;
            margin-top: 15px;
            background: linear-gradient(45deg, #ff758c, #ff7eb3);
            color: white;
            border: none;
            padding: 14px;
            font-size: 1.1rem;
            font-weight: 600;
            border-radius: 16px;
            cursor: pointer;
            transition: all 0.3s ease;
            box-shadow: 0 8px 20px rgba(255, 117, 140, 0.4);
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 8px;
        }

        .submit-btn:hover {
            transform: translateY(-3px) scale(1.01);
            box-shadow: 0 12px 25px rgba(255, 117, 140, 0.6);
            background: linear-gradient(45deg, #ff6086, #ff6a9e);
        }

        .result-card {
            margin-top: 30px;
            padding: 20px;
            border-radius: 16px;
            background: #eef5ff;
            border: 2px dashed #70a1ff;
            text-align: center;
            animation: bounceIn 0.6s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        }

        @keyframes bounceIn {
            0% { transform: scale(0.8); opacity: 0; }
            100% { transform: scale(1); opacity: 1; }
        }

        .result-card h2 {
            font-family: 'Fredoka', cursive;
            color: #2b5292;
            font-size: 1.8rem;
            margin-top: 5px;
        }
    </style>
</head>
<body>

    <div class="container">
        <div class="header">
            <h1>🏡 Dream House Valuer ✨</h1>
            <p>Fill in the details below to predict the estimated market price! 💕</p>
        </div>

        <form method="POST" action="/predict" class="grid-form">
            <div class="form-group">
                <label>🛏️ Bedrooms</label>
                <input type="number" name="bedrooms" value="3" min="0" required>
            </div>

            <div class="form-group">
                <label>🛁 Bathrooms</label>
                <input type="number" step="0.25" name="bathrooms" value="2" min="0" required>
            </div>

            <div class="form-group">
                <label>📐 Living Area (sqft)</label>
                <input type="number" name="living_area" value="2000" required>
            </div>

            <div class="form-group">
                <label>🌳 Lot Area (sqft)</label>
                <input type="number" name="lot_area" value="5000" required>
            </div>

            <div class="form-group">
                <label>🏢 Floors</label>
                <input type="number" step="0.5" name="floors" value="1.5" required>
            </div>

            <div class="form-group">
                <label>🌊 Waterfront Present</label>
                <select name="waterfront">
                    <option value="0">No ❌</option>
                    <option value="1">Yes 🌊</option>
                </select>
            </div>

            <div class="form-group">
                <label>👀 Views Rating (0-4)</label>
                <input type="number" name="views" value="0" min="0" max="4" required>
            </div>

            <div class="form-group">
                <label>🛠️ Condition (1-5)</label>
                <input type="number" name="condition" value="3" min="1" max="5" required>
            </div>

            <div class="form-group">
                <label>⭐ House Grade (1-13)</label>
                <input type="number" name="grade" value="7" min="1" max="13" required>
            </div>

            <div class="form-group">
                <label>🏠 Above Area (sqft)</label>
                <input type="number" name="area_above" value="1600" required>
            </div>

            <div class="form-group">
                <label>🚪 Basement Area (sqft)</label>
                <input type="number" name="area_basement" value="400" required>
            </div>

            <div class="form-group">
                <label>📅 Built Year</label>
                <input type="number" name="built_year" value="1995" required>
            </div>

            <div class="form-group">
                <label>🔨 Renovation Year</label>
                <input type="number" name="renovation_year" value="0" required>
            </div>

            <div class="form-group">
                <label>🌿 Lot Area Renovated</label>
                <input type="number" name="lot_area_renov" value="5000" required>
            </div>

            <div class="form-group">
                <label>🏫 Nearby Schools</label>
                <input type="number" name="schools" value="2" min="0" required>
            </div>

            <div class="form-group">
                <label>✈️ Airport Distance (km)</label>
                <input type="number" step="0.1" name="airport_dist" value="15" required>
            </div>

            <button type="submit" class="submit-btn">
                ✨ Predict Valuation ✨
            </button>
        </form>

        {% if prediction %}
        <div class="result-card">
            <p>🎉 Estimated House Valuation 🎉</p>
            <h2>${{ prediction }}</h2>
        </div>
        {% endif %}
    </div>

</body>
</html>
"""

@app.route('/', methods=['GET'])
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Extract features in exact order as expected by model:
        features = [
            float(request.form['bedrooms']),
            float(request.form['bathrooms']),
            float(request.form['living_area']),
            float(request.form['lot_area']),
            float(request.form['floors']),
            float(request.form['waterfront']),
            float(request.form['views']),
            float(request.form['condition']),
            float(request.form['grade']),
            float(request.form['area_above']),
            float(request.form['area_basement']),
            float(request.form['built_year']),
            float(request.form['renovation_year']),
            float(request.form['lot_area_renov']),
            float(request.form['schools']),
            float(request.form['airport_dist'])
        ]
        
        # Reshape for 2D prediction array
        final_features = np.array([features])
        prediction_val = model.predict(final_features)[0]
        formatted_prediction = f"{prediction_val:,.2f}"

        return render_template_string(HTML_TEMPLATE, prediction=formatted_prediction)

    except Exception as e:
        return render_template_string(HTML_TEMPLATE, prediction=f"Error processing input: {str(e)}")

if __name__ == '__main__':
    app.run(debug=True)
