import os
import requests
import random
from pathlib import Path
from openai import OpenAI
import base64

client = OpenAI()
PRIVATE_API_KEY = os.environ['IMAGE_KIT_API_KEY']
IMAGEKIT_URL = 'https://upload.imagekit.io/api/v1/files/upload'

struggles = [
    {"Category": "Emotional & Mental Well-being", "Struggle": "Parental burnout and overwhelm"},
    {"Category": "Emotional & Mental Well-being", "Struggle": "Child anxiety, depression, and emotional dysregulation"},
    {"Category": "Emotional & Mental Well-being", "Struggle": "Managing screen time without constant battles"},
    {"Category": "Emotional & Mental Well-being", "Struggle": "Feeling disconnected or guilty due to work/life imbalance"},
    {"Category": "Emotional & Mental Well-being", "Struggle": "Keeping calm during meltdowns and power struggles"},
    
    {"Category": "Technology & Media", "Struggle": "Balancing tech use and real-life connection"},
    {"Category": "Technology & Media", "Struggle": "Worrying about social media exposure and self-esteem"},
    {"Category": "Technology & Media", "Struggle": "Monitoring AI tools, chatbots, and online safety"},
    {"Category": "Technology & Media", "Struggle": "Competing with constant digital stimulation"},
    {"Category": "Technology & Media", "Struggle": "Deciding when and how to introduce smartphones"},
    
    {"Category": "Daily Routines & Discipline", "Struggle": "Getting kids to listen without yelling"},
    {"Category": "Daily Routines & Discipline", "Struggle": "Creating consistent routines amid chaos"},
    {"Category": "Daily Routines & Discipline", "Struggle": "Dealing with picky eating and mealtime drama"},
    {"Category": "Daily Routines & Discipline", "Struggle": "Bedtime resistance and sleep struggles"},
    {"Category": "Daily Routines & Discipline", "Struggle": "Keeping kids motivated for chores, homework, or school"},
    
    {"Category": "Relationships & Connection", "Struggle": "Feeling like you're failing or not doing enough"},
    {"Category": "Relationships & Connection", "Struggle": "Staying present instead of reactive"},
    {"Category": "Relationships & Connection", "Struggle": "Navigating sibling rivalry and conflict"},
    {"Category": "Relationships & Connection", "Struggle": "Helping your child feel safe, seen, and loved"},
    {"Category": "Relationships & Connection", "Struggle": "Repairing after conflict or disconnection"},
    
    {"Category": "Values & the Bigger Picture", "Struggle": "Raising emotionally intelligent, kind humans"},
    {"Category": "Values & the Bigger Picture", "Struggle": "Helping kids manage stress in a fast-paced world"},
    {"Category": "Values & the Bigger Picture", "Struggle": "Teaching resilience and optimism in uncertain times"},
    {"Category": "Values & the Bigger Picture", "Struggle": "Protecting childhood without over-sheltering"},
    {"Category": "Values & the Bigger Picture", "Struggle": "Balancing structure with freedom and creativity"},
    
    {"Category": "Modern Family Life", "Struggle": "Coping with co-parenting challenges or differing styles"},
    {"Category": "Modern Family Life", "Struggle": "Raising neurodivergent children with support and understanding"},
    {"Category": "Modern Family Life", "Struggle": "Managing finances while meeting kids' needs and desires"},
    {"Category": "Modern Family Life", "Struggle": "Supporting learning differences and school-related struggles"},
    {"Category": "Modern Family Life", "Struggle": "Finding your own parenting voice amid advice overload"},
]

