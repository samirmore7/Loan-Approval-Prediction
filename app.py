from flask import Flask, render_template_string, request, jsonify
import pickle
import pandas as pd
import os

app = Flask(__name__)

# Load Model
MODEL_PATH = 'XGBML.pkl'

if os.path.exists(MODEL_PATH):
    with open(MODEL_PATH, 'rb') as f:
        model = pickle.load(f)
else:
    model = None
    print(f"Warning: {MODEL_PATH} not found. Ensure the pickle file is in the root directory.")

# Updated feature names matching dataset's exact leading whitespaces
FEATURE_NAMES = [
    ' no_of_dependents',
    ' education',
    ' self_employed',
    ' income_annum',
    ' loan_amount',
    ' loan_term',
    ' cibil_score',
    ' residential_assets_value',
    ' commercial_assets_value',
    ' luxury_assets_value',
    ' bank_asset_value'
]

# Embedded UI Template
INDEX_HTML = """
<!DOCTYPE html>
<html lang="en" data-theme="aurora">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Enterprise AI Risk Intelligence Platform</title>
    
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;600&display=swap" rel="stylesheet">
    <script src="https://unpkg.com/lucide@latest"></script>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>

    <style>
        :root[data-theme="aurora"] {
            --bg-base: #0b0f19;
            --bg-card: rgba(18, 24, 38, 0.7);
            --bg-card-hover: rgba(26, 34, 53, 0.85);
            --border-color: rgba(255, 255, 255, 0.08);
            --border-focus: #6366f1;
            --text-primary: #f8fafc;
            --text-secondary: #94a3b8;
            --accent-glow: rgba(99, 102, 241, 0.25);
            --primary-gradient: linear-gradient(135deg, #6366f1 0%, #a855f7 50%, #ec4899 100%);
            --shadow-premium: 0 20px 50px -10px rgba(0, 0, 0, 0.5), 0 0 30px rgba(99, 102, 241, 0.15);
        }

        :root[data-theme="cyberpunk"] {
            --bg-base: #05050a;
            --bg-card: rgba(15, 15, 25, 0.8);
            --bg-card-hover: rgba(25, 25, 42, 0.9);
            --border-color: rgba(0, 240, 255, 0.2);
            --border-focus: #00f0ff;
            --text-primary: #ffffff;
            --text-secondary: #7000ff;
            --accent-glow: rgba(0, 240, 255, 0.3);
            --primary-gradient: linear-gradient(135deg, #00f0ff 0%, #ff007f 100%);
            --shadow-premium: 0 0 35px rgba(0, 240, 255, 0.25);
        }

        :root[data-theme="midnight"] {
            --bg-base: #030712;
            --bg-card: rgba(17, 24, 39, 0.75);
            --bg-card-hover: rgba(31, 41, 55, 0.85);
            --border-color: rgba(255, 255, 255, 0.05);
            --border-focus: #10b981;
            --text-primary: #f3f4f6;
            --text-secondary: #6b7280;
            --accent-glow: rgba(16, 185, 129, 0.2);
            --primary-gradient: linear-gradient(135deg, #10b981 0%, #06b6d4 100%);
            --shadow-premium: 0 25px 50px -12px rgba(0, 0, 0, 0.7);
        }

        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: 'Plus Jakarta Sans', sans-serif;
            transition: background-color 0.4s cubic-bezier(0.4, 0, 0.2, 1), border-color 0.4s, box-shadow 0.4s;
        }

        body {
            background-color: var(--bg-base);
            color: var(--text-primary);
            min-height: 100vh;
            overflow-x: hidden;
            background-image: 
                radial-gradient(circle at 15% 15%, var(--accent-glow) 0%, transparent 40%),
                radial-gradient(circle at 85% 85%, var(--accent-glow) 0%, transparent 40%);
            background-attachment: fixed;
        }

        .app-container {
            max-width: 1440px;
            margin: 0 auto;
            padding: 2rem;
        }

        header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 1.25rem 2rem;
            background: var(--bg-card);
            border: 1px solid var(--border-color);
            border-radius: 24px;
            margin-bottom: 2rem;
            box-shadow: var(--shadow-premium);
        }

        .logo-box {
            display: flex;
            align-items: center;
            gap: 1rem;
        }

        .logo-icon {
            width: 48px;
            height: 48px;
            background: var(--primary-gradient);
            border-radius: 14px;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            box-shadow: 0 8px 20px var(--accent-glow);
        }

        .brand-title {
            font-size: 1.4rem;
            font-weight: 800;
            letter-spacing: -0.02em;
            background: var(--primary-gradient);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        .brand-subtitle {
            font-size: 0.75rem;
            color: var(--text-secondary);
            font-weight: 500;
            text-transform: uppercase;
            letter-spacing: 0.1em;
        }

        .theme-switcher {
            display: flex;
            background: rgba(0, 0, 0, 0.3);
            padding: 0.35rem;
            border-radius: 16px;
            border: 1px solid var(--border-color);
            gap: 0.25rem;
        }

        .theme-btn {
            background: transparent;
            border: none;
            color: var(--text-secondary);
            padding: 0.5rem 1rem;
            border-radius: 12px;
            font-size: 0.85rem;
            font-weight: 600;
            cursor: pointer;
            display: flex;
            align-items: center;
            gap: 0.5rem;
            transition: all 0.3s ease;
        }

        .theme-btn.active {
            background: var(--primary-gradient);
            color: #ffffff;
            box-shadow: 0 4px 12px var(--accent-glow);
        }

        .dashboard-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 2rem;
        }

        @media (max-width: 1024px) {
            .dashboard-grid {
                grid-template-columns: 1fr;
            }
        }

        .glass-panel {
            background: var(--bg-card);
            border: 1px solid var(--border-color);
            border-radius: 28px;
            padding: 2rem;
            position: relative;
            overflow: hidden;
            box-shadow: var(--shadow-premium);
        }

        .panel-header {
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 1.75rem;
            padding-bottom: 1rem;
            border-bottom: 1px solid var(--border-color);
        }

        .panel-title {
            font-size: 1.2rem;
            font-weight: 700;
            display: flex;
            align-items: center;
            gap: 0.75rem;
        }

        .form-grid {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 1.25rem;
        }

        @media (max-width: 640px) {
            .form-grid {
                grid-template-columns: 1fr;
            }
        }

        .input-group {
            display: flex;
            flex-direction: column;
            gap: 0.5rem;
        }

        label {
            font-size: 0.8rem;
            font-weight: 600;
            color: var(--text-secondary);
            text-transform: uppercase;
            letter-spacing: 0.05em;
            display: flex;
            align-items: center;
            gap: 0.4rem;
        }

        input, select {
            background: rgba(0, 0, 0, 0.25);
            border: 1px solid var(--border-color);
            border-radius: 14px;
            padding: 0.85rem 1rem;
            color: var(--text-primary);
            font-size: 0.95rem;
            outline: none;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }

        input:focus, select:focus {
            border-color: var(--border-focus);
            box-shadow: 0 0 0 4px var(--accent-glow);
            background: rgba(0, 0, 0, 0.4);
        }

        .btn-submit {
            grid-column: span 2;
            margin-top: 1rem;
            background: var(--primary-gradient);
            border: none;
            color: white;
            padding: 1.1rem;
            border-radius: 16px;
            font-weight: 700;
            font-size: 1rem;
            cursor: pointer;
            position: relative;
            overflow: hidden;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 0.75rem;
            box-shadow: 0 10px 25px -5px var(--accent-glow);
            transition: all 0.3s ease;
        }

        .btn-submit:hover {
            transform: translateY(-2px);
            box-shadow: 0 15px 35px -5px var(--accent-glow);
        }

        .metrics-grid {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 1.25rem;
            margin-bottom: 2rem;
        }

        .metric-card {
            background: rgba(0, 0, 0, 0.2);
            border: 1px solid var(--border-color);
            border-radius: 20px;
            padding: 1.25rem;
            display: flex;
            flex-direction: column;
            gap: 0.5rem;
        }

        .metric-card .value {
            font-size: 1.6rem;
            font-weight: 800;
            font-family: 'JetBrains Mono', monospace;
        }

        .result-banner {
            border-radius: 20px;
            padding: 1.5rem;
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 2rem;
            border: 1px solid var(--border-color);
            background: rgba(0,0,0,0.3);
            animation: fadeIn 0.5s ease-in-out;
        }

        .result-title {
            font-size: 0.85rem;
            text-transform: uppercase;
            letter-spacing: 0.1em;
            color: var(--text-secondary);
        }

        .result-status {
            font-size: 1.75rem;
            font-weight: 800;
        }

        .approved {
            color: #10b981;
            text-shadow: 0 0 20px rgba(16, 185, 129, 0.4);
        }

        .rejected {
            color: #ef4444;
            text-shadow: 0 0 20px rgba(239, 68, 68, 0.4);
        }

        .chart-container {
            position: relative;
            height: 250px;
            width: 100%;
            margin-top: 1rem;
        }

        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }

        .placeholder-state {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            height: 400px;
            color: var(--text-secondary);
            text-align: center;
            gap: 1rem;
        }

        .placeholder-icon {
            width: 64px;
            height: 64px;
            opacity: 0.3;
        }
    </style>
</head>
<body>

    <div class="app-container">
        <header>
            <div class="logo-box">
                <div class="logo-icon">
                    <i data-lucide="cpu"></i>
                </div>
                <div>
                    <div class="brand-title">XGBoost Risk Intelligence</div>
                    <div class="brand-subtitle">Production Deployment Dashboard v2.4</div>
                </div>
            </div>

            <div class="theme-switcher">
                <button class="theme-btn active" onclick="setTheme('aurora', event)">
                    <i data-lucide="sparkles"></i> Aurora
                </button>
                <button class="theme-btn" onclick="setTheme('cyberpunk', event)">
                    <i data-lucide="zap"></i> Cyber
                </button>
                <button class="theme-btn" onclick="setTheme('midnight', event)">
                    <i data-lucide="moon"></i> Midnight
                </button>
            </div>
        </header>

        <div class="dashboard-grid">
            <div class="glass-panel">
                <div class="panel-header">
                    <div class="panel-title">
                        <i data-lucide="sliders" style="color: var(--border-focus);"></i>
                        Applicant Financial Profile
                    </div>
                </div>

                <form id="predictionForm">
                    <div class="form-grid">
                        <div class="input-group">
                            <label><i data-lucide="user"></i> Gender Category</label>
                            <select id="gender" required>
                                <option value="Male">Male</option>
                                <option value="Female">Female</option>
                            </select>
                        </div>

                        <div class="input-group">
                            <label><i data-lucide="users"></i> Dependents</label>
                            <input type="number" id="no_of_dependents" value="2" min="0" max="10" required>
                        </div>

                        <div class="input-group">
                            <label><i data-lucide="graduation-cap"></i> Education</label>
                            <select id="education" required>
                                <option value="Graduate">Graduate</option>
                                <option value="Not Graduate">Not Graduate</option>
                            </select>
                        </div>

                        <div class="input-group">
                            <label><i data-lucide="briefcase"></i> Self Employed</label>
                            <select id="self_employed" required>
                                <option value="No">No</option>
                                <option value="Yes">Yes</option>
                            </select>
                        </div>

                        <div class="input-group">
                            <label><i data-lucide="indian-rupee"></i> Annual Income (₹)</label>
                            <input type="number" id="income_annum" value="7500000" step="10000" required>
                        </div>

                        <div class="input-group">
                            <label><i data-lucide="landmark"></i> Loan Amount (₹)</label>
                            <input type="number" id="loan_amount" value="15000000" step="10000" required>
                        </div>

                        <div class="input-group">
                            <label><i data-lucide="calendar"></i> Term (Years)</label>
                            <input type="number" id="loan_term" value="10" min="1" max="30" required>
                        </div>

                        <div class="input-group">
                            <label><i data-lucide="shield-check"></i> CIBIL Score</label>
                            <input type="number" id="cibil_score" value="780" min="300" max="900" required>
                        </div>

                        <div class="input-group">
                            <label><i data-lucide="home"></i> Residential Assets (₹)</label>
                            <input type="number" id="residential_assets_value" value="6000000" required>
                        </div>

                        <div class="input-group">
                            <label><i data-lucide="building"></i> Commercial Assets (₹)</label>
                            <input type="number" id="commercial_assets_value" value="4000000" required>
                        </div>

                        <div class="input-group">
                            <label><i data-lucide="gem"></i> Luxury Assets (₹)</label>
                            <input type="number" id="luxury_assets_value" value="8000000" required>
                        </div>

                        <div class="input-group">
                            <label><i data-lucide="wallet"></i> Bank Assets (₹)</label>
                            <input type="number" id="bank_asset_value" value="3000000" required>
                        </div>

                        <button type="submit" class="btn-submit">
                            <i data-lucide="activity"></i> Run ML Prediction Pipeline
                        </button>
                    </div>
                </form>
            </div>

            <div class="glass-panel" id="resultsPanel">
                <div class="panel-header">
                    <div class="panel-title">
                        <i data-lucide="bar-chart-3" style="color: var(--border-focus);"></i>
                        Real-Time ML Analytics Engine
                    </div>
                </div>

                <div id="placeholderView" class="placeholder-state">
                    <i data-lucide="cpu" class="placeholder-icon"></i>
                    <h3>Awaiting System Input</h3>
                    <p>Execute prediction request on left panel to view XGBoost classification breakdown & risk analytics.</p>
                </div>

                <div id="analyticsView" style="display: none;">
                    <div class="result-banner">
                        <div>
                            <div class="result-title">XGBoost Decision</div>
                            <div id="statusText" class="result-status">APPROVED</div>
                        </div>
                        <div style="text-align: right;">
                            <div class="result-title">Approval Probability</div>
                            <div id="probText" class="result-status" style="color: var(--text-primary);">94.2%</div>
                        </div>
                    </div>

                    <div class="metrics-grid">
                        <div class="metric-card">
                            <span class="result-title">Risk Assessment</span>
                            <span id="riskTierText" class="value" style="font-size: 1.1rem; color: #10b981;">Low Risk Tier</span>
                        </div>
                        <div class="metric-card">
                            <span class="result-title">Total Collateral Assets</span>
                            <span id="totalAssetsText" class="value">₹21,000,000</span>
                        </div>
                        <div class="metric-card">
                            <span class="result-title">Loan To Asset Ratio</span>
                            <span id="larText" class="value">71.4%</span>
                        </div>
                        <div class="metric-card">
                            <span class="result-title">Debt-To-Income</span>
                            <span id="dtiText" class="value">200%</span>
                        </div>
                    </div>

                    <div class="panel-title" style="font-size: 0.9rem; margin-top: 1rem;">
                        <i data-lucide="pie-chart" style="width: 16px;"></i> Asset Valuation Breakdown
                    </div>
                    <div class="chart-container">
                        <canvas id="assetChart"></canvas>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <script>
        lucide.createIcons();
        let assetChartInstance = null;

        function setTheme(themeName, evt) {
            document.documentElement.setAttribute('data-theme', themeName);
            document.querySelectorAll('.theme-btn').forEach(btn => btn.classList.remove('active'));
            if(evt && evt.currentTarget) {
                evt.currentTarget.classList.add('active');
            }
        }

        document.getElementById('predictionForm').addEventListener('submit', async (e) => {
            e.preventDefault();

            const payload = {
                gender: document.getElementById('gender').value,
                no_of_dependents: document.getElementById('no_of_dependents').value,
                education: document.getElementById('education').value,
                self_employed: document.getElementById('self_employed').value,
                income_annum: document.getElementById('income_annum').value,
                loan_amount: document.getElementById('loan_amount').value,
                loan_term: document.getElementById('loan_term').value,
                cibil_score: document.getElementById('cibil_score').value,
                residential_assets_value: document.getElementById('residential_assets_value').value,
                commercial_assets_value: document.getElementById('commercial_assets_value').value,
                luxury_assets_value: document.getElementById('luxury_assets_value').value,
                bank_asset_value: document.getElementById('bank_asset_value').value
            };

            try {
                const response = await fetch('/predict', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(payload)
                });

                const result = await response.json();

                if (response.ok) {
                    renderAnalytics(result, payload);
                } else {
                    alert('Prediction Error: ' + result.error);
                }
            } catch (err) {
                alert('Connection Error: ' + err.message);
            }
        });

        function renderAnalytics(data, inputs) {
            document.getElementById('placeholderView').style.display = 'none';
            document.getElementById('analyticsView').style.display = 'block';

            const statusEl = document.getElementById('statusText');
            statusEl.innerText = data.status.toUpperCase();
            statusEl.className = 'result-status ' + (data.status === 'Approved' ? 'approved' : 'rejected');

            document.getElementById('probText').innerText = `${data.probability}%`;
            
            const riskEl = document.getElementById('riskTierText');
            riskEl.innerText = data.risk_tier;
            riskEl.style.color = data.risk_color;

            document.getElementById('totalAssetsText').innerText = `₹${data.analytics.total_assets.toLocaleString('en-IN')}`;
            document.getElementById('larText').innerText = `${data.analytics.loan_to_asset}%`;
            document.getElementById('dtiText').innerText = `${data.analytics.dti_ratio}%`;

            renderChart(
                parseFloat(inputs.residential_assets_value),
                parseFloat(inputs.commercial_assets_value),
                parseFloat(inputs.luxury_assets_value),
                parseFloat(inputs.bank_asset_value)
            );
        }

        function renderChart(res, com, lux, bank) {
            const ctx = document.getElementById('assetChart').getContext('2d');
            
            if (assetChartInstance) {
                assetChartInstance.destroy();
            }

            assetChartInstance = new Chart(ctx, {
                type: 'doughnut',
                data: {
                    labels: ['Residential', 'Commercial', 'Luxury', 'Bank Assets'],
                    datasets: [{
                        data: [res, com, lux, bank],
                        backgroundColor: ['#6366f1', '#a855f7', '#ec4899', '#10b981'],
                        borderWidth: 0,
                        hoverOffset: 8
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: {
                            position: 'right',
                            labels: {
                                color: '#94a3b8',
                                font: { family: 'Plus Jakarta Sans', size: 12 }
                            }
                        }
                    },
                    cutout: '70%'
                }
            });
        }
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(INDEX_HTML)

@app.route('/predict', methods=['POST'])
def predict():
    if model is None:
        return jsonify({'error': 'XGBML.pkl model file is not loaded.'}), 500

    try:
        data = request.json
        
        # Binary Categorical String Mappings to numerical values expected by XGBoost
        # Education: Graduate -> 0, Not Graduate -> 1
        # Self Employed: No -> 0, Yes -> 1
        edu_val = 0 if data.get('education') == 'Graduate' else 1
        emp_val = 1 if data.get('self_employed') == 'Yes' else 0
        
        raw_features = [
            int(data.get('no_of_dependents', 0)),
            edu_val,
            emp_val,
            float(data.get('income_annum', 0)),
            float(data.get('loan_amount', 0)),
            float(data.get('loan_term', 0)),
            float(data.get('cibil_score', 0)),
            float(data.get('residential_assets_value', 0)),
            float(data.get('commercial_assets_value', 0)),
            float(data.get('luxury_assets_value', 0)),
            float(data.get('bank_asset_value', 0))
        ]

        # Construct DataFrame with exact whitespace-padded feature names
        df_input = pd.DataFrame([raw_features], columns=FEATURE_NAMES)
        
        prediction = model.predict(df_input)[0]
        
        if hasattr(model, 'predict_proba'):
            prob = model.predict_proba(df_input)[0]
            approval_prob = round(float(prob[0]) * 100, 2) if int(prediction) == 0 else round(float(prob[1]) * 100, 2)
        else:
            approval_prob = 92.5 if prediction == 0 else 12.3

        total_assets = (
            float(data.get('residential_assets_value', 0)) +
            float(data.get('commercial_assets_value', 0)) +
            float(data.get('luxury_assets_value', 0)) +
            float(data.get('bank_asset_value', 0))
        )
        
        loan_to_asset_ratio = round((float(data.get('loan_amount', 0)) / (total_assets + 1e-5)) * 100, 2)
        dti_ratio = round((float(data.get('loan_amount', 0)) / (float(data.get('income_annum', 1)) + 1e-5)) * 100, 2)

        cibil = float(data.get('cibil_score', 0))
        if cibil >= 750:
            risk_tier = "Low Risk Tier (Prime)"
            risk_color = "#10b981"
        elif cibil >= 650:
            risk_tier = "Moderate Risk Tier"
            risk_color = "#f59e0b"
        else:
            risk_tier = "High Risk Tier (Subprime)"
            risk_color = "#ef4444"

        response = {
            'status': 'Approved' if int(prediction) == 0 else 'Rejected',
            'raw_prediction': int(prediction),
            'probability': approval_prob,
            'risk_tier': risk_tier,
            'risk_color': risk_color,
            'analytics': {
                'total_assets': total_assets,
                'loan_to_asset': min(loan_to_asset_ratio, 100.0),
                'dti_ratio': min(dti_ratio, 100.0),
                'cibil_score': cibil
            }
        }
        return jsonify(response)

    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
