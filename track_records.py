class TrackRecords:
    def __init__(self):
        self.color_counts = {
            'Red': {'Upper Body': 0, 'Lower Body': 0},
            'Blue': {'Upper Body': 0, 'Lower Body': 0},
            'Green': {'Upper Body': 0, 'Lower Body': 0},
            'White': {'Upper Body': 0, 'Lower Body': 0},
            'Black': {'Upper Body': 0, 'Lower Body': 0},
            'Yellow': {'Upper Body': 0, 'Lower Body': 0},
            'Orange': {'Upper Body': 0, 'Lower Body': 0},
            'Purple': {'Upper Body': 0, 'Lower Body': 0},
            'Pink': {'Upper Body': 0, 'Lower Body': 0},
        }
        self.age_gender_distribution = {
            "(4-6)": {"Male": 0, "Female": 0},
            "(8-12)": {"Male": 0, "Female": 0},
            "(15-20)": {"Male": 0, "Female": 0},
            "(25-32)": {"Male": 0, "Female": 0},
            "(38-43)": {"Male": 0, "Female": 0},
            "(48-53)": {"Male": 0, "Female": 0},
            "(60-100)": {"Male": 0, "Female": 0}
        }

    def add_record(self, record):
        track_id, detected_date, detected_time, predicted_age, predicted_gender, upper_custum, lower_custum = record
        upper_custum_colour = upper_custum[0]
        lower_custum_colour = lower_custum[0]

        self.color_counts[upper_custum_colour]['Upper Body'] +=1
        self.color_counts[lower_custum_colour]['Lower Body'] +=1

        self.age_gender_distribution[predicted_age][predicted_gender] +=1


    def get_count_dicts(self):
        return self.color_counts, self.age_gender_distribution

if __name__ == '__main__':
    processor = TrackRecords()
    record = (1, "2023-10-18", "08:30:00", "(4-6)", "Male", ("Red", 78), ("Blue", 78))

    processor.add_record(record)

    color_counts, age_gender_distribution = processor.get_count_dicts()
    print("="*25)
    print("Color Counts:", color_counts)

    print("="*25)
    print("Age Gender Distribution:", age_gender_distribution)
