import os

from groq import Groq

client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)
query = "Why is the sky blue?"
chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "system",
            "content": 'You are a helpful assistant that responds to questions from the user. You always respond in JSON format which has two keys. "Speech" and "Data". A detailed response to the question should be stored in the "Data" key of the JSON object and wrappered in <data></data> opening/closing tags.. A short conversational version that\'s not too lengthy and can be easily spoken in a few seconds should be stored in "Speech" and the value should be wrapped in opening <speech> and closing </speech> tagh.\nExamples:\n{\n  "Speech": "<speech>Yes, dogs can look up, though their range of motion might be more limited compared to humans.</speech>",\n  "Data": "<data>Dogs are capable of looking up but their neck and skull structure allows a more restricted range of upward vision compared to humans. This means while dogs can definitely look upwards, they won\'t have the same vertical range as humans do, and how high they can look can also depend on the breed and the individual dog’s anatomy.</data>"\n}\n{\n  "Speech": "<speech>Yes, ducks can look up. They have flexible necks that allow them to move their heads in various directions.</speech>",\n  "Data": "<data>Ducks have a good range of motion in their necks, enabling them to look up and around easily. This flexibility helps them stay alert to their surroundings and look for predators or other threats from different angles, including above.</data>"\n}',
        },
        {"role": "user", "content": query},
    ],
    model="mixtral-8x7b-32768",
    stream=True,
)

for i in chat_completion:
    print(i)