principles = [
    {"Principle": "Connection over correction", "Category": "Connection & Presence", "Scientific Support": "Attachment theory; emotion coaching research (Gottman)"},
    {"Principle": "Stay tuned to your own alignment first", "Category": "Modeling & Vibration", "Scientific Support": "Self-regulation & emotional contagion (Hatfield et al.)"},
    {"Principle": "Your child’s emotions are guidance", "Category": "Emotional Regulation", "Scientific Support": "Somatic markers theory; interoception science"},
    {"Principle": "Appreciate your child as they are", "Category": "Modeling & Vibration", "Scientific Support": "Positive reinforcement; unconditional positive regard (Rogers)"},
    {"Principle": "Don't try to fix their negative emotion—be a calm presence", "Category": "Emotional Regulation", "Scientific Support": "Co-regulation; emotion socialization (Morris et al.)"},
    {"Principle": "Focus on what you want to see, not what you don’t", "Category": "Belief & Focus", "Scientific Support": "Selective attention; expectancy theory"},
    {"Principle": "Your mood sets the tone", "Category": "Modeling & Vibration", "Scientific Support": "Emotional contagion; parent affect impacts child behavior"},
    {"Principle": "Let go of needing them to be different so you can feel better", "Category": "Modeling & Vibration", "Scientific Support": "Differentiation of self (Bowen theory)"},
    {"Principle": "Trust their inner guidance", "Category": "Autonomy & Growth", "Scientific Support": "Self-determination theory"},
    {"Principle": "Don’t make your child responsible for your emotions", "Category": "Emotional Regulation", "Scientific Support": "Parentification research; boundaries literature"},
    {"Principle": "Soft is strong: lead with love, not control", "Category": "Connection & Presence", "Scientific Support": "Authoritative parenting (vs authoritarian)"},
    {"Principle": "Focus on connection during conflict", "Category": "Connection & Presence", "Scientific Support": "Emotionally responsive parenting; affective neuroscience"},
    {"Principle": "What you believe about your child becomes your reality", "Category": "Belief & Focus", "Scientific Support": "Pygmalion effect; confirmation bias"},
    {"Principle": "Practice appreciating your child daily", "Category": "Modeling & Vibration", "Scientific Support": "Positive psychology; gratitude interventions"},
    {"Principle": "Every child is different—honor their uniqueness", "Category": "Autonomy & Growth", "Scientific Support": "Differentiated instruction; temperament theory"},
    {"Principle": "Let them have their own emotional journey", "Category": "Emotional Regulation", "Scientific Support": "Emotion coaching; autonomy-supportive parenting"},
    {"Principle": "Don’t try to teach when they’re dysregulated", "Category": "Emotional Regulation", "Scientific Support": "Neurobiology of learning; amygdala hijack (Goleman)"},
    {"Principle": "Your vibration matters more than your words", "Category": "Modeling & Vibration", "Scientific Support": "Nonverbal communication research"},
    {"Principle": "Be the energy you want to see", "Category": "Modeling & Vibration", "Scientific Support": "Mirror neurons; behavioral modeling"},
    {"Principle": "Invite cooperation, don’t demand obedience", "Category": "Connection & Presence", "Scientific Support": "Collaborative parenting; autonomy-support"},
    {"Principle": "Let your alignment be more influential than their behavior", "Category": "Modeling & Vibration", "Scientific Support": "Social referencing; emotional regulation"},
    {"Principle": "Focus on solutions, not problems", "Category": "Belief & Focus", "Scientific Support": "Solution-focused therapy; cognitive reframing"},
    {"Principle": "Don’t argue for your limitations—or theirs", "Category": "Belief & Focus", "Scientific Support": "Self-efficacy theory (Bandura)"},
    {"Principle": "Tune into what feels good and true in the moment", "Category": "Emotional Regulation", "Scientific Support": "Interoceptive awareness; mindfulness research"},
    {"Principle": "Expect things to go well", "Category": "Belief & Focus", "Scientific Support": "Optimism research; placebo effect parallels"},
    {"Principle": "Speak to their inner being, not their behavior", "Category": "Connection & Presence", "Scientific Support": "Attachment theory; respect-based parenting"},
    {"Principle": "Let the contrast help you clarify your desire", "Category": "Emotional Regulation", "Scientific Support": "Cognitive appraisal theory; growth mindset"},
    {"Principle": "Imagine the version of them you want to grow", "Category": "Belief & Focus", "Scientific Support": "Visioning; developmental priming"},
    {"Principle": "Relieve yourself of the burden to be perfect", "Category": "Emotional Regulation", "Scientific Support": "Self-compassion (Neff); modeling imperfection"},
    {"Principle": "Alignment is the most effective form of discipline", "Category": "Modeling & Vibration", "Scientific Support": "Modeling behavior; self-regulation research"},
    {"Principle": "Say yes to what’s working", "Category": "Connection & Presence", "Scientific Support": "Positive reinforcement; appreciative inquiry"},
    {"Principle": "Make your child feel seen and safe", "Category": "Connection & Presence", "Scientific Support": "Felt safety (Siegel); polyvagal theory"},
    {"Principle": "Let them feel their feelings without fixing", "Category": "Emotional Regulation", "Scientific Support": "Emotion validation; distress tolerance"},
    {"Principle": "Trust in their natural desire to feel good", "Category": "Autonomy & Growth", "Scientific Support": "Intrinsic motivation; flow theory"},
    {"Principle": "Don’t use fear to motivate", "Category": "Autonomy & Growth", "Scientific Support": "Threat-based parenting consequences; cortisol effects"},
    {"Principle": "Use contrast as a launch pad, not a punishment", "Category": "Belief & Focus", "Scientific Support": "Growth mindset; narrative psychology"},
    {"Principle": "Align before you respond", "Category": "Emotional Regulation", "Scientific Support": "Response flexibility; mindfulness practice"},
    {"Principle": "Drop the story—be present", "Category": "Connection & Presence", "Scientific Support": "Mindfulness; ACT (acceptance and commitment therapy)"},
    {"Principle": "Believe in their potential more than their performance", "Category": "Belief & Focus", "Scientific Support": "Fixed vs growth mindset; self-fulfilling prophecy"}
]

