# 🧠 MindCheck — Student Stress Level Predictor

> *Answer a few questions. Understand your stress. Get actionable tips.*

## 🌟 What is MindCheck?

MindCheck is a machine learning powered web app that predicts a student's stress level — **Low, Medium, or High** — based on psychological, physical, academic, environmental, and social factors.

It doesn't just give a label. It shows a **confidence percentage**, highlights your **personal risk factors**, and gives you a **tailored action plan** with practical recommendations you can actually act on.

Built for students. Designed to feel human.

---

## 🚀 Live Demo

**App:** https://student-burnout-predictor-d9gr93cavnyrhrcruyznqi.streamlit.app/

---

## ✨ Features

- 🎯 **Stress Prediction** — Classifies stress into Low, Medium, or High with a confidence score
- 📊 **Probability Breakdown** — Visual bars showing the likelihood of each stress level
- ⚠️ **Risk Factor Detection** — Flags your most critical stress triggers with colour-coded pills
- 💡 **Personalised Recommendations** — Tailored advice for sleep, anxiety, academics, career, social life, and more
- 🧠 **Meaningful Questions** — No confusing number scales; every question is in plain English with emoji options
- 🎨 **Gen-Z Friendly Design** — Dark gradient UI, animated hero, glowing result cards, hover effects

---

## 🗂️ Project Structure

```
mindcheck/
│
├── stress_predictor_app.py      # Main Streamlit app
├── stress_predictor_model.pkl   # Trained Random Forest model
├── scaler.pkl                   # StandardScaler for preprocessing
├── requirements.txt             # Python dependencies
└── README.md                    # You are here
```

---

## 🧪 How It Works

```
Student answers 20 questions
         ↓
Answers are mapped to numeric values
         ↓
Tuned Random Forest model predicts stress level
         ↓
App shows result + confidence % + risk factors + recommendations
```

The app takes inputs across 5 categories — Psychological, Physical, Environment, Academic, and Social — and feeds them into a trained machine learning model that returns a prediction instantly.

---

## 📊 Model Details

| Property | Details |
|---|---|
| **Dataset** | Student Stress Factors (Kaggle, 1100 records) |
| **Features** | 20 (psychological, physical, academic, environmental, social) |
| **Target** | Stress Level — Low (0), Medium (1), High (2) |
| **Algorithm** | Random Forest Classifier |
| **Tuning** | GridSearchCV with 5-fold cross validation |
| **Best Parameters** | n_estimators=200, max_depth=None, min_samples_split=5, min_samples_leaf=2 |
| **Test Accuracy** | **90.9%** |

### Model Comparison

| Model | Accuracy |
|---|---|
| Logistic Regression | 88.2% |
| Decision Tree | 85.5% |
| Random Forest (default) | 89.0% |
| **Tuned Random Forest** ✅ | **90.9%** |

### Top Predictive Features

All 20 features showed strong correlation (>0.5) with stress level. The most influential were:

- Self Esteem (0.756)
- Bullying (0.751)
- Sleep Quality (0.749)
- Future Career Concerns (0.742)
- Anxiety Level (0.736)

---

## 🛠️ Tech Stack

| Layer | Tool |
|---|---|
| **Language** | Python 3.10+ |
| **Web Framework** | Streamlit |
| **ML Library** | Scikit-learn |
| **Data Processing** | Pandas, NumPy |
| **Visualisation** | Matplotlib, Seaborn |
| **Model Persistence** | Pickle |
| **Deployment** | Streamlit Community Cloud |

---

## 📁 Dataset

- **Source:** [Student Stress Factors — Kaggle](https://www.kaggle.com/datasets/rxnach/student-stress-factors-a-comprehensive-analysis)
- **Size:** 1,100 students
- **Features:** 20
- **Classes:** 3 (Low, Medium, High stress)
- **Missing Values:** None

---

## 🔍 ML Pipeline Summary

1. **Data Loading & Inspection** — shape, dtypes, null check
2. **EDA** — correlation heatmap, boxplots, distribution plots, group bar charts
3. **Preprocessing** — train/test split (80/20), stratified sampling, StandardScaler
4. **Modelling** — Logistic Regression, Decision Tree, Random Forest
5. **Evaluation** — accuracy, confusion matrix, classification report (precision, recall, F1)
6. **Hyperparameter Tuning** — GridSearchCV over 108 combinations, 540 total fits
7. **Model Saving** — Pickle for model and scaler
8. **Deployment** — Streamlit Community Cloud

---

## ⚠️ Disclaimer

MindCheck is a student project built for **awareness and educational purposes only**. It is not a clinical tool and should not be used as a substitute for professional mental health advice. If you are experiencing serious stress or mental health concerns, please reach out to a qualified counsellor or mental health professional.

---

## 👨‍💻 Author

Made with 💜 by a student, for students.

Feel free to fork, star ⭐, or contribute!

---

## 📄 License

This project is licensed under the MIT License — feel free to use and build on it.
