import csv

# Constants for metric weights
FIRST_PITCH_STRIKE_WEIGHT = 1
TWO_THIRDS_STRIKE_WEIGHT = 2
STRIKEOUT_WEIGHT = 5
WALK_WEIGHT = -5
LEADOFF_RETIRED_WEIGHT = 2
SOFT_CONTACT_WEIGHT = 3
MEDIUM_CONTACT_WEIGHT = 1
HARD_CONTACT_WEIGHT = -3
STRIKE_RATIO_BONUS = 2
NO_WALK_BONUS = 2
STRIKEOUT_TO_WALK_BONUS = 2
AVG_PITCHES_BONUS = 3

def print_intro():
    print("\nWelcome to the Pitching Outing Grader!")
    print("This program takes in metrics about pitching outings and uses process & outcome metrics to score an outing.")

def validate_csv_file(csv_file, required_fields):
    """
    Validates the structure of the CSV file.
    """
    try:
        with open(csv_file) as file:
            reader = csv.DictReader(file)
            if not all(field in reader.fieldnames for field in required_fields):
                raise ValueError(f"CSV file {csv_file} is missing required fields: {required_fields}")
    except FileNotFoundError:
        raise FileNotFoundError(f"The file {csv_file} was not found.")
    except Exception as e:
        raise RuntimeError(f"Error reading the file {csv_file}: {e}")

def loadin_data(csv_file):
    """
    Loads data from a CSV file and returns a list of outings.
    """
    required_fields = ['player_id', 'date', 'batters_faced', 'first_pitch_strikes', '2/3_strikes', 
                       'strikeouts', 'walks', 'total_pitches', 'strikes', 'soft_contact', 
                       'medium_contact', 'hard_contact', 'leadoff_retired']
    validate_csv_file(csv_file, required_fields)

    outings = []
    with open(csv_file) as file:
        reader = csv.DictReader(file)
        for row in reader:
            try:
                outing = {key: int(row[key]) if key not in ['player_id', 'date'] else row[key] 
                          for key in row}
                outings.append(outing)
            except ValueError as e:
                print(f"Error in data format: {e}")
    return outings

def calculate_score(outing):
    """
    Calculates the score of an outing based on predefined metrics and weights.
    """
    score = 0
    score += outing['first_pitch_strikes'] * FIRST_PITCH_STRIKE_WEIGHT
    score += outing['2/3_strikes'] * TWO_THIRDS_STRIKE_WEIGHT
    score += outing['strikeouts'] * STRIKEOUT_WEIGHT
    score += outing['walks'] * WALK_WEIGHT
    score += outing['leadoff_retired'] * LEADOFF_RETIRED_WEIGHT
    score += outing['soft_contact'] * SOFT_CONTACT_WEIGHT
    score += outing['medium_contact'] * MEDIUM_CONTACT_WEIGHT
    score += outing['hard_contact'] * HARD_CONTACT_WEIGHT

    if (outing['strikes'] / outing['total_pitches']) > 0.6:
        score += STRIKE_RATIO_BONUS
    if outing['walks'] == 0:
        score += NO_WALK_BONUS
    elif (outing['strikeouts'] / outing['walks']) > 1.5:
        score += STRIKEOUT_TO_WALK_BONUS

    avg_pitches_per_ab = outing['total_pitches'] / outing['batters_faced']
    if avg_pitches_per_ab < 3.5:
        score += AVG_PITCHES_BONUS

    final_score = round(score / outing['batters_faced'], 2)
    print(f'Outing Score: {final_score}')
    return final_score

def save_score(scores, filename="player_scores.csv"):
    """
    Saves scores into a CSV file.
    """
    try:
        with open(filename, "w", newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["player_id", "date", "score"])
            for outing, score in scores:
                writer.writerow((outing['player_id'], outing['date'], score))
        print("Scores saved.")
    except Exception as e:
        print(f"Error saving scores: {e}")

def input_outing(filename="Outing.csv"):
    """
    Allows the user to input a new outing and appends it to the CSV file.
    """
    fieldnames = ['player_id', 'date', 'batters_faced', 'first_pitch_strikes', '2/3_strikes', 
                  'strikeouts', 'walks', 'total_pitches', 'strikes', 'soft_contact', 
                  'medium_contact', 'hard_contact', 'leadoff_retired']
    outing = {}
    for field in fieldnames:
        if field in ['player_id', 'date']:
            outing[field] = input(f"{field.replace('_', ' ').title()}: ")
        else:
            while True:
                try:
                    outing[field] = int(input(f"{field.replace('_', ' ').title()}: "))
                    break
                except ValueError:
                    print(f"Invalid input. Please enter an integer for {field}.")

    try:
        with open(filename, "a", newline='') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writerow(outing)
        print("Data successfully saved to file.")
    except Exception as e:
        print(f"Error saving outing: {e}")

def main():
    print_intro()
    user = input("Would you like to Grade or Add an outing?(A to add, G to Grade): ")
    if user.upper() == 'A':
        input_outing()
    elif user.upper() == 'G':
        input_file = "Outing.csv"
        outings = loadin_data(input_file)
        scores = []
        for outing in outings:
            score = calculate_score(outing)
            scores.append((outing, score))
        save_score(scores)
    else:
        print(ValueError("Invalid Input."))

if __name__ == "__main__":
    main()