child_stages = [
    "toddler",
    "preschooler",
    "early childhood",
    "middle childhood",
    "tween",
    "teen",
]

points_of_view = [
    "mother",
    "father",
    "child",
]

names = [
    'Charles', 'Charlotte', 'Kairo', 'Asher', 'Chloe', 'Isla', 'Eleanor', 'Sofia', 'Julian', 'Thiago',
    'Naomi', 'Willa', 'Aurora', 'Axel', 'Giselle', 'Iris', 'Farah', 'Aiden', 'Emilia', 'Edison',
    'Lily', 'Hugo', 'Antonio', 'August', 'Zoey', 'Lars', 'Jack', 'Cassius', 'Kai', 'Adeline',
    'Viktor', 'Livia', 'Bodhi', 'Ximena', 'Javier', 'Levi', 'Hazel', 'Oscar', 'Lior', 'Ronan',
    'Gabriel', 'Yosef', 'Ines', 'Zara', 'Camila', 'Cleo', 'Isaac', 'Delilah', 'Gunnar', 'Hassan',
    'David', 'Andres', 'Lucy', 'Elio', 'Omar', 'Avery', 'Ivy', 'Indira', 'Leandro', 'Vivian',
    'Dakota', 'Marina', 'Logan', 'Willow', 'Remy', 'Tessa', 'Leo', 'Nora', 'Yara', 'Anjali',
    'Dimitri', 'Maverick', 'Benjamin', 'Jude', 'Dante', 'Jace', 'Celeste', 'Nova', 'Carmen', 'Daniel',
    'Freya', 'Gemma', 'Mira', 'Sage', 'Felix', 'Penelope', 'Niko', 'Hudson', 'Sebastian', 'Aurelia',
    'Laila', 'Elizabeth', 'Vihaan', 'Addison', 'Sasha', 'Dylan', 'Kenji', 'Emma', 'Matilda', 'Rhea',
    'Stella', 'Zain', 'Uriel', 'Mateo', 'Anthony', 'Salma', 'Ethan', 'Grayson', 'Xander', 'James',
    'William', 'Everly', 'Marco', 'Amara', 'Mila', 'Riya', 'Joseph', 'Pax', 'Adrian', 'Scarlett',
    'Rowan', 'Paloma', 'Abigail', 'Jayden', 'Nina', 'Luna', 'Victoria', 'Keira', 'Rafael', 'Layla',
    'Jamal', 'Soren', 'Lincoln', 'Vera', 'Aaliyah', 'Michael', 'Arlo', 'Rishi', 'Tariq', 'Noah',
    'Leona', 'Harper', 'Kian', 'Sarai', 'Gunnar', 'Elias', 'Everett', 'Liam', 'Mason', 'Stella',
    'Selah', 'Emily', 'Alina', 'Olivia', 'Jasmine', 'Finn', 'Amelia', 'Sienna', 'Arjun', 'Jonas',
    'Elijah', 'Lucia', 'Riley', 'Julian', 'Shiloh', 'Samuel', 'Calliope', 'Karim', 'Cassius', 'Charlotte',
    'Willow', 'Quinn', 'Zoe', 'Ayden', 'Hazel', 'Theodore', 'Maya', 'Michael', 'Esme', 'Ezra',
    'Aurora', 'Eliana', 'Emma', 'Abigail', 'Aurelia', 'Leo', 'Eleanor', 'Harper', 'Mateo', 'Lucas',
    'Selah', 'Vivian', 'Sofia', 'Athena', 'James', 'Camila', 'Sienna', 'Benjamin', 'Gianna', 'Malik',
    'Anika', 'Rania', 'Isabella', 'Olivia', 'Akira', 'Isaac', 'Grayson', 'Layla', 'Josiah', 'Sage',
    'Mila', 'Antonio', 'Rowan', 'Penelope', 'Dalia', 'Julian', 'Noah', 'Lucy', 'Pilar', 'Scarlett',
    'Dora', 'Lila', 'Gabriel', 'Matthew', 'Ember', 'Willa', 'Hudson', 'Michael', 'Joseph', 'Jaxon',
    'Talia', 'Sophia', 'Yasmin', 'Ivy', 'Willow', 'Sofia', 'Mateo', 'Mason', 'Leah', 'Carter',
    'Evelyn', 'Riley', 'Julian', 'Kali', 'Luna', 'Aurora', 'Ava', 'Emily', 'Layla', 'Zoey',
    'Chloe', 'Jack', 'Oliver', 'Samuel', 'Victoria', 'Gianna', 'Liam', 'Nora', 'Isla', 'Sofia',
    'Owen', 'Emma', 'Henry', 'Grace', 'Isabella', 'Sophia', 'Zara', 'Ella', 'Stella', 'Nia',
    'Willow', 'Lily', 'Avery', 'Ava', 'Addison', 'Hazel', 'Ella', 'Sofia', 'Charlotte', 'Mia'
]

