import wikipedia
from wikipedia.exceptions import DisambiguationError, PageError
import warnings
from bs4 import GuessedAtParserWarning

# Suppress BeautifulSoup warnings
warnings.filterwarnings("ignore", category=GuessedAtParserWarning)


def wiki_search():
    print("Welcome to the Wikipedia search tool!")
    while True:
        # Get input from the user
        search_query = input("Enter page title: ").strip()

        # Exit on blank input
        if not search_query:
            print("Thank you.")
            break

        try:
            # Retrieve the Wikipedia page
            result_page = wikipedia.page(search_query)
            print(f"\n{result_page.title}")
            print(wikipedia.summary(search_query, sentences=2))
            print(result_page.url)

        except DisambiguationError as options_error:
            # Handle disambiguation and suggest options
            print("We need a more specific title. Try one of the following, or a new search:")
            print(options_error.options)

        except PageError:
            # Handle case where page does not exist
            print(f'Page "{search_query}" does not match any pages. Try another id!')

        except Exception as unknown_error:
            # Catch unexpected errors
            print(f"An unexpected error occurred: {unknown_error}")


if __name__ == "__main__":
    wiki_search()
