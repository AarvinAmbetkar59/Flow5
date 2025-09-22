import json

# Load JSON
with open("schemefinderdataset.json", "r", encoding="utf-8") as f:
    schemes = json.load(f)

# --- Matching function ---
def match_scheme(user, scheme):
    """Return a score (0-1) how well the user matches a scheme."""
    eligibility = scheme.get("eligibility", {})
    score = 0
    total = 2  # we are using occupation and age as minimal info

    # Occupation
    if user["occupation"].lower() in [o.lower() for o in eligibility.get("occupation", [])]:
        score += 1

    # Age
    age_criteria = eligibility.get("age", {})
    min_age = age_criteria.get("min", 0)
    max_age = age_criteria.get("max", 1000)
    if min_age <= user["age"] <= max_age:
        score += 1

    return score / total  # 0 to 1

# --- Example user input ---
user_input = {
    "occupation": "farmer",
    "age": 25,
    # land, crop, state optional
}

# Compute match scores
scheme_scores = []
for scheme in schemes:
    score = match_scheme(user_input, scheme)
    if score > 0:  # only consider partially matching schemes
        scheme_scores.append((scheme["scheme_id"], scheme["name"], score, scheme.get("benefits","")))

# Sort by score descending
scheme_scores.sort(key=lambda x: x[2], reverse=True)

# Display top schemes
print("Predicted schemes (most likely first):\n")
for s_id, s_name, score, benefits in scheme_scores[:10]:
    print(f"{s_id} - {s_name} (score: {score:.2f})")
    print(f"Benefits: {benefits}\n")
