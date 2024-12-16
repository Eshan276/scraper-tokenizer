import re
import string
import json
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Function to clean and preprocess the text


def preprocess(text):
    text = text.lower()  # Lowercase
    # Remove punctuation
    text = ''.join([char for char in text if char not in string.punctuation])
    tokens = word_tokenize(text)  # Tokenization
    return ' '.join(tokens)  # Rejoin into a string

# Function to load the JSON files for nearby restaurants and the main restaurant


def load_json(file_path):
    with open(file_path, 'r') as f:
        return json.load(f)


# Load all nearby restaurant menus and the main restaurant menu
nearby_1 = load_json("Data/chennai-dosas-hicksville.json")  # Restaurant 1 JSON
nearby_2 = load_json("Data/dosaworld.json")  # Restaurant 2 JSON
# Restaurant 3 JSON
nearby_3 = load_json("Data/kathis-and-kababs-hicksville.json")
nearby_4 = load_json("Data/menu_data_jazzera.json")  # Restaurant 4 JSON
# Restaurant 5 JSON
nearby_5 = load_json("Data/taste-of-chennai-hicksville.json")
main_restaurant = load_json(
    "Data/menu_items_village.json")  # Main Restaurant JSON

# Function to extract dish descriptions from a restaurant's menu


def extract_descriptions(menu):
    descriptions = []
    # print(menu)
    for item in menu["menu"]:
        description = item.get("description", "")
        name = re.sub(r'^\d+\.\s*', '', item.get("name", ""))
        if description:
            descriptions.append(description)
        else:
            descriptions.append(name)
    return descriptions


def extract_descriptions_new(menu):
    descriptions = []
    # print(menu)
    for item in menu["menu"]:
        description = item.get("description", "")
        name = re.sub(r'^\d+\.\s*', '', item.get("name", ""))
        descriptions.append(name)
    return descriptions


def ex2(menu):
    descriptions = []
    prices = []
    for item in menu:
        # print(item)
        for i in item['items']:
            print(i)
            description = i.get("description", "")
            name = re.sub(r'^\d+\.\s*', '', i.get("name", ""))
            price = i.get("price")
            # print("name", name)
            descriptions.append(name)
            prices.append(price)
            # print("description", descriptions)
    # for item in menu["menu"]:
    #     description = item.get("description", "")
    #     name = re.sub(r'^\d+\.\s*', '', item.get("name", ""))
    #     if description:
    #         descriptions.append(description)
    #     else:
    #         descriptions.append(name)
    return descriptions, prices


# Extract descriptions from all the menus
descriptions_main = extract_descriptions_new(main_restaurant)
descriptions_nearby_1 = extract_descriptions(nearby_1)
descriptions_nearby_2 = extract_descriptions(nearby_2)
descriptions_nearby_3 = extract_descriptions(nearby_3)
print("descriptions_nearby_3")
descriptions_nearby_4, prices_nearby_4 = ex2(nearby_4)
print("descriptions_nearby_4", descriptions_nearby_4)
descriptions_nearby_5 = extract_descriptions(nearby_5)

# Combine all the descriptions into one list for vectorization
all_descriptions = (
    descriptions_main +
    descriptions_nearby_1 +
    descriptions_nearby_2 +
    descriptions_nearby_3 +
    descriptions_nearby_4 +
    descriptions_nearby_5
)

# Preprocess all descriptions
processed_descriptions = [preprocess(desc) for desc in all_descriptions]

# TF-IDF Vectorizer to convert text descriptions to vectors
vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform(processed_descriptions)

# Separate the descriptions into respective menus
tfidf_main = tfidf_matrix[:len(descriptions_main)]
tfidf_nearby_1 = tfidf_matrix[len(descriptions_main):len(
    descriptions_main)+len(descriptions_nearby_1)]
tfidf_nearby_2 = tfidf_matrix[len(descriptions_main)+len(descriptions_nearby_1):len(
    descriptions_main)+len(descriptions_nearby_1)+len(descriptions_nearby_2)]
tfidf_nearby_3 = tfidf_matrix[len(descriptions_main)+len(descriptions_nearby_1)+len(descriptions_nearby_2):len(
    descriptions_main)+len(descriptions_nearby_1)+len(descriptions_nearby_2)+len(descriptions_nearby_3)]
tfidf_nearby_4 = tfidf_matrix[len(descriptions_main)+len(descriptions_nearby_1)+len(descriptions_nearby_2)+len(descriptions_nearby_3):len(
    descriptions_main)+len(descriptions_nearby_1)+len(descriptions_nearby_2)+len(descriptions_nearby_3)+len(descriptions_nearby_4)]
tfidf_nearby_5 = tfidf_matrix[len(descriptions_main)+len(descriptions_nearby_1)+len(
    descriptions_nearby_2)+len(descriptions_nearby_3)+len(descriptions_nearby_4):]

# Compute cosine similarity between each dish in the main restaurant and each dish in the nearby restaurants


def compare_menus(tfidf_main, tfidf_nearby):
    similarities = cosine_similarity(tfidf_main, tfidf_nearby)
    return similarities


# Compare main restaurant with nearby restaurant 1-5
similarities_1 = compare_menus(tfidf_main, tfidf_nearby_1)
similarities_2 = compare_menus(tfidf_main, tfidf_nearby_2)
similarities_3 = compare_menus(tfidf_main, tfidf_nearby_3)
similarities_4 = compare_menus(tfidf_main, tfidf_nearby_4)
similarities_5 = compare_menus(tfidf_main, tfidf_nearby_5)

