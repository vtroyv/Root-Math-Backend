import os
import json
from dotenv import load_dotenv
from openai import OpenAI
from typing import Dict
from pydantic import ValidationError
from ..models.question_full_response_model import GPTStructuredResponse
from ..models.lesson_response_model import GPTLessonStructedResponse

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
    # (like totalMarks, finalFeedback) from the mark-specific keys (e.g., firstMark, secondMark, etc.).
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

    # STEP 2: Build an example JSON skeleton for GPT to follow.
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
    # NOTE the added instruction: "Double-escape backslashes in math expressions..."
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
            "No additional fields are allowed.\n\n"

            "IMPORTANT:\n"
            "1. When you include a LaTeX backslash (e.g. \\sqrt), you MUST double-escape "
            "   it for valid JSON. That means you write \"\\\\sqrt\" in the JSON.\n"
            "2. Make sure the dynamic mark keys match exactly: e.g. 'thirdMark' not 'thridMark'.\n"
            "3. Return only valid JSON with double quotes for all strings. No extra keys.\n"
        )
    }

    # STEP 4: Build user/developer messages with the student's work + instructions.
    #         Also emphasize the double-backslash requirement in the user prompt.
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
                "    \"thirdMark\": { \"feedback\": \"...\" },\n"
                "    ...\n"
                "  },\n"
                "  \"totalMarks\": \"...\",\n"
                "  \"finalFeedback\": \"...\"\n"
                "}\n\n"
                "No additional fields are allowed. Do not wrap it in triple backticks or markdown.\n\n"
                "**Important**: For math expressions, wrap them in dollar signs, and double-escape backslashes.\n"
                "For example, `$ \\sqrt{4pq} $` must appear as `\"$ \\\\sqrt{4pq} $\"` in valid JSON.\n\n"
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
        return validated.model_dump()  # Return a dict to the router
    except (json.JSONDecodeError, ValidationError) as e:
        print("[ERROR] GPT response invalid:\n", e)
        print("[ERROR] Raw GPT response :\n", raw_response)
        return {
            "error": "Invalid GPT Response format or schema",
            "raw_response": raw_response
        }


def sketch_feedback(feedBackData: dict) -> dict:
    pass

def grade_lesson_feedback(feedBackData: dict) -> dict:
    """
    Calls GPT to generate a structured marking response with a dynamic set of 'marks' keys.
    """
   
    task_data = feedBackData.task
    latex = feedBackData.latexInput
    gpt = task_data.task.gpt
    instructions = task_data.task.instructions

    print('The task_data is ', task_data)
    print('The latex of the students response is ', latex)
    # print(f"The gpt data is {task_data}")
    
    #Step 1: Build an example JSON skeleton for GPT to follow
    feedback_example = {
        "feedback": "<Concise feedback for task but state the reason for students work being incorrect or correct text>", 
        "correct": "<true or false bool for task boolean>"
    }
    
    feedback_example_json_str =json.dumps(feedback_example, indent=2)
    
    print(f"The feedback_example will look liks {feedback_example_json_str}")
    
    #Step 2: Construct a system message to force valud JSON.
    # NOTE the added instruction: "Double-escape backslashes in math expressions..."
    
    system_message ={
        "role":"user", # --->change this to developer when you get tier3 access 
        "content": (
            "You are an assistant that provides structured feedback in valid JSON format."
            "DO NOT return any extra keys, and do not wrap it in markdown. "
            "The JSON MUST match this shape: \n\n"
            f"{feedback_example_json_str}\n\n"
            "NO additional fields are allowed.\n\n"
             "IMPORTANT:\n"
             "1. WHen you include a Latex backslash (e.g. \\sqrt or \\cdot), you MUST double-escape "
             " it for valid JSON. That means you write \"\\\\sqrt\" in the JSON. \n"
             "2. Return only valid JSON with double quotes for all strings. No extra keys. \n"
        )
    }
    
    #Step 3: Build user/developer messages with the student's work + instructions
    #Also emphasize the double-backslash requirement in the user prompt
    
    user_messages=[
        {
            "role": "user", #----> Change this to developer when you get tier 3 access
            "content":gpt
        },
        {
            "role":"user", 
            "content": (
                f"Here is the student's work in latex: \n{latex}"
                f"Here are the instrunctions for checking if the students work is correct or incorrect: \n{instructions}"
                "Please ouput **only** valid JSON with the exact shape shown below. "
                "Use double quotes for all keys/strings. Return no extra text, disclaimers, or code blocks. \n\n"
                "The required JSON structure is: \n\n"
                "{\n"
                "  \"feedback\": \"...\", \n "
                "\" correct\": \"True || False\" \n"
                "}\n\n"
                "No additional fields are allowed. Do not wrap it in triple backticks or markdown. \n\n"
                "Please do not include the actual answer in your feedback only a hint or the reason why the student is incorrect"
                "**Important**: Fpr math expressions, essentially any latex, wrap them in dollar signs, and double-escape backslashes. \n"
                "For example, `$ \\sqrt{4pq} $` must appear as `\"$ \\\\sqrt{4pq} $\"` in valid JSON.\n\n"
                "Return the JSON object only, with no extra text."
            )
            
        }
    ]
    #Step 4: Call the OpenAI API
    completion = client.chat.completions.create(
        model ="o1-mini",
        messages=[system_message] + user_messages,
        temperature=1, 
        max_completion_tokens=2000 
        # store=True
    )
    
    
    raw_response = completion.choices[0].message.content.strip()
    print(f"[DEBUG] GPT raw response: \n{raw_response}")
    
    #STEP 5: Validate the response with pydantic 
    try:
        json_data = json.loads(raw_response)
        print(f"The json_data is {json_data}")
        validated= GPTLessonStructedResponse(**json_data)
        return validated.model_dump()
    except (json.JSONDecodeError, ValidationError) as e:
        print("[ERROR] GPT Response invalid: \n", e)
        print("[ERROR] Raw GPT response: \n", raw_response)
        return{
            "error": "Invalid GPT Response format or schema",
            "raw_response": raw_response
        }
        

def ask_tutor_response(promptData: dict) -> dict:
    pass

