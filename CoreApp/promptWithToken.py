import json
import subprocess
import requests

prompt = """
As a mobile security expert, please perform a comprehensive security analysis of the provided Android/iOS app code. Your analysis should focus on identifying potential security vulnerabilities, related to the following categories:

Categories:

* Insecure Data Storage: Look for sensitive data (e.g., personal information, authentication tokens) stored without proper encryption or protection mechanisms.
* Improper Input Validation: Check for inputs that are not properly sanitized, which could lead to injection attacks or crashes.
* Insecure Network Communication: Identify any use of non-secure protocols (e.g., HTTP instead of HTTPS) or weak SSL/TLS configurations.
* Hardcoded Secrets: Search for embedded API keys, passwords, or other sensitive information hardcoded into the app.
* Authentication and Authorization Flaws: Examine the authentication mechanisms for weaknesses and ensure proper authorization checks are in place.
* Use of Deprecated or Vulnerable APIs: Spot any reliance on outdated libraries or APIs known to have security issues.
* Insufficient Error Handling: Look for exceptions or errors that are not properly handled, potentially revealing stack traces or sensitive information.
* Weak Cryptography: Identify the use of weak encryption algorithms or improper cryptographic implementations.
* Permission Misconfigurations: Review the app's permissions to ensure they are necessary and not overly broad.

Instructions:

1. Identify and Describe Issues: For each security vulnerability found, provide a clear and concise description, including the affected code snippets or sections.
2. Assess Impact: Explain the potential risks and impact associated with each vulnerability.
3. Recommend Solutions: Offer practical recommendations or code fixes to address the identified issues.
4. Prioritize Findings: Rank the vulnerabilities based on their severity (e.g., critical, high, medium, low).

Output Format:

* Title: Brief title of the vulnerability.
* Description: Detailed explanation of the issue.
* Location: File names and line numbers where the issue is found.
* Impact: Potential consequences if the vulnerability is exploited.
* Recommendation: Steps or code changes required to fix the issue.
* Severity Level: Critical, High, Medium, or Low.


Output Format:

Please provide your findings in a markdown table with the following structure (wrapped in triple apostrophes):

'''
| 🏷️ Title | 📝 Description | 📍 Location | 💥 Impact | 🛠️ Recommendation | ⚠️ Severity Level |
|----------|---------------|------------|-----------|-------------------|-------------------|
| Brief title of the vulnerability | Detailed explanation of the issue. | File names and line numbers where the issue is found. | Potential consequences if the vulnerability is exploited. | Steps or code changes required to fix the issue. | 🚨 Critical/🔴 High/🟠 Medium/🟡 Low |
| Next vulnerability title | Detailed explanation of the next issue. | File names and line numbers where the next issue is found. | Potential consequences if the next vulnerability is exploited. | Steps or code changes required to fix the next issue. | 🚨 Critical/🔴 High/🟠 Medium/🟡 Low |
'''

Issues Found Example (wrapped in triple apostrophes):

'''
| 🏷️ Title | 📝 Description | 📍 Location | 💥 Impact | 🛠️ Recommendation | ⚠️ Severity Level |
|----------|---------------|------------|-----------|-------------------|-------------------|
| SQL Injection in Login Form | The login form is vulnerable to SQL injection attacks due to unsanitized user input being directly concatenated into SQL queries. | auth.php, lines 45-52 | An attacker could bypass authentication, extract sensitive data from the database, or potentially gain full control of the database. | Use prepared statements or parameterized queries instead of string concatenation. Implement input validation and sanitization. | 🚨 Critical
'''

No Issues Found Example (wrapped in triple apostrophes):

'''
✅ No Security Issues Were Found!
'''

Use this framework to conduct a thorough security review of the app code, ensuring all potential vulnerabilities are identified and addressed, please DO NOT add any additional explainations or comments, ONLY answer using markdown code depending on the case (Issues Found or No Issues Found) without triple apostrophes.
Please only take in consideration code that is related to any of the categories above.


The next lines are the code to review:

"""

def extract_message(response):

    try:
        data = json.loads(response)
        return data['data']['value']
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON response: {e}")
        return None


# The token should be the last non-empty line
token =f"token_here"
with open('diff_result.txt', 'r') as file:
    diff_result = file.read()
url = 'https://caas.api.godaddy.com/v1/prompts'
headers = {
    'Authorization': f"sso-jwt {token}",
    'accept': 'application/json',
    'Content-Type': 'application/json'
}

data = {
    "prompt": f"'{prompt}\n{diff_result}'",
    "provider": "openai_chat",
    "providerOptions":
    {
        "model": "gpt-4o",
        "temperature": 0.7,
        "top_p": 1,
        "max_tokens": 4096
    },
    "isPrivate": "false"
}

response = requests.post(url, headers=headers, json=data)
json_message = f"{response.text}"
message = extract_message(json_message)
print(message)
with open('result.txt', 'w') as file:
    file.write(str(message))
