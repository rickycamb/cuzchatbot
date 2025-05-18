from flask import Flask, render_template, request, session
from difflib import get_close_matches

app = Flask(__name__)
app.secret_key = "your_secret_key_here"  # Change this to a secure secret key

# Enhanced Knowledge Base for CUZ (maintain original case)
knowledge_base = {
    # General Information
    "What programs do you offer?": "Catholic University in Zimbabwe offers programs in Commerce & IT, Education & Social Sciences, and Theology. For details visit: https://cuz.ac.zw/academic-programmes/",
    "information": "For general inquiries, email info@cuz.ac.zw or call +2638688002370",
    "contact": "Main Campus: 18443 Cranborne Ave, Harare | Email: info@cuz.ac.zw | Phone: +2638688002370",
    "campuses": "Catholic University in Zimbabwe has campuses in Harare, Bulawayo, Mutare, Gokwe, Chinhoyi, Masvingo, Gweru, and Chishawasha",

    # Admissions
    "How do I apply for admission?": "Apply online at https://portal.cuz.ac.zw/apply. Steps: 1) Create account 2) Complete form 3) Upload documents 4) Pay $20-$30 fee",
    "admission": "Apply online at: https://portal.cuz.ac.zw/apply",
    "enrol": "Apply online at: https://portal.cuz.ac.zw/apply",
    "enroll": "Apply online at: https://portal.cuz.ac.zw/apply",
    "enrollment": "Apply online at: https://portal.cuz.ac.zw/apply",
    "accommodations": "We currently do not offer accommodation kindly contact our office to assist you on +2638688002370",
    "accommodation": "We currently do not offer accommodation kindly contact our office to assist you on +2638688002370",
    "What are the admission requirements?": "Undergrad: 5 'O' Levels (English & Maths) + 2 'A' Levels. Mature entry (25+ years) with work experience also accepted",
    "deadlines": "Applications close 1-2 months before semester start (August/January intakes)",

    # Programs
    "commerce programs": "Faculty of Commerce offers: BBM&IT, Accounting, Finance, Marketing. Details: https://cuz.ac.zw/fcit/ or WhatsApp +263780008886",
    "education programs": "Faculty of Education offers: Education degrees, Social Sciences, Development Studies. Details: https://cuz.ac.zw/fessh/ or WhatsApp +263784042292",
    "theology programs": "Faculty of Theology offers: Theology degrees, Peace Building, Chaplaincy. Details: https://cuz.ac.zw/terp/ or WhatsApp +263784042292",
    "Masters": "Postgraduate programs: https://cuz.ac.zw/post-graduate-studies/",
    "Degree": "Undergraduate programs: https://cuz.ac.zw/faculty-of-commerce-innovation-and-technology/",

    # Fees
    "What is the tuition fee?": "Undergrad: ~$800-$1,200/year | Postgrad: ~$1,500-$2,000/year | Application fee: $20-$30",
    "fees": "Undergraduate: $800-$1,200/yr | Postgraduate: $1,500-$2,000/yr | Payment plans available",

    # Student Services
    "student services": "We offer: Academic advising, Counseling, Career services, Chaplaincy, and Student welfare support",

    # Short Courses
    "short courses": "We offer 3-6 month courses in: Project Management, Digital Marketing, GIS, Disaster Management, Counseling, and more. Contact respective faculties",

    # Scholarships
    "scholarships": "Limited scholarships available. Contact financial aid office at finaid@cuz.ac.zw for opportunities",

    # Conversational
    "Hi": "Hello! How can I assist you with Catholic University in Zimbabwe information today?",
    "Hello": "Welcome to Catholic University in Zimbabwe chatbot! Ask me about programs, admissions, or student services",
    "ok": "You can ask me about: 1) Academic programs 2) Admission process 3) Fees 4) Student services",
    "noted": "Feel free to ask about our programs, admission requirements, or campus information",
    "Thank you": "You're welcome! For further assistance, contact info@cuz.ac.zw",
    "Thanks": "Happy to help! Visit www.cuz.ac.zw for more details",

    # Fallback
    "default": "I couldn't understand your query. Please contact info@cuz.ac.zw or visit https://cuz.ac.zw for assistance"
}

# Keyword mapping for better matching
keyword_mapping = {
    "program": "What programs do you offer?",
    "programs": "What programs do you offer?",
    "apply": "How do I apply for admission?",
    "require": "What are the admission requirements?",
    "requirements": "What are the admission requirements?",
    "fee": "What is the tuition fee?",
    "service": "What student services are available?",
    "contact": "contact",
    "master": "Masters",
    "degree": "Degree",
    "thank": "Thank you",
    "commerce": "commerce programs",
    "education": "education programs",
    "theology": "theology programs",
    "campus": "campuses",
    "scholarship": "scholarships",
    "short course": "short courses"
}


def get_best_match(user_input):
    user_input_lower = user_input.lower()  # Only use lowercase for matching

    # First check for direct matches
    for question in knowledge_base:
        if user_input_lower == question.lower():
            return knowledge_base[question]  # Return original case response

    # Then check for keyword matches
    for keyword, mapped_question in keyword_mapping.items():
        if keyword in user_input_lower:
            return knowledge_base[mapped_question]  # Return original case response

    # Then try fuzzy matching
    questions = [q.lower() for q in knowledge_base.keys()]
    matches = get_close_matches(user_input_lower, questions, n=1, cutoff=0.6)

    if matches:
        matched_question = matches[0]
        for q in knowledge_base:
            if q.lower() == matched_question:
                return knowledge_base[q]  # Return original case response

    # Fallback to default response
    return knowledge_base["default"]


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/set_name", methods=["POST"])
def set_name():
    name = request.form.get("name", "").strip()
    if name:
        session["name"] = name
        return f"Hello {name}, how can I assist you with CUZ information today?"
    return "Hello, how can I assist you with Catholic University in Zimbabwe information today?"


@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.form.get("user_input", "").strip()
    if not user_input:
        return "Please type your question so I can assist you."

    response = get_best_match(user_input)

    # Personalize response if we have the user's name (without changing case)
    if "name" in session and not any(x in user_input.lower() for x in ["hi", "hello"]):
        response = f"{session['name']}, {response}"

    return response


if __name__ == "__main__":
    app.run(debug=True)