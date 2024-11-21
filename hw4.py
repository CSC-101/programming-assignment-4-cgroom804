import sys
from logging import exception
import build_data
from data import CountyDemographics


def display(counties: list[build_data.CountyDemographics]):
    if not counties:
        print("No counties available")
        return None
    for county in counties:
        print("--------------------")
        print(f"County: {county.county}, State: {county.state}")
        print(f"Education:\n{county.education}")
        print(f"Ethnicities:\n{county.ethnicities}")
        print(f"Income:\n{county.income}")
        print("--------------------")

def filter_state(counties: list[build_data.CountyDemographics], state: str) -> list[build_data.CountyDemographics]:
    filtered_list = []
    for county in counties:
        if county.state == state:
            filtered_list.append(county)
    print(f"Filter: state == {state}, {len(filtered_list)} entries)")
    return filtered_list

def filter_gt(counties: list[build_data.CountyDemographics], level: str, field: str, value: float) -> list[build_data.CountyDemographics]:
    filtered_list = []
    for county in counties:
        if getattr(county, field)[level] > value:
            filtered_list.append(county)
    print(f"Filter: {field} gt, {len(filtered_list)} entries")
    return filtered_list

def filter_lt(counties: list[build_data.CountyDemographics], level: str, field: str, value: float) -> list[build_data.CountyDemographics]:
    filtered_list = []
    for county in counties:
        if getattr(county, field)[level] < value:
            filtered_list.append(county)
    print(f"Filter: {field} gt, {len(filtered_list)} entries")
    return filtered_list

def population_total(counties: list[build_data.CountyDemographics]):
    if counties:
        total = 0
        for county in counties:
            total += county.population["2014 Population"]
        print(f"2014 population: {total}")
        return counties

def population(counties: list[build_data.CountyDemographics], level: str, field: str):
    if counties:
        total = 0
        for county in counties:
            total += getattr(county, field)[level] * county.population["2014 Population"]
        print(f"2014 {field}.{level} population: {total}")
        return counties

def percent(counties: list[build_data.CountyDemographics], level: str, field: str):
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

def main(): # takes no arguments
    #operation = display.ops
    #print(operation)
    #operations_file = sys.argv[1]
    #operations_file = "inputs/bachelors_gt_60.ops"

    counties = build_data.get_data()
    try:
        with open(operation, "r") as file:
            print(f"{len(counties)} records loaded")
            for line in file:
                line = line.strip()
                if not line:
                    continue
                sections = line.split(":")
                operation =  sections[0]

                if operation == "display":
                    display(counties)
                elif operation == "filter-state":
                    state = sections[1]
                    result = filter_state(counties, state)
                elif operation == "filter-gt":
                    detail = sections[1].split(".")
                    level = detail[1]
                    value = float(sections[2])
                    field = detail[0]
                    result = filter_gt(counties, level, field, value)
                elif operation == "filter-lt":
                    detail = sections[1].split(".")
                    level = detail[1]
                    value = float(sections[2])
                    field = detail[0]
                    result = filter_lt(counties, level, field, value)
                elif operation == "population-total":
                    result = population_total(counties)
                elif operation == "population":
                    detail = sections[1].split(".")
                    level = detail[1]
                    field = detail[0]
                    result = population(counties, level, field)
                elif operation == "percent":
                    detail = sections[1].split(".")
                    level = detail[1]
                    field = detail[0]
                    result = percent(counties, level, field)
                else:
                    print(f"Error: '{operation}' not a valid operation")
    except FileNotFoundError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Error: {e}")

main()