# Price data from all the menus


def extract_prices(menu):
    return [item.get("price") for item in menu["menu"]]


prices_main = extract_prices(main_restaurant)
print("prices_main", prices_main)
prices_nearby_1 = extract_prices(nearby_1)
prices_nearby_2 = extract_prices(nearby_2)
prices_nearby_3 = extract_prices(nearby_3)
# prices_nearby_4 = extract_prices(nearby_4)
prices_nearby_5 = extract_prices(nearby_5)

# Function to compare dishes and prices


# def compare_dishes_and_prices(similarity_matrix, descriptions_main, descriptions_nearby, prices_main, prices_nearby, restaurant_name):
#     for i, similarity_row in enumerate(similarity_matrix):
#         for j, similarity_score in enumerate(similarity_row):
#             if similarity_score > 0.7:  # Threshold for considering dishes similar
#                 print(
#                     f"Dish '{descriptions_main[i]}' from Main Restaurant is similar to '{descriptions_nearby[j]}' from {restaurant_name}.")
#                 print(
#                     f"Price Comparison: Main Restaurant ({prices_main[i]}), {restaurant_name} ({prices_nearby[j]})")
#                 print(f"Cosine Similarity: {similarity_score:.2f}\n")


# # Compare and print results for each nearby restaurant
# compare_dishes_and_prices(similarities_1, descriptions_main,
#                           descriptions_nearby_1, prices_main, prices_nearby_1, "Restaurant 1")
# compare_dishes_and_prices(similarities_2, descriptions_main,
#                           descriptions_nearby_2, prices_main, prices_nearby_2, "Restaurant 2")
# compare_dishes_and_prices(similarities_3, descriptions_main,
#                           descriptions_nearby_3, prices_main, prices_nearby_3, "Restaurant 3")
# compare_dishes_and_prices(similarities_4, descriptions_main,
#                           descriptions_nearby_4, prices_main, prices_nearby_4, "Restaurant 4")
# compare_dishes_and_prices(similarities_5, descriptions_main,
#                           descriptions_nearby_5, prices_main, prices_nearby_5, "Restaurant 5")

def compare_dishes_and_prices(similarity_matrix, descriptions_main, descriptions_nearby, prices_main, prices_nearby, restaurant_name):
    results = []
    unmatched = []  # To store unmatched dishes

    for i, similarity_row in enumerate(similarity_matrix):
        max_similarity_score = 0  # Track the highest similarity score for the current main dish
        best_match = None  # Track the best match details
        lowest_price = float('inf')  # Initialize to a very high value

        for j, similarity_score in enumerate(similarity_row):
            if similarity_score > max_similarity_score and similarity_score > 0.7:  # Ensure similarity > 0.7
                max_similarity_score = similarity_score
                # Compare prices, update if the current match has a better price
                current_price = prices_nearby[j]
                # current_price = float(current_price) if current_price else 0
                if str(current_price)[0] == "$":  # Skip if price is missing
                    current_price = float(current_price[1:])
                    # current_price = float(2.99)
                print("current_price", current_price)
                if current_price < lowest_price:
                    lowest_price = current_price
                    best_match = {
                        "main_dish": descriptions_main[i],
                        "nearby_dish": descriptions_nearby[j],
                        "main_price": prices_main[i],
                        "nearby_price": current_price,
                        "similarity_score": similarity_score,
                        "restaurant_name": restaurant_name
                    }

        if best_match:  # Add the best match for the current main dish
            results.append(best_match)
        else:  # No match found above the threshold
            unmatched.append({
                "main_dish": descriptions_main[i],
                "main_price": prices_main[i],
                "restaurant_name": restaurant_name,
                "reason": "No match above similarity threshold"
            })

    return results, unmatched


# Collect results and unmatched dishes for each nearby restaurant
all_results = []
all_unmatched = []

results_1, unmatched_1 = compare_dishes_and_prices(similarities_1, descriptions_main,
                                                   descriptions_nearby_1, prices_main, prices_nearby_1, "Restaurant 1")
all_results.extend(results_1)
all_unmatched.extend(unmatched_1)

results_2, unmatched_2 = compare_dishes_and_prices(similarities_2, descriptions_main,
                                                   descriptions_nearby_2, prices_main, prices_nearby_2, "Restaurant 2")
all_results.extend(results_2)
all_unmatched.extend(unmatched_2)

results_3, unmatched_3 = compare_dishes_and_prices(similarities_3, descriptions_main,
                                                   descriptions_nearby_3, prices_main, prices_nearby_3, "Restaurant 3")
all_results.extend(results_3)
all_unmatched.extend(unmatched_3)

results_4, unmatched_4 = compare_dishes_and_prices(similarities_4, descriptions_main,
                                                   descriptions_nearby_4, prices_main, prices_nearby_4, "Restaurant 4")
all_results.extend(results_4)
all_unmatched.extend(unmatched_4)

results_5, unmatched_5 = compare_dishes_and_prices(similarities_5, descriptions_main,
                                                   descriptions_nearby_5, prices_main, prices_nearby_5, "Restaurant 5")
all_results.extend(results_5)
all_unmatched.extend(unmatched_5)

# Prepare final output
final_output = {
    "matched_dishes": all_results,
    "unmatched_dishes": all_unmatched
}
print("length" , len(all_unmatched))
# Save results to a JSON file
with open('comparison_results_with_missing.json', 'w') as json_file:
    json.dump(final_output, json_file, indent=4)