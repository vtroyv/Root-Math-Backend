import os
import json
from dotenv import load_dotenv
from openai import OpenAI
from typing import Dict, List, Any
from pydantic import ValidationError, RootModel,BaseModel
from ...models.question_full_response_model import GPTStructuredResponse
from ...models.lesson_response_model import GPTLessonStructedResponse

# Load environment variables from .env file
load_dotenv()

client = OpenAI(
    organization=os.getenv("OPENAI_ORG_ID"),
    api_key=os.getenv("OPENAI_API_KEY")
)

def grade_feedback(feedBackData: dict) -> dict:
    """
    Calls GPT to generate a structured marking response with a dynamic set of 'marks' keys.
    // I need to first of all change this so that it returns the feedback in a manner that can be displayed nicely, 
    # I also need to ensure that it is giving less assistance in regards to telling the answers and more incontext help!
    //Also let's try utilize more 
    """

    # print(f"The question data for the llm is {feedBackData}")
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
    # print(f"[DEBUG] GPT raw response: \n{raw_response}")

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


class Block(BaseModel):
    type: str
    level: int = None      # for 'heading' blocks
    content: str = None    # for 'heading' and 'paragraph' blocks
    points: List[str] = None  # for 'bullet-points' blocks


def grade_feedback_blocks(feedBackData: dict) -> List[Dict[str, Any]]:
    """
    Generates an array of blocks compatible with BlockRenderer:
    - { type: 'heading', level: N, content: '...' }
    - { type: 'paragraph', content: '...' }
    - { type: 'bullet-points', points: [...] }
    Wrap all math expressions in dollar signs, e.g. $x^2 + y^2$.
    Double-escape any LaTeX backslashes (e.g. use \\\\sqrt).
    """
    question_data = feedBackData.get("questionData", {})
    structured_output = question_data.get("structured-output", {})
    student_response = feedBackData.get("usersSympyResponse", "")

    # Example blocks schema
    example_blocks = [
        {"type": "heading", "level": 2, "content": "Comments"},
        {"type": "paragraph", "content": "Your solution shows good understanding."},
        {"type": "bullet-points", "points": [
            "Correct expansion: $p^2 + 2pq + q^2$.",
            "Check simplification of final term."
        ]}
    ]
    example_str = json.dumps(example_blocks, indent=2)

    # System prompt enforcing JSON schema
    system_content = (
        "Return ONLY a single JSON object **no markdown**, with exactly two keys:\n\n"
        "  1) \"feedbackBlocks\": an array of blocks of shape\n"
        "       { type: 'heading', level: <int>, content: '<string>' }\n"
        "       or { type: 'paragraph', content: '<string>' }\n"
        "       or { type: 'bullet-points', points: ['<string>', …] }\n\n"
        "  2) \"isCorrect\": a Boolean, true if the student earned all the marks (i.e. 4/4), false otherwise.\n\n"
        "Wrap every math expression in dollar signs ($…$) and double-escape backslashes (\\\\sqrt).  \n"
        "Here’s an example output:\n"
        '{\n'
        '  "feedbackBlocks": [\n'
        '    { "type": "heading", "level": 2, "content": "Comments" },\n'
        '    { "type": "paragraph", "content": "Good algebraic manipulation." },\n'
        '    { "type": "bullet-points", "points": [\n'
        '       "Correct expansion: $p^2 + 2pq + q^2$.",\n'
        '       "Remember to take the square root of both sides."\n'
        '     ] }\n'
        '  ],\n'
        '  "isCorrect": false\n'
        '}'
    )

    

    # Build messages
    criteria_text = "".join(f"- {inst}\n" for key, inst in structured_output.items() if key not in ('totalMarks','finalFeedback'))
    user_content = (
        f"Here is the student's Sympy response:\n{student_response}\n\n"
        "Based on the marking criteria below, generate structured feedback blocks as described.\n"
        + criteria_text
        + f"Total marks guidance: {structured_output.get('totalMarks','')}\n"
        + f"Overall summary instructions: {structured_output.get('finalFeedback','')}"
    )
    messages = [
        {"role": "system", "content": system_content},
        {"role": "user", "content": user_content}
    ]

    resp = client.chat.completions.create(
        model="chatgpt-4o-latest",
        messages=messages,
        temperature=0.3,
        max_tokens=1500,
        store=True
    )
    raw = resp.choices[0].message.content.strip()
    try:
        parsed = json.loads(raw)
    except json.JSONDecodeError as e:
        raise ValueError(f"Response not valid JSON: {e}\nRaw response:\n{raw}")

    # extract our two keys
    feedback_blocks = parsed["feedbackBlocks"]
    is_correct      = parsed["isCorrect"]

    # validate each block as before
    blocks = []
    errors = []
    for idx, item in enumerate(feedback_blocks):
        try:
            blocks.append(Block.parse_obj(item).dict(exclude_none=True))
        except ValidationError as ve:
            errors.append(f"Block {idx} invalid: {ve}")

    if errors:
        raise ValueError("Invalid block structure:\n" + "\n".join(errors) + f"\nRaw response:\n{raw}")

    return {'feedback':blocks, 'status':is_correct}

    


def llm_sketch_feedback(coords:list, tools_output:list, guide:dict) -> List[Dict[str,Any]]:
   
    # print('the tools output in llm is', tools_output)

    
    in_correct_features = []
    
    comparison_list = tools_output[0]['comparison']
    
    for i in comparison_list:
        if (i['is_correct'] != True):
            in_correct_features.append(i['label'])
            
        
    
    guidance = guide['feedback']['response']
    
    
    # Now lets get a list of the labels which we will cross check with the response object
    print('the coords are ', coords)
    print('the guidance for the llm is ', guidance)
    
    print('the incorrect features are ', in_correct_features)
    
    labels=[]
    for i in coords:
        labels.append(i['label'])
    
    if (len(labels) == len(in_correct_features)):
        return guidance['all']
    
    else:
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
        

def multiple_choice_image_response(feeddBackData: dict) -> dict:
    #GOING TO NEED TO COME BACK HERE AND MARK IT PROPERLY
    
    # This function will be slightly different starting off in the initial MVP version it won't be using any llm powered capabilities
    # However down the line I seek to use llm powered capabilities to input actual images and provide more unique feedback
    #FIRST OF ALL YOU NEED TO READ THE EXPLANATION AND CORRECT OR INCORRECT FROM THE TASK
    print('The feedback data is ', feeddBackData)
    return ({
        "feedback": "This is a multiple choice image response",
        "correct": True
    })


def ask_tutor_response(promptData: dict) -> dict:
    pass

