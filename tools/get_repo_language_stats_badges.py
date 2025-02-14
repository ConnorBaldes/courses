import requests
import argparse
import json

# Function to get the language stats
def get_language_stats(username, repo, file_extension=None):
    url = f"https://api.github.com/repos/{username}/{repo}/languages"
    
    response = requests.get(url)
    if response.status_code == 200:
        languages = response.json()

        # If a file extension is specified, filter the languages
        if file_extension:
            filtered_languages = {}
            for lang, bytes in languages.items():
                # This assumes you want to only include files with the specified extension
                # If you have more specific filtering criteria, you can modify this section
                if lang.lower().endswith(file_extension.lower()):
                    filtered_languages[lang] = bytes
            languages = filtered_languages

        total = sum(languages.values())

        # Sorting languages by usage
        sorted_languages = sorted(languages.items(), key=lambda x: x[1], reverse=True)

        # Generate Markdown for the language stats with badges
        markdown = "### Language Stats\n\n"
        for language, bytes in sorted_languages:
            percentage = (bytes / total) * 100
            # Ensure the percentage is rounded to two decimal places
            percentage = round(percentage, 2)
            
            # Generate badge URL based on percentage
            badge_url = f"https://img.shields.io/badge/{language}-{percentage}%25-"
            
            # Assign color based on percentage
            if percentage >= 90:
                badge_url += "brightgreen"
            elif percentage >= 60:
                badge_url += "yellowgreen"
            elif percentage >= 30:
                badge_url += "yellow"
            elif percentage >= 10:
                badge_url += "orange"
            else:
                badge_url += "lightgray"

            # Add the badge to the markdown
            markdown += f"![{language} Language Stats]({badge_url})\n"
        
        # Output the markdown
        print(markdown)
    else:
        print("Failed to retrieve language data")

# Command-line interface
def main():
    parser = argparse.ArgumentParser(description="Fetch GitHub repository language stats.")
    parser.add_argument('username', help="GitHub username")
    parser.add_argument('repo', help="GitHub repository name")
    parser.add_argument('--file-type', '-f', help="Filter by file extension (e.g., .js, .py)")

    args = parser.parse_args()

    get_language_stats(args.username, args.repo, args.file_type)

if __name__ == "__main__":
    main()
