import requests

# github api link
base_url = "https://api.github.com"

# function to connect and retrieve info
def get_github_info(name):
    url = f"{base_url}/users/{name}/events"
    all_events = []

    while url:
        response = requests.get(url)

          # Check if the request was successful
        if response.status_code == 200:
            events = response.json() # Parse the JSON response

            all_events.extend(events)

            if 'Link' in response.headers:
                links = response.headers['Link']

                next_url = None
                for link in links.split(','):
                    if 'rel="next"' in link:
                        next_url = link.split(',')[0][1:-1]
                        break
                
                url = next_url

            else:
                url = None

        else:
            print(f"Error: {response.status_code}")    
            return None

    return all_events

# Enter github username here
github_user = "<username>"  
user_info = get_github_info(github_user)

if user_info:
    # Print out the  events 
    if len(user_info) > 0:
        print(f"Recent event details: {len(user_info)} events for user '{github_user}':/n")
        for event in user_info:
            event_type = event.get("type", "Unknown Event")
            repo_name = event.get("repo", {}).get("name", "Unknown Repo")
            created_at = event.get("created_at", "Unknown Date")
            print(f"{created_at}: {event_type} in {repo_name}")
    else:
        print("No events found for this user.")
else:
    print("User not found")
