import csv

# Open the input .txt file
with open('library.txt', 'r') as file:
    lines = file.readlines()

# Create a list to store the book data
books = []

# Iterate through the lines and extract the book data
i = 0
while i < len(lines):
    if lines[i].startswith('Book title: '):
        title = lines[i].strip().replace('Book title: ', '')
        i += 1
    else:
        i += 1
        continue
    
    if i < len(lines) and lines[i].startswith('Book Author: '):
        author = lines[i].strip().replace('Book Author: ', '')
        i += 1
    else:
        author = ''
        i += 1
    
    if i < len(lines) and lines[i].startswith('Book Description: '):
        description = lines[i].strip().replace('Book Description: ', '')
        i += 1
    else:
        description = ''
        i += 1
    
    books.append([title, author, description])

# Open the output .csv file
with open('library.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    
    # Write the header row
    writer.writerow(['Book title', 'Book Author', 'Book Description'])
    
    # Write the book data rows
    writer.writerows(books)