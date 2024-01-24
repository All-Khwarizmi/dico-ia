import csv
import os
import datetime

# File paths
system_prompts_file = 'system_prompts.csv'
interactions_file = 'interactions.csv'

# Initialize files with headers
def init_files():
    if not os.path.exists(system_prompts_file):
        with open(system_prompts_file, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['PromptID', 'SystemPrompt'])

    if not os.path.exists(interactions_file):
        with open(interactions_file, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['UserPrompt', 'SystemPromptID', 'PromptName', 'LLMResponse', 'ModelName', 'Date', 'Quality', 'Comments', 'UserFeedback', ])

# Function to add a new system prompt
def add_system_prompt(prompt):
    prompt_id = 1
    prompts = {}

    if os.path.exists(system_prompts_file):
        with open(system_prompts_file, 'r', newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                prompts[row['SystemPrompt']] = row['PromptID']
                prompt_id = max(prompt_id, int(row['PromptID']) + 1)
        print("Added system prompt with ID:", prompt_id)
            

    if prompt not in prompts:
        with open(system_prompts_file, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([prompt_id, prompt])
        prompts[prompt] = prompt_id
        print("Added system prompt:", prompt)

    return prompts[prompt]

# Function to get the ID of a system prompt
def get_system_prompt_id(prompt):
    with open(system_prompts_file, 'r', newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['SystemPrompt'] == prompt:
                return row['PromptID']
    return None

# Function to log an interaction with LLM
def add_llm_call_row(system_prompt_id,prompt_name, user_prompt, llm_response, model_name, quality=None, comments=None, user_feedback=None):
    date_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(interactions_file, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([user_prompt, system_prompt_id,prompt_name, llm_response, model_name, date_time, quality, comments, user_feedback, ])


# Function to update quality and comments for the last row
def update_last_row_quality_comments(quality, comments):
    if not os.path.exists(interactions_file):
        print("Interactions file does not exist.")
        return

    with open(interactions_file, 'r', newline='') as file:
        reader = csv.reader(file)
        rows = list(reader)

    if len(rows) > 1:  # Check if there's more than just the header
        rows[-1][5] = quality   # Update quality
        rows[-1][6] = comments  # Update comments

        with open(interactions_file, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(rows)
    else:
        print("No interaction data to update.")