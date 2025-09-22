import json

# Load schemes JSON
with open("schemefinderdataset.json", "r", encoding="utf-8") as f:
    schemes = json.load(f)

print("Provide your details (mandatory fields: category, occupation, age, state; others optional):\n")

# --- User input line by line ---
category_input = input("1) Category (Farmer / Construction Worker) [mandatory]: ").strip().lower()
occupation_input = input("2) Occupation (e.g., farmer, construction_worker) [mandatory]: ").strip().lower()

# Age input (mandatory)
age_input = input("3) Age [mandatory]: ").strip()
while not age_input.isdigit():
    age_input = input("Please enter a valid numeric age: ").strip()
age_input = int(age_input)

# State input (mandatory)
state_input = ""
while not state_input:
    state_input = input("4) State / Resident State [mandatory]: ").strip().lower()

# Optional inputs
land_input = input("5) Land owned in hectares (optional, leave blank if none): ").strip()
land_input = float(land_input) if land_input else None

crop_input = input("6) Crops grown (comma separated, optional): ").strip()
crops_list = [c.strip().lower() for c in crop_input.split(",")] if crop_input else None

worked_days_input = input("7) Worked days last year (optional): ").strip()
worked_days_input = int(worked_days_input) if worked_days_input else None

registered_input = input("8) Registered with board? (yes/no, optional): ").strip().lower()
if registered_input == "yes":
    registered_input = True
elif registered_input == "no":
    registered_input = False
else:
    registered_input = None

# --- User dictionary ---
user = {
    "category": category_input,
    "occupation": occupation_input,
    "age": age_input,
    "land_owned_hectares": land_input,
    "state": state_input,
    "crop_type": crops_list,
    "worked_days_last_year": worked_days_input,
    "registered_with_board": registered_input
}

# --- Matching function ---
def match_scheme(user, scheme):
    score = 0
    elig = scheme.get("eligibility", {})

    mandatory_score = 0

    # Category match
    if user.get("category") == scheme.get("category", "").lower():
        mandatory_score += 3

    # Occupation match
    elig_occupations = [o.lower() for o in elig.get("occupation", [])]
    if user.get("occupation") in elig_occupations:
        mandatory_score += 2

    # Age check (mandatory if defined)
    if "age" in elig:
        min_age = elig["age"].get("min", 0)
        max_age = elig["age"].get("max", 1000)
        if not (min_age <= user["age"] <= max_age):
            return 0

    # State check
    if "resident_state" in elig:
        if user["state"] != elig["resident_state"].lower():
            return 0
    else:
        # No state restriction, still eligible
        mandatory_score += 1

    score += mandatory_score

    # Optional scoring fields
    if "land_owned_hectares" in elig and user.get("land_owned_hectares") is not None:
        min_land = elig["land_owned_hectares"].get("min", 0)
        max_land = elig["land_owned_hectares"].get("max", 1000)
        if min_land <= user["land_owned_hectares"] <= max_land:
            score += 1

    if user.get("crop_type") and "crop_type" in elig:
        elig_crops = [c.lower() for c in elig["crop_type"]]
        if any(crop in elig_crops for crop in user["crop_type"]):
            score += 1

    if "worked_days_last_year" in elig and user.get("worked_days_last_year") is not None:
        min_days = elig["worked_days_last_year"].get("min", 0)
        if user["worked_days_last_year"] >= min_days:
            score += 1

    if "registered_with_board" in elig and user.get("registered_with_board") is not None:
        if user["registered_with_board"] == elig["registered_with_board"]:
            score += 1

    # Additional optional scoring
    for key in ["priority_groups", "joint_borrower_applicants", "credit_limit", "components", "implementation"]:
        if elig.get(key):
            score += 1

    return score

# --- Compute top matches ---
scored_schemes = [(scheme, match_scheme(user, scheme)) for scheme in schemes]
scored_schemes.sort(key=lambda x: x[1], reverse=True)

# --- Display top 5 results ---
print("\nTop recommended schemes for you:\n")
for scheme, score in scored_schemes[:5]:
    print(f"{scheme['scheme_id']} - {scheme['name']} (Match score: {score})")

    benefits = scheme.get("benefits", "N/A")
    if isinstance(benefits, list):
        benefits = "\n  - " + "\n  - ".join(benefits)
    print(f"Benefits: {benefits}")

    if "objectives" in scheme:
        objectives = scheme["objectives"]
        if isinstance(objectives, list):
            objectives = "\n  - " + "\n  - ".join(objectives)
        print(f"Objectives: {objectives}")

    if "implementation" in scheme:
        print("Implementation Info:")
        for k, v in scheme["implementation"].items():
            print(f"  {k}: {v}")

    print("\n")
