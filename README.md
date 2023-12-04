# CCPL-Checker
![ccpl-checker](https://github.com/bdriggs/ccpl-checker/assets/65035792/2c890e84-8889-4ef0-9e5e-2b3f3583c0b9)

A small Python application that checks for available PlayStation 5 games at the Cuyahoga County public library.

## How to Use

1. Clone the repoository locally
2. Install required modules: `pip install -r requirements.txt`
3. Run the application: `python main.py`

## File Structure

- The main logic for this application is contained within `./utilities/ccpl.py`
- The application outputs all files to the `./files` directory, which includes the search results for the query run against the library's catalog (in CSV), the list of available PlayStation 5 games, and any new games that have been added since the previous run of the application (both housed within lists containing JSON).