subject_starters = [
    "drop of",
    "moment of",
    "boost of",
    "dose of",
    "hit of",
    "nudge toward",
    "spark of"
]

subject_finishers = [
    "emotional attunement",
    "connection",
    "calm",
    "peace",
    "parental mastery",
    "presence",
    "clarity",
    "grace",
    "love",
    "stillness",
    "soulful parenting",
    "sacred pause",
    "soft strength"
]

def generate_story(struggle, child_stage, point_of_view, name1, name2):
    
    prompt = f"""
        You are an award-winning short story writer.
        Write a short vignette that illustrates a family dealing with: {struggle}

        Pick the top 5 Abraham-Hicks-inspired principles from the following list that could help with the issue above, then pick 1 of those at random, and weave it into the story.
        Principles: {principles}

        The vignette should include a child in the {child_stage} stage.
        It should be written from the point of view of the: {point_of_view}
        Characters in the story can be named {name1} and/or {name2}.
        
        Do not explicity mention Abraham-Hicks.
        Length: Between 150 and 200 words. Use short paragraphs.
        Only return the vignette and nothing else.
    """

    completion = client.chat.completions.create(
        model="o4-mini",
        messages=[
            {
                "role": "user",
                "content": prompt,
            },
        ],
    )

    return completion.choices[0].message.content

def generate_title(story):
    
    prompt = f"""
        Write a short title the following story.
        Length: 5-8 words.
        Story: {story}
      
        Only return the title and nothing else.
    """

    completion = client.chat.completions.create(
        model="o4-mini",
        messages=[
            {
                "role": "user",
                "content": prompt,
            },
        ],
    )

    return completion.choices[0].message.content

