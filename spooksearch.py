import requests
import json
import argparse

# Function to print the help menu
def print_help():
    help_text = """
    Usage:
        spooksearch.py -e EMAIL -k API_KEY -f FILE_PATH

    Arguments:
        -e, --email       Your email for API authentication
        -k, --api_key     Your Dehashed API Key
        -f, --file        Path to the text file containing a list of emails/usernames to query

    Example:
        python spooksearch.py -e youremail@example.com -k yourapikey -f queries.txt
    """
    print(help_text)

# Function to validate the email
def is_valid_email(email):
    return '@' in email and '.' in email

# Function to validate the API key (assuming it should be alphanumeric)
def is_valid_api_key(api_key):
    return api_key.isalnum()

# Main function
def main():
    # Argument parser for command-line arguments
    parser = argparse.ArgumentParser(description="Dehashed API Client - SpookSearch")
    parser.add_argument("-e", "--email", required=True, type=str, help="Your email for API authentication")
    parser.add_argument("-k", "--api_key", required=True, type=str, help="Your Dehashed API key")
    parser.add_argument("-f", "--file", required=True, type=str, help="Path to the text file containing the emails or usernames")
    args = parser.parse_args()

    email = args.email
    api_key = args.api_key
    file_path = args.file

    # Validate email and API key format
    if not is_valid_email(email):
        print("Invalid email format. Exiting.")
        return

    if not is_valid_api_key(api_key):
        print("Invalid API key format. Exiting.")
        return

    try:
        # Read the list of queries from the file
        with open(file_path, 'r') as file:
            queries = [line.strip() for line in file if line.strip()]  # Remove empty lines and whitespace

        # Send the HTTP request for each query
        for query in queries:
            print(f"\nQuerying for: {query}")
            url = f"https://api.dehashed.com/search?query=username={query}"
            headers = {
                "Accept": "application/json"
            }

            # Use the email and API key for basic authentication
            try:
                response = requests.get(url, headers=headers, auth=(email, api_key))

                if response.status_code == 200:
                    # Parse and format the JSON response
                    json_data = response.json()
                    print(json.dumps(json_data, indent=4))  # Pretty print the JSON data
                else:
                    print(f"Error: {response.status_code} - {response.reason}")

            except requests.exceptions.RequestException as e:
                print(f"An error occurred: {str(e)}")

    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
    except Exception as e:
        print(f"Unexpected error: {str(e)}")

if __name__ == "__main__":
    main()
