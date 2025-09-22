import json
import openai
import sys

openai.api_key = "YOUR_OPENAI_API_KEY_HERE"

with open("schemefinderdataset.json", "r", encoding="utf-8") as f:
    schemes = json.load(f)

def match_scheme(user, scheme):
    score = 0
    elig = scheme.get("eligibility", {})
    # Mandatory scoring fields



    # If User input occupation matches any in eligibility, give 3 points
    if user.get("category") == scheme.get("category", "").lower():
        score += 3



   
    # If User input occupation matches any in eligibility, give 2 points
    elig_occupations = [o.lower() for o in elig.get("occupation", [])]
    if user.get("occupation") in elig_occupations:
        score += 2




    # Age check,provides schemes only if in range
    if "age" in elig:
        min_age = elig["age"].get("min", 0)
        max_age = elig["age"].get("max", 1000)
        if not (min_age <= user["age"] <= max_age):
            return 0
    
    if "resident_state" in elig:
        if user["state"].strip().lower() != elig["resident_state"].strip().lower():
            return 0
    else:
        score += 1

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

    for key in ["priority_groups", "joint_borrower_applicants", "credit_limit", "components", "implementation"]:
        if elig.get(key):
            score += 1

    return score

print("\nHello! I am SchemeBot. I can help you find government schemes.")
print("Type 'exit' anytime to quit.\n")

def get_input(prompt, cast_type=str, optional=False, default=None):
    while True:
        val = input(f"\nSchemeBot: {prompt}\nYou:\n").strip()
        if val.lower() == "exit":
            print("\nSchemeBot: Goodbye! Stay safe and good luck!\n")
            sys.exit(0)
        if optional and val == "":
            return default
        try:
            return cast_type(val) if val else default
        except ValueError:
            print("SchemeBot: Invalid input, please try again.")

# --- Conversation before scheme mode ---
def chat_mode():
    print("\nSchemeBot: We can chat normally. Say 'schemes' whenever you want me to suggest government schemes.")
    while True:
        user_input = input("You:\n").strip().lower()
        if user_input == "exit":
            print("\nSchemeBot: Goodbye! Stay safe and good luck!\n")
            sys.exit(0)
        elif user_input == "schemes":
            print("\nSchemeBot: Great! Let's start finding suitable government schemes for you.\n")
            break
        elif user_input in ["hi", "hello", "hey"]:
            print("SchemeBot: Hello! How are you today?")
        elif "how are you" in user_input:
            print("SchemeBot: I'm just a bot, but I'm ready to chat or help you find schemes!")
        elif user_input in ["thanks", "thank you"]:
            print("SchemeBot: You're welcome! You can type 'schemes' anytime to check for government schemes.")
        else:
            print("SchemeBot: I see! You can keep chatting or type 'schemes' to get government schemes.")

# --- Scheme mode ---
def scheme_mode(user_data):
    while True:
        # Ask user if they want to update any field or keep previous
        print("\nSchemeBot: Let's enter your details. Press Enter to keep previous value (if any).")

        user_data["category"] = get_input(
            "Enter your category (Farmer / Construction Worker):",
            str, optional=True, default=user_data.get("category")
        )
        user_data["occupation"] = get_input(
            "Enter your occupation:",
            str, optional=True, default=user_data.get("occupation")
        )
        user_data["age"] = get_input(
            "Enter your age:",
            int, optional=True, default=user_data.get("age")
        )
        user_data["state"] = get_input(
            "Enter your state of residence:",
            str, optional=True, default=user_data.get("state")
        )
        user_data["land_owned_hectares"] = get_input(
            "Land owned in hectares (optional):",
            float, optional=True, default=user_data.get("land_owned_hectares")
        )
        crop_input = get_input(
            "Crops grown (comma separated, optional):",
            str, optional=True,
            default=",".join(user_data.get("crop_type", [])) if user_data.get("crop_type") else ""
        )
        user_data["crop_type"] = [c.strip().lower() for c in crop_input.split(",")] if crop_input else None
        user_data["worked_days_last_year"] = get_input(
            "Worked days last year (optional):",
            int, optional=True, default=user_data.get("worked_days_last_year")
        )
        reg_board = get_input(
            "Registered with board? (yes/no, optional):",
            str, optional=True,
            default=("yes" if user_data.get("registered_with_board") else "no") if "registered_with_board" in user_data else None
        )
        if reg_board:
            if reg_board.lower() == "yes":
                user_data["registered_with_board"] = True
            elif reg_board.lower() == "no":
                user_data["registered_with_board"] = False
            else:
                user_data["registered_with_board"] = None
        else:
            user_data["registered_with_board"] = None

        # Compute schemes
        scored_schemes = [(scheme, match_scheme(user_data, scheme)) for scheme in schemes]
        scored_schemes.sort(key=lambda x: x[1], reverse=True)

        # Display top schemes
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

        # Ask whether to continue or exit
        while True:
            cont = input("SchemeBot: Do you want to update info or exit? (type 'yes' to continue, 'exit' to quit)\nYou:\n").strip().lower()
            if cont == "exit":
                print("\nSchemeBot: Goodbye! Stay safe and good luck!\n")
                sys.exit(0)
            elif cont == "yes":
                break  # Continue scheme loop
            else:
                print("SchemeBot: Please type 'yes' to continue or 'exit' to quit.")

# --- Run bot ---
user_data = {}
chat_mode()         # first normal conversation
scheme_mode(user_data)  # then scheme-finding