def generate_appreciation(story):
    
    prompt = f"""
        You are an award-winning short story writer.
        Write a short "rampage of appreciation" in the style of Abraham-Hicks, relating to the following story, but more generic, without mentioning specific story details: {story}
      
        Do not explicitly mention Abraham-Hicks.
        Length: Between 50 and 75 words.
        Only return the rampage of appreciation and nothing else.
        Each sentence should be on its own line.
        Include at least one sentence appreciating something about children or parenthood.

        Example:
        Oh, what a delight it is to be the one my child turns to in the quiet moments!
        I love remembering that my calm is a gift to them and to me.
        I appreciate the sacred chaos of parenting, where love is louder than logic.
        I revel in the small wins—the glances, the breath, the laughter.
        I honor the journey we’re on, and how beautiful it is to walk it with awareness.        
    """

    completion = client.chat.completions.create(
        model="o4-mini",
        messages=[
            {
                "role": "user",
                "content": prompt,
            },
        ],
    )

    return completion.choices[0].message.content

def generate_mantra(story, appreciation):
    
    prompt = f"""
        Write a 1-sentence mantra in the style of Abraham-Hicks that relates to the following story and rampage of appreciation, but more generic, without mentioning specific details.
        Story: {story}
        Rampage of appreciation: {appreciation}
      
        Do not explicity mention Abraham-Hicks.
        Only return the mantra and nothing else.
        Length: 6-9 words.

        Example: The energy I bring to the task is more important than the task itself.
    """

    completion = client.chat.completions.create(
        model="o4-mini",
        messages=[
            {
                "role": "user",
                "content": prompt,
            },
        ],
    )

    return completion.choices[0].message.content

def generate_intro(story, appreciation, mantra, struggle):
    
    prompt = f"""
        Write a 2-sentence email intro in the style of Abraham-Hicks for parents who may be struggling with: {struggle}
        Include a warm greeting.
        
        The content of the email is as follows:
        Story: {story}
        Rampage of appreciation: {appreciation}
        Mantra: {mantra}
      
        Do not explicity mention Abraham-Hicks.
        Use second person and perhaps first person plural.
        Only return the 2-sentence email intro and nothing else.
        Length: 30-40 words

        
    """

    completion = client.chat.completions.create(
        model="o4-mini",
        messages=[
            {
                "role": "user",
                "content": prompt,
            },
        ],
    )

    return completion.choices[0].message.content

def generate_image(story):
    response = client.images.generate(
		model="dall-e-3",
		prompt=f"""
            ### INSTRUCTION (critical – obey exactly)
            Create a single 1024×1024 image.  
            The final image must contain **zero** letters, numbers, symbols, words, logos, signatures, signage, speech bubbles, or text‑like marks of any kind.

            ### ART STYLE
            - Beautiful fractal mosaic digital painting style, with angular color blocking, light pastel tones, geometric shadows, and painterly light. 
            - Stylized realism with emotional depth and cinematic composition.

            ### CRITICAL – FACE QUALITY
            Render all faces with natural, realistic proportions, clear symmetrical features, and gentle, authentic smiles. No distortions, no extra facial elements, no text.


            ### SUBJECT
            An art piece depicting the following story: {story}
		""",
		size="1024x1024",
		quality="standard",
		n=1,
	)

    return response.data[0].url

def generate_sign_off(struggle):
    
    prompt = f"""
        Write a super short email sign-off to end an email newsletter for parents with all of the love and enthusaism of Abraham-Hicks.
        
        Assume the parent is struggling with the following: 
        {struggle}

        Do not explicity mention Abraham-Hicks or words that are specific to them.
        Do not include any tips or to-dos, just encouragement.
        Only return the sign-off and nothing else.
        Use second person and perhaps first person plural.
        Include zero closing/valediction.
        Length: Between 15 and 20 words.
    """

    completion = client.chat.completions.create(
        model="o4-mini",
        messages=[
            {
                "role": "user",
                "content": prompt,
            },
        ],
    )

    return completion.choices[0].message.content

