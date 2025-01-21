# IN this file we will use GPT to interact with Sympy and attempt to mark the student's work

import os
import json
from dotenv import load_dotenv
from openai import OpenAI
from typing import Dict
from pydantic import ValidationError
from ..models.fullResponseModel import GPTStructuredResponse

# Load environment variables from .env file
load_dotenv()

client = OpenAI(
    organization=os.getenv("OPENAI_ORG_ID"),
    api_key=os.getenv("OPENAI_API_KEY")
)

def grade_feedback(feedBackData: dict) -> dict:
    """
    Calls GPT to generate a structured marking response with a dynamic set of 'marks' keys.
    """

    print(f"The question data for the llm is {feedBackData}")
    question_data = feedBackData["questionData"]
    structured_output_obj = question_data["structured-output"]
    student_work_sympy = feedBackData["usersSympyResponse"]

    # STEP 1: Separate out known top-level keys from 'structured-output'
    # (like totalMarks, finalFeedback) from the mark-specific keys (like firstMark, secondMark, etc.).
    mark_criteria: Dict[str, str] = {}
    total_marks_instructions = ""
    final_feedback_instructions = ""

    for key, instruction in structured_output_obj.items():
        if key == "totalMarks":
            total_marks_instructions = instruction
        elif key == "finalFeedback":
            final_feedback_instructions = instruction
        else:
            mark_criteria[key] = instruction

    # STEP 2: Build an example JSON "skeleton" for GPT to follow.
    marks_example = {
        "marks": {
            k: {"feedback": f"<feedback for {k} here>"}
            for k in mark_criteria.keys()
        },
        "totalMarks": "<total marks text>",
        "finalFeedback": "<overall summary>"
    }
    example_json_str = json.dumps(marks_example, indent=2)

    # STEP 3: Construct system message to force valid JSON.
    system_message = {
        "role": "system",
        "content": (
            "You are an assistant that provides structured feedback in valid JSON format. "
            "DO NOT return any extra keys, and do not wrap it in markdown. "
            "The JSON MUST match this shape:\n\n"
            f"{example_json_str}\n\n"
            "Where 'marks' is an object with each dynamic key, "
            "and each key has a single 'feedback' field (string). "
            "'totalMarks' is a string. 'finalFeedback' is a string.\n"
            "No additional fields are allowed."
        )
    }

    # STEP 4: Build user/developer messages with the student's work + instructions.
    user_messages = [
        {
            "role": "developer",
            "content": question_data.get("gpt-role-content", "")
        },
        {
            "role": "user",
            "content": (
                f"Here is the student's Sympy work:\n{student_work_sympy}\n\n"
                "Below are the marking criteria for each mark:\n"
                + "\n".join([f"{k}: {v}" for k, v in mark_criteria.items()]) + "\n\n"
                f"Total Marks Instructions: {total_marks_instructions}\n"
                f"Final Feedback Instructions: {final_feedback_instructions}\n\n"
                "Please output **only** valid JSON with the exact shape shown below. "
                "Use double quotes for all keys/strings. Return no extra text, disclaimers, or code blocks.\n\n"
                "The required JSON structure is:\n\n"
                "{\n"
                "  \"marks\": {\n"
                "    \"firstMark\": { \"feedback\": \"...\" },\n"
                "    \"secondMark\": { \"feedback\": \"...\" },\n"
                "    ...\n"
                "  },\n"
                "  \"totalMarks\": \"...\",\n"
                "  \"finalFeedback\": \"...\"\n"
                "}\n\n"
                "No additional fields are allowed. Do not wrap it in triple backticks or markdown.\n\n"
                "**Important**: Whenever you include a mathematical expression in the 'feedback' fields, "
                "wrap it using **dollar sign** notation. For example:\n"
                "  $ (p + q)^2 $   or   $ \\sqrt{4pq} $.\n\n"
                "Do NOT use backslash parentheses (\\( ... \\)). Just use $ ... $ for math.\n\n"
                "Only wrap the math; do not wrap normal text in LaTeX.\n\n"
                "Return the JSON object only, with no extra text."
            )
        }
    ]

    # STEP 5: Call the OpenAI API
    completion = client.chat.completions.create(
        model="chatgpt-4o-latest",
        messages=[system_message] + user_messages,
        temperature=0.7,
        max_tokens=2000,
        store=True,
    )

    raw_response = completion.choices[0].message.content.strip()
    print(f"[DEBUG] GPT raw response: \n{raw_response}")

    # STEP 6: Validate response with Pydantic
    try:
        json_data = json.loads(raw_response)
        validated = GPTStructuredResponse(**json_data)
        return validated.dict()  # Return a dict to the router
    except (json.JSONDecodeError, ValidationError) as e:
        print("[ERROR] GPT response invalid:\n", e)
        print("[ERROR] Raw GPT response :\n", raw_response)
        return {
            "error": "Invalid GPT Response format or schema",
            "raw_response": raw_response
        }
