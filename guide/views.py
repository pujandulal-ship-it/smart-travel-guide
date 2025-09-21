from django.shortcuts import render
from django.conf import settings
import joblib
import pandas as pd
from sklearn.preprocessing import LabelEncoder
import os
import requests
import numpy as np
import traceback

def home(request):
    print(f"DEBUG: Request method: {request.method}")
    print(f"DEBUG: POST data: {request.POST}")
    
    recommendations = None
    error_message = None
    
    if request.method == 'POST':
        destination = request.POST.get('destination', 'new york').lower().strip()
        season = request.POST.get('season', 'summer').lower().strip()
        activity = request.POST.get('activity', 'sightseeing').lower().strip()
        
        print(f"DEBUG: Processing request for {destination}, {season}, {activity}")
        
        try:
            
            model_path = 'C:/Users/Pujan/Travel Guide/guide/travel_recommendation_model.joblib'
            mlb_items_path = 'C:/Users/Pujan/Travel Guide/guide/multilabel_binarizer_items.joblib'
            
            if not os.path.exists(model_path):
                raise FileNotFoundError(f"Model file not found: {model_path}")
            if not os.path.exists(mlb_items_path):
                raise FileNotFoundError(f"Items binarizer not found: {mlb_items_path}")
            
            model = joblib.load(model_path)
            mlb_items = joblib.load(mlb_items_path)
            
            print(f"DEBUG: Model loaded successfully")
            print(f"DEBUG: mlb_items classes length: {len(mlb_items.classes_)}")
            
            
            label_encoders = {}
            encoder_paths = {
                'destination': 'C:/Users/Pujan/Travel Guide/guide/destination_encoder_classes.joblib',
                'season': 'C:/Users/Pujan/Travel Guide/guide/season_encoder_classes.joblib',
                'activity': 'C:/Users/Pujan/Travel Guide/guide/activity_encoder_classes.joblib'
            }
            
            for column, path in encoder_paths.items():
                if os.path.exists(path):
                    le = LabelEncoder()
                    le.classes_ = joblib.load(path)
                    label_encoders[column] = le
                    print(f"DEBUG: Loaded {column} encoder with {len(le.classes_)} classes")
                else:
                    print(f"WARNING: {column} encoder missing: {path}")
                    le = LabelEncoder()
                    le.classes_ = np.array(['unknown'])
                    label_encoders[column] = le
            
            input_data = pd.DataFrame([[destination, season, activity]], 
                                    columns=['destination', 'season', 'activity'])
            
            encoded_input = [0, 0, 0]  
            try:
                for i, column in enumerate(input_data.columns):
                    le = label_encoders[column]
                    if input_data[column][0] in le.classes_:
                        encoded_val = le.transform([input_data[column][0]])[0]
                    else:
                        encoded_val = 0  
                    encoded_input[i] = encoded_val
                    print(f"DEBUG: Encoded {column}: '{input_data[column][0]}' -> {encoded_val}")
                
                input_df = pd.DataFrame([encoded_input], columns=['destination', 'season', 'activity'])
                print(f"DEBUG: Encoded input: {input_df.values.tolist()}")
                
            except Exception as e:
                print(f"WARNING: Encoding failed: {e}")
                input_df = pd.DataFrame([[0, 0, 0]], columns=['destination', 'season', 'activity'])
            
            try:
                prediction = model.predict(input_df)
                binary_prediction = prediction[0]
                print(f"DEBUG: Prediction shape: {prediction.shape}")
                print(f"DEBUG: Binary prediction length: {len(binary_prediction)}")
                print(f"DEBUG: First 10 prediction values: {binary_prediction[:10].tolist()}")
                
                items_count = len(mlb_items.classes_)
                print(f"DEBUG: Items count: {items_count}")
                
                if len(binary_prediction) < items_count:
                    print(f"ERROR: Prediction too short ({len(binary_prediction)} < {items_count})")
                    recommended_items = ['comfortable shoes', 'water bottle', 'camera', 'light jacket', 'sunglasses', 'hat']
                else:
                    recommended_items = []
                    for i in range(min(items_count, len(binary_prediction))):
                        if binary_prediction[i] == 1:
                            recommended_items.append(mlb_items.classes_[i])
                    print(f"DEBUG: Found {len(recommended_items)} predicted items: {recommended_items}")
                
                recommended_items = recommended_items[:6]
                recommended_items_str = ', '.join(recommended_items) if recommended_items else 'No specific items recommended'
                
            except Exception as e:
                print(f"ERROR during prediction: {e}")
                traceback.print_exc()
                recommended_items_str = 'comfortable shoes, water bottle, camera, light jacket, sunglasses, hat'
            
            famous_places = ['Check out local landmarks!']
            recommended_apps = ['Consider a maps app like Google Maps.']
            tips = ['Carry a map and stay hydrated.']
            
            destination_overrides = {
                'new york': {
                    'places': ['Central Park', 'Times Square', 'Rockefeller Center'],
                    'apps': ['Citymapper', 'OpenTable', 'NYC Ferry'],
                    'tips': ['Get a MetroCard', 'Dress in layers', 'Book Broadway tickets']
                },
                'paris': {
                    'places': ['Eiffel Tower', 'Louvre Museum', 'Notre-Dame'],
                    'apps': ['Paris Metro', 'TripAdvisor', 'Citymapper'],
                    'tips': ['Learn basic French', 'Buy museum pass', 'Visit early']
                },
                'pokhara': {
                    'places': ['Phewa Lake', 'World Peace Pagoda', 'Tal Barahi Temple'],
                    'apps': ['Maps.me', 'Nepal Travel', 'Weather Nepal'],
                    'tips': ['Carry cash', 'Hire local guide', 'Check weather']
                },
                'tokyo': {
                    'places': ['Shibuya Crossing', 'Senso-ji Temple', 'Tokyo Tower'],
                    'apps': ['Japan Travel', 'Google Translate', 'Suica'],
                    'tips': ['Get Suica card', 'Learn basic Japanese', 'Try sushi']
                },
                'london': {
                    'places': ['Big Ben', 'Tower Bridge', 'British Museum'],
                    'apps': ['Citymapper', 'TfL Go', 'Visit London'],
                    'tips': ['Get Oyster card', 'Check weather', 'Try fish and chips']
                }
            }
            
            if destination in destination_overrides:
                overrides = destination_overrides[destination]
                famous_places = overrides.get('places', famous_places)
                recommended_apps = overrides.get('apps', recommended_apps)
                tips = overrides.get('tips', tips)
            
            
            weather = "sunny"  
            try:
                if hasattr(settings, 'WEATHER_API_KEY') and settings.WEATHER_API_KEY != '26c25838c2414732be4132435251809':
                    weather_url = f"http://api.weatherapi.com/v1/current.json?key={settings.WEATHER_API_KEY}&q={destination.replace(' ', '%20').capitalize()}"
                    weather_response = requests.get(weather_url, timeout=5)
                    if weather_response.status_code == 200:
                        weather_data = weather_response.json()
                        weather_condition = weather_data['current']['condition']['text']
                        temperature = weather_data['current']['temp_c']
                        weather = f"{weather_condition} ({temperature}°C)"
                        print(f"DEBUG: Weather API success: {weather}")
                    else:
                        print(f"DEBUG: Weather API failed with status {weather_response.status_code}")
                        weather = "sunny"
                else:
                    print("DEBUG: No valid Weather API key found")
                    weather = "sunny"
            except Exception as e:
                print(f"DEBUG: Weather API error: {e}")
                weather = "sunny"

            # Step 10: Create blog content
            famous_places_str = ', '.join(famous_places[:3]) if len(famous_places) > 1 else famous_places[0]
            recommended_apps_str = ', '.join(recommended_apps[:2]) if len(recommended_apps) > 1 else recommended_apps[0]
            tips_str = ', '.join(tips[:2]) if len(tips) > 1 else tips[0]
            
            blog_content = f"Since you are, going to {destination.capitalize()} in {season.capitalize()}! Don't miss {famous_places_str}. Don't forget to take {recommended_items_str}. For a hassle-free trip, use {recommended_apps_str} and follow these tips: {tips_str}. Current weather: {weather}"

            recommendations = {
                'destination': destination,
                'season': season,
                'activity': activity,
                'weather': weather,
                'items': recommended_items,
                'blog': blog_content
            }
            
            print(f"DEBUG: Recommendations created successfully")
            print(f"DEBUG: Final output - Items: {len(recommended_items)}, Places: {len(famous_places)}, Apps: {len(recommended_apps)}, Tips: {len(tips)}")

        except Exception as e:
            print(f"FATAL ERROR in home view: {e}")
            traceback.print_exc()
            import traceback
            traceback.print_exc()
            
            # Complete fallback
            recommendations = {
                'destination': destination,
                'season': season,
                'activity': activity,
                'weather': 'sunny',
                'items': ['comfortable shoes', 'water bottle', 'camera', 'light jacket', 'sunglasses'],
                'blog': f"Error generating recommendations for {destination}. Please try again with a different destination."
            }
            error_message = f"ML Error: {str(e)[:100]}..."
        if recommendations and hasattr(recommendations, 'blog') and recommendations.blog:
            tips = [tip.strip() for tip in recommendations.blog.split('.') if tip.strip()][:3]
    else:
            tips = []

    return render(request, 'guide/home.html', {'recommendations': recommendations, 'error_message': error_message})