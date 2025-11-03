# generate_email.py
data = {
  "subject": "Application: Backend Developer Position",
  "body": """Dear HCL Hiring Team,

I am writing to express my enthusiastic interest in the Backend Developer position at HCL. With a robust background in developing scalable and efficient backend systems, I am particularly drawn to HCL's innovative projects and reputation for technological excellence.

My experience includes proficiency in modern programming languages like Python and Java, designing RESTful APIs, and managing databases. I am confident my skills in building robust, high-performance applications align well with the requirements of this role, and I am eager to contribute to your team's success.

My resume, attached for your review, provides further detail on my qualifications. I welcome the opportunity to discuss how my expertise can benefit HCL. Thank you for your time and consideration.

Sincerely,
[nameOA]
"""
}

name = "vishesh"


final = data["body"].replace("[nameOA]", name)
print(final)
