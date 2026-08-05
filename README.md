# Loan-Approval-Prediction
https://loan-approval-prediction-zagr.onrender.com/

# 💳 Loan Approval Prediction

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![Machine Learning](https://img.shields.io/badge/Machine%20Learning-Scikit--Learn-orange.svg)](https://scikit-learn.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A Machine Learning project designed to automate and predict the loan eligibility of applicants based on their personal, financial, and occupational details. This system helps financial institutions streamline the decision-making process, reduce manual errors, and mitigate credit risk.

---

## 📌 Table of Contents
- [Project Overview](#-project-overview)
- [Dataset Features](#-dataset-features)
- [Workflow](#-workflow)
- [Installation & Setup](#-installation--setup)
- [Usage](#-usage)
- [Model Evaluation](#-model-evaluation)
- [Technologies Used](#-technologies-used)
- [Contributing](#-contributing)


---

## 🚀 Project Overview
Manual loan approval processes are often time-consuming and prone to human bias. This project builds a predictive model using historical financial and demographic data to instantly classify whether an applicant's loan application should be **approved** or **rejected**.

---

## 📊 Dataset Features
The dataset typically includes the following features:

| Feature Name | Description | Data Type |
| :--- | :--- | :--- |
| **Loan_ID** | Unique Loan Identifier | Categorical |
| **Gender** | Male / Female | Categorical |
| **Married** | Applicant dependency status (Yes / No) | Categorical |
| **Dependents** | Number of family members dependent on the applicant | Numeric |
| **Education** | Graduate / Not Graduate | Categorical |
| **Self_Employed** | Self-employment status (Yes / No) | Categorical |
| **ApplicantIncome** | Income of the applicant | Numeric |
| **CoapplicantIncome** | Income of the co-applicant | Numeric |
| **LoanAmount** | Loan amount requested (in thousands) | Numeric |
| **Loan_Amount_Term** | Term of loan in months | Numeric |
| **Credit_History** | Credit history meets guidelines (1 = Yes, 0 = No) | Categorical |
| **Property_Area** | Urban / Semi-Urban / Rural | Categorical |
| **Loan_Status** | Target variable (Approved: Y / N) | Categorical |

---

## 🔄 Workflow
1. **Data Preprocessing:** 
   - Handling missing/null values using imputation (mean/median for numerical, mode for categorical).
   - Encoding categorical variables (Label Encoding / One-Hot Encoding).
   - Outlier detection and feature scaling.
2. **Exploratory Data Analysis (EDA):** 
   - Visualizing correlations between features (e.g., Credit History vs. Loan Status, Applicant Income vs. Loan Amount).
3. **Model Training:** 
   - Training various classification algorithms such as Logistic Regression, Decision Trees, Random Forest, and Support Vector Machines (SVM).
4. **Evaluation & Optimization:** 
   - Comparing models using metrics like Accuracy, Precision, Recall, F1-Score, and ROC-AUC.

---

## ⚙️ Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/samirmore7/Loan-Approval-Prediction.git](https://github.com/samirmore7/Loan-Approval-Prediction.git)
   cd Loan-Approval-Prediction
Create a virtual environment (optional but recommended):

Bash
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
Install the required dependencies:

Bash
pip install -r requirements.txt
💻 Usage
Open the Jupyter Notebook or Python script in your workspace:

Bash
jupyter notebook
Run the data preprocessing and exploratory data analysis steps.

Train the machine learning models and generate predictions on test datasets.

📈 Model Evaluation
The models are evaluated primarily based on Accuracy and F1-Score to ensure that false positives and false negatives are minimized, protecting the institution from high-risk loans while maintaining a good customer approval rate.

🛠️ Technologies Used
Language: Python

Libraries:

pandas, numpy for data manipulation

matplotlib, seaborn for data visualization

scikit-learn for machine learning models and metrics

🤝 Contributing
Contributions, issues, and feature requests are welcome! Feel free to check the issues page.

Fork the Project

Create your Feature Branch (git checkout -b feature/AmazingFeature)

Commit your Changes (git commit -m 'Add some AmazingFeature')

Push to the Branch (git origin push feature/AmazingFeature)

Open a Pull Request