def save_image(image_url, email_date):
    image_response = requests.get(image_url)
    if image_response.status_code == 200:
        image_path = Path("images") / f"{email_date}.png"
        with open(image_path, 'wb') as image_file:
            image_file.write(image_response.content)
    else:
        print("Failed to download the image.")

def save_subject(subject, email_date):
    subject_path = Path("emails") / f"{email_date}/subject.txt"
    with open(subject_path, 'w') as subject_file:
        subject_file.write(subject)

def create_email_dir(email_date):
    email_dir = Path("emails") / email_date
    email_dir.mkdir(parents=True, exist_ok=True)

def save_email(intro, title, story, appreciation, mantra, sign_off, email_date):
    email_dir = Path("emails") / email_date
    email_path = email_dir / "content.html"
    
    with open(Path("template.html"), "r") as template_file:
        template = template_file.read()
    with open(Path("template.css"), "r") as css_file:
        css = css_file.read()

    if "," in intro.split(".")[0]:
        intro = "<b>" + intro.split(",")[0] + "</b>," + ",".join(intro.split(",")[1:])

    story_lines = story.split('\n')
    story = ''
    for i, line in enumerate(story_lines):
        if i == 0 and line.strip():
            first_char = line[0]
            rest_of_line = line[1:]
            story += f'<p><span class="dropcap">{first_char}</span>{rest_of_line}</p>\n'
        elif line.strip():
            story += f'<p>{line}</p>\n'

    appreciation_lines = appreciation.split('\n')
    appreciation = ''
    for line in appreciation_lines:
        if line.strip():
            appreciation += f'<li>{line.strip()}</li>\n'

    content = template.format(
        css=css,
        email_date=email_date,
        intro=intro,
        title=title,
        story=story,
        appreciation=appreciation,
        mantra=mantra,
        sign_off=sign_off
    )
    
    with open(email_path, "w") as email_file:
        email_file.write(content)

def upload_image(email_date):
    # Upload from file (can also use base64 or URL)
    file_path = f"images/{email_date}.png"

    with open(file_path, 'rb') as f:
        file_data = f.read()

    # Encode the image as base64
    encoded_file = base64.b64encode(file_data).decode()

    # Optional: specify a filename and folder
    payload = {
        'file': encoded_file,
        'fileName': f"{email_date}.png",
        'folder': '/primedparents',
        'useUniqueFileName': 'false',
    }

    # Make the request
    response = requests.post(
        IMAGEKIT_URL,
        auth=(PRIVATE_API_KEY, ''),
        data=payload
    )

    # Parse and print the CDN URL
    if response.status_code == 200:
        result = response.json()
    else:
        print("Upload failed:", response.text)

    return result['url']

def run(email_date):
    struggle = random.choice(struggles)
    child_stage = random.choice(child_stages)
    point_of_view = random.choice(points_of_view)
    name1 = random.choice(names)
    name2 = random.choice(names)
    subject_starter = random.choice(subject_starters)
    subject_finisher = random.choice(subject_finishers)
    subject = f"🫶 Your daily {subject_starter} {subject_finisher}"

    print(subject)
    print(struggle)
    print(child_stage)
    print(point_of_view)

    story = generate_story(struggle, child_stage, point_of_view, name1, name2)

    title = generate_title(story)

    appreciation = generate_appreciation(story)

    mantra = generate_mantra(story, appreciation)

    sign_off = generate_sign_off(struggle)

    intro = generate_intro(story, appreciation, mantra, struggle)

    image = generate_image(story)

    create_email_dir(email_date)
    save_subject(subject, email_date)
    save_email(intro, title, story, appreciation, mantra, sign_off, email_date)
    save_image(image, email_date)
    image_url = upload_image(email_date)

    print(email_date)
    print(intro)
    print("")
    print("")
    print(title)
    print("")
    print("")
    print(story)
    print("")
    print("")
    print(appreciation)
    print("")
    print("")
    print(mantra)
    print("")
    print("")
    print(sign_off)
    print(image_url)


email_date = os.getenv('STARTING_DATE')
run(email_date)