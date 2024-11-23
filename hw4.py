import build_data
#imports the file build_data

#displays the demographics of a county
def display(counties: list[build_data.CountyDemographics]):
    #counties: A list of CountyDemographics objects.
    if not counties:
        print("No counties available")
        return None
    for county in counties:
        print(f"County: {county.county}, State: {county.state}")
        print(f"Education:\n{county.education}")
        print(f"Ethnicities:\n{county.ethnicities}")
        print(f"Income:\n{county.income}")
        print("--------------------")
    #Prints all the information in format

#filters counties by state
def filter_state(counties: list[build_data.CountyDemographics], state: str) -> list[build_data.CountyDemographics]:
    #counties: A list of CountyDemographics objects, state: abbreviation for state
    if counties:
        filtered_list = []
        for county in counties:
            if county.state == state:
                filtered_list.append(county)
        print(f"Filter: state == {state}, {len(filtered_list)} entries")
        return filtered_list
    #list[build_data.CountyDemographics]: A list of counties in the specified state.

#filters counties of a given level and field greater than the specified value
def filter_gt(counties: list[build_data.CountyDemographics], level: str, field: str, value: float) -> list[build_data.CountyDemographics]:
    #counties: A list of CountyDemographics objects, field: type of data, level: group in field, value: percent to be greater than
    if counties:
        filtered_list = []
        for county in counties:
            if getattr(county, field)[level] > value:
                filtered_list.append(county)
        print(f"Filter: {field} gt, {len(filtered_list)} entries")
        return filtered_list
    #list[build_data.CountyDemographics]: A list of counties in the given level and field greater than the specified value

#filters counties of a given level and field less than the specified value
def filter_lt(counties: list[build_data.CountyDemographics], level: str, field: str, value: float) -> list[build_data.CountyDemographics]:
    # counties: A list of CountyDemographics objects, field: type of data, level: group in field, value: percent to be greater than
    if counties:
        filtered_list = []
        for county in counties:
            if getattr(county, field)[level] < value:
                filtered_list.append(county)
        print(f"Filter: {field} lt, {len(filtered_list)} entries")
        return filtered_list
    #list[build_data.CountyDemographics]: A list of counties in the given level and field less than the specified value

#calculates total 2014 population of a list of counties
def population_total(counties: list[build_data.CountyDemographics]):
    # counties: A list of CountyDemographics objects
    if counties:
        total = 0
        for county in counties:
            total += county.population["2014 Population"]
        print(f"2014 population: {total}")
    #prints the total 2014 population of counties

#calculates the population of a specified level and field
def population(counties: list[build_data.CountyDemographics], level: str, field: str):
    # counties: A list of CountyDemographics objects, field: type of data, level: group in field
    if counties:
        total = 0
        for county in counties:
            total += getattr(county, field)[level] * county.population["2014 Population"]
        print(f"2014 {field}.{level} population: {total}")
    #prints the population of the specified level and field

#calculates the percentage of a population that is of a specified level and field
def percent(counties: list[build_data.CountyDemographics], level: str, field: str):
    # counties: A list of CountyDemographics objects, field: type of data, level: group in field
    if counties:
        total = 0
        for county in counties:
            total += county.population["2014 Population"]
        filtered_pop = 0
        for county in counties:
            filtered_pop += getattr(county, field)[level] * county.population["2014 Population"]
        if total != 0:
            total_percent = filtered_pop/total
            print(f"2014 {field}.{level} population: {total_percent}")
        else:
            print(f"2014 {field}.{level} population: 0")
        return counties
    #Prints the percentage of the population that is of the specified level and field

def main(): # takes no arguments
    operation = input("Provide an operation: ") #asks for an operation
    #input example: "inputs/bachelors_gt_60.ops"

    counties = build_data.get_data() #gets the list of counties
    with open(operation, "r") as file: #opens the given file
        print(f"{len(counties)} records loaded")
        for line in file: #reads file line by line
            line = line.strip()
            if not line:
                continue
            sections = line.split(":") #breaks up line into instructions
            operation =  sections[0]
            try:  # tries to run the following code
                #Checks which function to run
                if operation == "display":
                    display(counties)
                elif operation == "filter-state":
                    state = sections[1]
                    counties = filter_state(counties, state)
                elif operation == "filter-gt":
                    detail = sections[1].split(".")
                    level = detail[1]
                    value = float(sections[2])
                    field = detail[0].lower()
                    counties = filter_gt(counties, level, field, value)
                elif operation == "filter-lt":
                    detail = sections[1].split(".")
                    level = detail[1]
                    value = float(sections[2])
                    field = detail[0].lower()
                    counties = filter_lt(counties, level, field, value)
                elif operation == "population-total":
                    counties = population_total(counties)
                elif operation == "population":
                    detail = sections[1].split(".")
                    level = detail[1]
                    field = detail[0].lower()
                    counties = population(counties, level, field)
                elif operation == "percent":
                    detail = sections[1].split(".")
                    level = detail[1]
                    field = detail[0].lower()
                    counties = percent(counties, level, field)
                else:
                    print(f"Error: '{operation}' not a valid operation")
            #if the error is a file not found, print the following code
            except FileNotFoundError as e:
                print(f"Error: {e}")
            #if the error is an exception, print the following code
            except Exception as e:
                print(f"Error: {e}")

main() #runs the program