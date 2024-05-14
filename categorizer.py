import csv
from openai import OpenAI

# Set up your OpenAI API key
client = OpenAI(api_key='ADD_OPENAI_API_KEY') # Replace with your actual API key

# Function to generate LCSH using GPT-4o
def generate_lcsh(book_title, book_author, book_description):
    prompt = f"Generate Library of Congress Subject Headings (LCSH) for the following book:\n\nTitle: {book_title}\nAuthor: {book_author}\nDescription: {book_description}. Please include one lcsh per line, without numbering or bulleting the list. Your output is being added directly onto a sticker, so only categories, no commentary!"
    
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
    )

    lcsh = response.choices[0].message.content.strip()
    return lcsh

# Open the CSV file for reading and writing
with open('library.csv', 'r+', newline='', encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile)
    rows = list(reader)

    # Add a new header for the LCSH column if it doesn't exist
    if "LCSH" not in rows[0]:
        rows[0].append("LCSH")

    # Generate LCSH for each book and update the corresponding row
    for i in range(1, len(rows)):
        row = rows[i]
        book_title, book_author, book_description = row[:3]  # Assuming the first three columns are title, author, and description
        
        if len(row) < 4:  # If LCSH column doesn't exist for this row
            lcsh = generate_lcsh(book_title, book_author, book_description)
            row.append(lcsh)
            rows[i] = row
            
            # Write the updated row back to the CSV file
            csvfile.seek(0)
            writer = csv.writer(csvfile)
            writer.writerows(rows)
            csvfile.flush()  # Ensure the changes are written to the file immediately
        
    print("CSV file has been updated with LCSH.")