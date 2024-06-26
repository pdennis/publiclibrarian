# Bookshelf to card catalogue

It's a tool for taking pictures of books, either the covers or spines on a bookshelf, and turning those pictures into a nice little organized CSV file of your books.

This was never intended to be public, and as of so, needless to say, it's provided without warranty. 

Try to clean up the pictures, rotate the image so the book spines are horizontal and easily readable, and not too many books in frame at a time. 

This script is designed to process pictures of bookshelves, extracting information from book spines or covers, and using it to create a card catalogue. It utilizes the OpenAI API to convert images containing book covers or spines into text descriptions. The text descriptions are then stored in a text file. It'll loop through as many images as you add to the pictures folder, and append all of the results to library.txt

![a screenshot of the tool in use](./example.png)

## Prerequisites

- Python 3.x installed on your system.
- An active OpenAI API key. You can obtain one from the OpenAI website.

## Installation

1. Clone the repository or download the script.
2. Install the required Python packages using pip:

    ```
    pip install requests
    ```

## Usage

1. **API Key Setup**:
   
    Replace the `api_key` variable in the script with your actual OpenAI API key.

2. **Starting a Virtual Environment**:
   
    If you want to isolate dependencies, you can create and activate a virtual environment. Navigate to the directory containing the script in your terminal and execute the following commands:

    ```
    python3 -m venv venv
    source venv/bin/activate
    ```

3. **Running the Script**:
   
    Place the images you want to process in the  `pictures` directory.  

    Arrange the pictures so the book titles are as easy to read as possible. They can be just the spines, or the covers. Works a little better when text is horizonal. Covers will be more reliable. Try not to do more than 10 in a single picture. Robot get confused.ß

    Then, run the script using:

    ```
    python script.py
    ```

4. **Output**:
   
    The script will process each image in the `pictures` directory, extract text descriptions using the OpenAI API, and append the results to a file named `library.txt` in the same directory.

## Convert the output to CSV

The script will output a semi-structured text file. For boring reasons, it's easier to have GPT4 output this text consistently than it is trying to get it to output raw .csv formatted text without extranious commentary. 

As a result, we need an extra script to convert the output to structured data. That's what csvconverter.py does.

run
```
python3 csvconverter.py
```
and it will create a new file called library.csv, and you're good to go.

### LCSH Generation Script

This script extends your existing `library.csv` script by adding Library of Congress Subject Headings (LCSH) to each book entry using GPT-4o.

#### Setup

1. **Install Dependencies**
   ```sh
   pip install openai
   ```

2. **Add Your OpenAI API Key**
   Replace `'ADD_OPENAI_API_KEY'` with your actual OpenAI API key in the script.

#### Usage

1. **Run the Script**
   Execute the script in your Python environment. It will read `library.csv`, generate LCSH for each book entry, and update the CSV file with the new LCSH column.

2. **Review the Updates**
   Open `library.csv` to verify that the LCSH have been correctly added to each book entry.

This script automates the categorization of your book collection, enhancing the organization and searchability of your library data.

## Dynix interface

![a screenshot of the tool in use](./Dynix.png)


This is a silly little project to clone old Dynix terminal interfaces. Run using 

```
python3 interface.py
```

And follow the instructions. 

It will read directly from library.csv (NOT library.txt, so you must run the csvconverter script for it to work)

## Notes

- Ensure that the images you want to process are in either PNG, JPG, or JPEG format.
- Try to have the spines of the book oriented horizontally, to make it easier for GPT4 to read. Also, GPT4 can't process full rez pictures, so you'll have problems if you try to process too many books at once. I try to limit to 10-15 books per image tops.
- The extracted text descriptions will be added to `library.txt` with a header indicating  each image the analysis came from.
- The results will not be perfect

