import pandas as pd
from django.core.management.base import BaseCommand
from guide.models import Destination, Season, Activity, TravelRecommendation

class Command(BaseCommand):
    help = 'Import travel data from CSV file'
    
    def handle(self, *args, **options):
        csv_path = 'C:/Users/Pujan/Travel Guide/travel_data.csv'
        
        try:
            df = pd.read_csv(csv_path)
            self.stdout.write(self.style.SUCCESS(f'Successfully loaded CSV with {len(df)} rows'))
            
            created_count = 0
            for index, row in df.iterrows():
                # Get or create destination
                destination, _ = Destination.objects.get_or_create(
                    name=row['destination'].strip().title()
                )
                
                # Get or create season
                season, _ = Season.objects.get_or_create(
                    name=row['season'].strip().lower()
                )
                
                # Get or create activity
                activity, _ = Activity.objects.get_or_create(
                    name=row['activity'].strip().lower()
                )
                
                # Create or update recommendation
                recommendation, created = TravelRecommendation.objects.update_or_create(
                    destination=destination,
                    season=season,
                    activity=activity,
                    defaults={
                        'recommended_items': row['recommended_items'],
                        'famous_places': row['famous_places'],
                        'recommended_apps': row['recommended_apps'],
                        'tips': row['tips']
                    }
                )
                
                if created:
                    created_count += 1
            
            self.stdout.write(self.style.SUCCESS(
                f'Data import completed! Imported {created_count} new recommendations.'
            ))
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error importing data: {str(e)}'))
            import traceback
            traceback.print_exc()