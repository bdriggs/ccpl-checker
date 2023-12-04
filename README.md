# CCPL-Checker

![ccpl-checker](https://github.com/bdriggs/ccpl-checker/assets/65035792/465684b6-06f9-41d3-82fd-3aa8bbb2e212)

A small Python application that checks for available PlayStation 5 games at the Cuyahoga County public library.

## How to Use

1. Clone the repository locally
2. Install required modules: `pip install -r requirements.txt`
3. Run the application: `python main.py`

## File Structure

- The main logic for this application is contained within `./utilities/ccpl.py`
- The application outputs all files to the `./files/` directory, which includes the search results for the query run against the library's catalog (in CSV), the list of available PlayStation 5 games, and any new games that have been added since the previous run of the application (both housed within lists containing JSON).
