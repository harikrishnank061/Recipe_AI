import streamlit as st
import cohere
import time

# Function to generate a complete cooking recipe using Cohere Generate API
def generate_recipe(api_key, ingredients, time_available, dietary_preference):
    try:
        # Initialize the Cohere client with the provided API key
        co = cohere.Client(api_key)
        
        # Create a detailed prompt for a complete recipe
        prompt = (
            f"Generate a complete cooking recipe based on the following details:\n"
            f"Ingredients: {ingredients}\n"
            f"Time available: {time_available} minutes\n"
            f"Dietary preference: {dietary_preference}\n"
            "\nInclude the following sections:\n"
            "1. Recipe Name\n"
            "2. Short Description\n"
            "3. Ingredients List\n"
            "4. Step-by-Step Instructions\n"
            "5. Serving Suggestions\n"
        )
        
        # Call the generate method for more detailed text responses
        response = co.generate(
            model="command-xlarge",  
            prompt=prompt,
            max_tokens=1500,  # Increased tokens for full recipes
            temperature=0.7,  # Balanced creativity
            k=0,  # Use all possible completions for more variety
            p=0.8,
            stop_sequences=["\n\n"],
            frequency_penalty=0.2,
            presence_penalty=0.2
        )
        
        # Extract the generated text
        recipe_text = response.generations[0].text.strip()
        
        # Ensure the response contains all required sections
        required_sections = ["Ingredients List", "Step-by-Step Instructions", "Serving Suggestions"]
        for section in required_sections:
            if section not in recipe_text:
                return "⚠️ The generated recipe is missing some sections. Please try again."
        
        return recipe_text
    except Exception as e:
        # Handle errors and display error messages in the Streamlit app
        st.error(f"Error: {str(e)}")
        return None

# Streamlit app layout
st.set_page_config(page_title="Cooking Recipe Generator", page_icon="🥘")
st.title("🥘 Cooking Recipe Generator")
st.markdown("Generate complete cooking recipes based on your available ingredients, time, and dietary preferences.")

# Input API key directly in the app
api_key = st.text_input("Enter your Cohere API Key", type="password")

# Show a warning if the API key is not provided
if not api_key:
    st.warning("⚠️ Please enter your Cohere API key to proceed.")

# Input fields for recipe generation
ingredients = st.text_area("Enter the ingredients you have (comma-separated)", height=150)
time_available = st.number_input("Available Cooking Time (in minutes)", min_value=1, max_value=240, value=30)
dietary_preference = st.selectbox("Dietary Preference", ["No Preference", "Vegetarian", "Vegan", "Gluten-Free", "Low Carb", "Keto", "High Protein"], index=0)

# Button to trigger recipe generation
if st.button("Generate Recipe"):
    if api_key and ingredients.strip():
        # Add a loading spinner while generating the recipe
        with st.spinner("Generating recipe... Please wait."):
            start_time = time.time()
            recipe = generate_recipe(api_key, ingredients, time_available, dietary_preference)
            end_time = time.time()
            if recipe:
                st.subheader("Generated Recipe:")
                st.write(recipe)
            st.write(f"Recipe generated in {end_time - start_time:.2f} seconds.")
    else:
        st.warning("⚠️ Please provide both the API key and the ingredients to generate a recipe.")

st.markdown("---")
st.caption("Powered by Cohere | Built with ❤️ using Streamlit")
