import json

# Load schemes JSON
with open("schemefinderdataset.json", "r", encoding="utf-8") as f:
    schemes = json.load(f)

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

    # Age check
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

# --- Chatbot ---
user_data = {}
print("Hello! I am SchemeBot. I can help you find government schemes.")
print("Type 'exit' anytime to quit.\n")

while True:
    user_input = input("You:\n").strip().lower()
    
    if user_input == "exit":
        print("SchemeBot: Goodbye! Stay safe and good luck!")
        break

    # Simple conversation responses
    if any(greet in user_input for greet in ["hello", "hi", "hey"]):
        print("SchemeBot: Hello! I can suggest government schemes for you. Let's start with your details.")
        continue
    if "how are you" in user_input:
        print("SchemeBot: I'm just a bot, but I'm ready to help you find schemes!")
        continue
    if "thanks" in user_input or "thank you" in user_input:
        print("SchemeBot: You're welcome! Do you want to check for schemes now?")
        continue

    # Ask for mandatory inputs if not already provided
    if "category" not in user_data:
        print("SchemeBot: Enter your category (Farmer / Construction Worker):")
        user_data["category"] = input("You:\n").strip().lower()
        continue

    if "occupation" not in user_data:
        print("SchemeBot: Enter your occupation:")
        user_data["occupation"] = input("You:\n").strip().lower()
        continue

    if "age" not in user_data:
        while True:
            try:
                print("SchemeBot: Enter your age:")
                user_data["age"] = int(input("You:\n").strip())
                break
            except ValueError:
                print("Please enter a valid numeric age.")
        continue

    if "state" not in user_data:
        print("SchemeBot: Enter your state of residence:")
        user_data["state"] = input("You:\n").strip().lower()
        continue

    # Ask optional inputs
    if "land_owned_hectares" not in user_data:
        print("SchemeBot: Land owned in hectares (optional, leave blank if none):")
        val = input("You:\n").strip()
        user_data["land_owned_hectares"] = float(val) if val else None
        continue

    if "crop_type" not in user_data:
        print("SchemeBot: Crops grown (comma separated, optional):")
        val = input("You:\n").strip()
        user_data["crop_type"] = [c.strip().lower() for c in val.split(",")] if val else None
        continue

    if "worked_days_last_year" not in user_data:
        print("SchemeBot: Worked days last year (optional):")
        val = input("You:\n").strip()
        user_data["worked_days_last_year"] = int(val) if val else None
        continue

    if "registered_with_board" not in user_data:
        print("SchemeBot: Registered with board? (yes/no, optional):")
        val = input("You:\n").strip().lower()
        if val == "yes":
            user_data["registered_with_board"] = True
        elif val == "no":
            user_data["registered_with_board"] = False
        else:
            user_data["registered_with_board"] = None
        continue

    # Compute top matches
    scored_schemes = [(scheme, match_scheme(user_data, scheme)) for scheme in schemes]
    scored_schemes.sort(key=lambda x: x[1], reverse=True)

    print("\nSchemeBot: Top recommended schemes for you:\n")
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

    # Clear optional fields to allow updated input next time
    for key in ["land_owned_hectares", "crop_type", "worked_days_last_year", "registered_with_board"]:
        if key in user_data:
            del user_data[key]
