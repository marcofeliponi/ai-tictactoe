import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from xgboost import XGBClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import GridSearchCV
import joblib 

def train_model():
    df = pd.read_csv('collected_data.csv')

    X = df[[f'cell_{i}' for i in range(9)]].values
    y = df['move'].values

    encoder = LabelEncoder()
    y = encoder.fit_transform(y)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    param_grid = {
        'max_depth': [3, 4, 5],
        'learning_rate': [0.01, 0.1, 0.2],
        'n_estimators': [50, 100, 150],
        'subsample': [0.6, 0.8, 1.0],
    }

    grid_search = GridSearchCV(
        XGBClassifier(eval_metric='mlogloss'),
        param_grid,
        cv=3,
        scoring='accuracy'
    )
    
    grid_search.fit(X_train, y_train)
    best_model = grid_search.best_estimator_

    y_pred = best_model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Acurácia do modelo: {accuracy}")

    joblib.dump(best_model, 'game_model.pkl')
    joblib.dump(encoder, 'encoder.pkl')

def load_model():
    return joblib.load('game_model.pkl')

def load_encoder():
    return joblib.load('encoder.pkl')

def make_prevision(flattened_board):
    numeric_board = convert_board_to_numeric(flattened_board)
    model = load_model()
    encoder = load_encoder()
    predicted = model.predict([numeric_board])[0]
    return encoder.inverse_transform([predicted])[0]

def convert_board_to_numeric(board):
    mapping = {'X': 1, 'O': -1, '': 0}
    return [mapping[cell] for cell in board]

if __name__ == "__main__":
    train_model()
