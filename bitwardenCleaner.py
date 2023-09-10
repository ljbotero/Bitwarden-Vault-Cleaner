import json
import os
import ping3
from urllib.parse import urlparse, urlsplit, urlunsplit  # Import the urlparse, urlsplit, and urlunsplit functions


# Constants for file names
input_file_name = "bitwarden_export_file.json" # Replace this with your export file from Bitwarden
output_file_name = f"{input_file_name.replace('.json', '_output.json')}"
deleted_file_name = f"{input_file_name.replace('.json', '_deleted.json')}"

# Load data from the input file
with open(input_file_name, 'r') as input_file:
    data = json.load(input_file)

# Initialize variables
processed_items = 0
total_items = len(data['items'])
duplicates = {}  # Change this line to initialize duplicates as a dictionary
deleted_items = []
updated_items = []

# Function to check if a URL is reachable using ping
def is_url_reachable(url):
    try:
        # Ping the URL, wait for a response for 5 seconds
        response_time = ping3.ping(url, timeout=5)
        return response_time is not None

    except Exception as e:
        print(f"Error while pinging URL: {url}, Error: {e}")
        return False

# Function to check if a URL is valid
def is_valid_url(url):
    try:
        # Use urlsplit to parse the URL
        parts = urlsplit(url)

        # Check if the scheme and netloc (host) are not empty
        if parts.scheme and parts.netloc:
            return True
        else:
            return False

    except Exception as e:
        print(f"Error while checking URL validity: {url}, Error: {e}")
        return False

# Function to remove query parameters from a URL
def remove_query_parameters(url):
    try:
        parts = urlsplit(url)
        scheme, netloc, path, _, _ = parts
        clean_url = urlunsplit((scheme, netloc, path, '', ''))
        return clean_url
    except Exception as e:
        print(f"Error removing query parameters from URL: {url}, Error: {e}")
        return url

# ... (other parts of the script)

# Iterate through the items and update URIs
for item in data['items']:
    item_name = item['name']
    print(f"Processing item ({processed_items}/{total_items}): {item_name}")

    # Check if the item has a "login" field
    if 'login' not in item or not isinstance(item['login'], dict):
        print(f"Skipping item: {item_name} as it does not have a 'login' field")
        processed_items += 1
        continue

    uris = item['login']['uris']
    username = item['login']['username']
    password = item['login']['password']

    # Ensure uris, username, and password are not None
    if uris is None or username is None or password is None:
        print(f"Skipping item: {item_name} as it has missing data")
        processed_items += 1
        continue

    # Handle non-standard URIs separately
    standard_uris = []
    non_standard_uris = []

    for uri_data in uris:
        uri = uri_data['uri']

        # Remove query parameters from the URL
        clean_uri = remove_query_parameters(uri)

        if not is_valid_url(clean_uri):
            print(f"Skipping invalid URL for item: {item_name}, URI: {clean_uri}")
            non_standard_uris.append(uri_data)
            continue

        # Check if the URI is "https://" or "http://"
        if clean_uri in ["https://", "http://"]:
            # If there's only one URI and it's "https://" or "http://", keep it
            if len(uris) == 1:
                standard_uris.append(uri_data)
        else:
            standard_uris.append({"uri": clean_uri})  # Add the URI to standard_uris

    # If all URIs are "http://" or "https://", skip this item
    if not standard_uris and not non_standard_uris:
        print(f"Skipping item: {item_name} as all URIs are 'http://' or 'https://'")
        processed_items += 1
        continue

    item['login']['uris'] = standard_uris

    # Construct item_key based on standard URIs only
    item_key = f"{username}_{password}_{','.join(sorted(uri_data['uri'] for uri_data in standard_uris))}"

    if item_key in duplicates:
        reason_for_deletion = f"Duplicate of {duplicates[item_key]}"
        deleted_items.append({**item, "reasonForDeletion": reason_for_deletion})
        print(f"Removing item: {item_name} as it's a duplicate of {duplicates[item_key]}")
    else:
        duplicates[item_key] = item_name

        # Check if any standard URI is reachable and not "https://" or "http://"
        uris_valid = any(
            is_url_reachable(uri_data['uri']) and not (uri_data['uri'] in ["https://", "http://"])
            for uri_data in standard_uris
        )

        if uris_valid or not standard_uris:
            updated_items.append(item)
        else:
            reason_for_deletion = "All standard URIs are invalid"
            deleted_items.append({**item, "reasonForDeletion": reason_for_deletion})
            print(f"Removing item: {item_name} because all standard URIs are invalid")

    # Append non-standard URIs back to the item
    item['login']['uris'] += non_standard_uris

    # Save the data and deleted items in real-time
    with open(output_file_name, 'w') as output_file:
        json.dump(data, output_file, indent=2)

    with open(deleted_file_name, 'w') as deleted_file:
        json.dump(deleted_items, deleted_file, indent=2)

    processed_items += 1

# Save the final data with updated and deleted items
with open(output_file_name, 'w') as output_file:
    json.dump(data, output_file, indent=2)

print(f"Processed {processed_items} items out of {total_items}.")
print(f"Updated items: {len(updated_items)}, Deleted items: {len(deleted_items)}")
