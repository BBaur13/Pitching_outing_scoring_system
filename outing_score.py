
import csv

def print_intro():
    print("\nWelcome to the Pitching Outing Grader!")
    print("This program takes in metrics about pitching outings and uses process & outcome metrics to score an outing.")


def loadin_data(csv_file):
    #takes in a csv file with the outing and all of its metrics and uses a dictionary to assign each data value to a key
    print("\nEnter a new outing:")
    outing = []
    with open(csv_file) as file:
        reader = csv.DictReader(file)
        for row in reader:
            outing.append({
            'player_id': row['player_id'],
            'date': row['date'],
            'batters_faced': int(row['batters_faced']),
            'first_pitch_strikes': int(row['first_pitch_strikes']),
            '2/3_strikes': int(row['2/3_strikes']),
            'strikeouts': int(row['strikeouts']),
            'walks': int(row['walks']),
            'total_pitches': int(row['total_pitches']),
            'strikes': int(row['strikes']),
            'soft_contact': int(row['soft_contact']),
            'medium_contact': int(row['medium_contact']),
            'hard_contact': int(row['hard_contact']),
            'leadoff_retired': int(row['leadoff_retired'])
})
    return outing
def calculate_score(outing):
    #Calculates the score based on the data,most straight forward part
    score = 0 
    score += outing['first_pitch_strikes'] 
    score += outing['2/3_strikes'] * 2
    score += outing['strikeouts'] * 5
    score -= outing['walks'] * 5
    score += outing['leadoff_retired'] * 2
    score += outing['soft_contact'] * 3
    score += outing['medium_contact'] 
    score -= outing['hard_contact'] * 3 
    
    if (outing['strikes'] / outing['total_pitches']) > 0.6:
        score += 2
    if outing['walks'] == 0:
        score += 2        
    elif (outing['strikeouts'] / outing['walks']) > 1.5:
        score += 2

    avg_pitches_per_ab = outing['total_pitches'] / outing['batters_faced']
    
    if (avg_pitches_per_ab < 3.5):
        score += 3
    else: 0
    final_score = round(score / outing['batters_faced'], 2)
    print(f' Outing Score: {final_score}')
    return final_score

def save_score(scores, filename="player_scores.csv"):
    #Saves players outing scores and puts it in a new seperate csv file called "player_scores.csv"
    with open("player_scores.csv", "w", newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["player_id", "date", "score"]) # creating the headers
        for outing, score in scores: # makes a row for each outing that will include player's name, outing date, and their score.
            writer.writerow((outing['player_id'], outing['date'], score))
    
    print("Scores saved.")
    
def input_outing(filename="Outing.csv"):
        #User can enter in the metrics of a new outing that will go into the outing.csv
        print("enter a new pitching outing: ")
        
        fieldnames = ['player_id', 'date', 'batters_faced', 'first_pitch_strikes', '2/3_strikes', 'strikeouts', 'walks', 'total_pitches', 'strikes', 'soft_contact','medium_contact', 'hard_contact','leadoff_retired'] # list we are about to use in our dictionary
        
        outing = {}
        outing['player_id'] = input("Player ID: ")
        outing['date'] = input("Date (MM-DD-YY): ")
        outing['batters_faced'] = int(input("Batters Faced: "))
        outing['total_pitches'] = int(input('Total Pitches: '))
        outing['strikes'] = int(input('# of Strikes: '))
        outing['first_pitch_strikes'] = int(input("First Pitch Strikes: "))
        outing['2/3_strikes'] = int(input ("2/3 Strikes: "))
        outing['strikeouts'] = int(input("Strikeouts: "))
        outing['walks'] = int(input("Walks: "))
        outing['leadoff_retired'] = int(input("# of leadoffs retired: "))
        outing['soft_contact'] = int(input("# of Soft Contact: "))
        outing['medium_contact'] = int(input("# of Medium Contact: "))
        outing['hard_contact'] = int(input("# of Hard Contact: "))

        with open(filename, "a", newline='') as file:
            # learned the hard way how a = append and w = write, this adds each of our 'fieldnames' to the 'outing.csv' file stated above.
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            file.write('\n')
            writer.writerow(outing)
            
            print("Data successfully saved to file.")
def save_cum_scores(scores, filename='cumulative_scores.csv'):
    #Saves total score of each player, same as save but now, if the names match we add them
    cumulative = {}
    #read initial file
    with open("player_scores.csv", newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            player = row['player_id']
            score = float(row['score'])
    #make new scores cumulative totals
    for outing, score in scores:
        player = outing['player_id']
        if player in cumulative:
            cumulative[player]['total_score'] += score
            cumulative[player]['outings'] += 1
        else:
            cumulative[player] = {'total_score': score, 'outings': 1} # creates dictionary for new player
    
    #sort players by total score, addition for another day
    
    
    #use the dictionary, and save to file
    with open('cumulative_scores.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['player_id', 'total_score', 'outings','average_score'])
        #average calculation down here
        for player in cumulative:
            total = cumulative[player]['total_score']
            count = cumulative[player]['outings']
            average = round(total / count, 2)
            writer.writerow([player, round(total, 2), count, average])
    print("Total scores saved.")
    
    

def main():
    #call all the functions here.
    print_intro()
    user = input("Would you like to Grade or Add an outing?(A to add, G to Grade): ")
    if user.upper() == 'A':
        input_outing()
    elif user.upper() == 'G':
        input_file = "Outing.csv"
        outings = loadin_data(input_file)
        scores =[]
        for outing in outings:
            score = calculate_score(outing)
            scores.append((outing, score))
        save_score(scores) 
        save_cum_scores(scores)
    else:
        print(ValueError("Invalid Input."))
         
        
if __name__ == "__main__":
    main()
    