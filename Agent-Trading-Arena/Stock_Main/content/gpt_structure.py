import json
import random
import openai
import time
from timeout_decorator import timeout
from content.utils import *
from database_utils import round_two_decimal, trans_url
import os
from pathlib import Path
from openai import OpenAI
import re

# Configure API based on selected provider
if llm_provider == 'openai':
    openai.api_key = openai_api_key
elif llm_provider == 'deepseek':
    from openai import OpenAI  # DeepSeek uses OpenAI-compatible API
    openai.api_key = deepseek_api_key


def temp_sleep(seconds=1):
    time.sleep(seconds)


def llm_single_request(prompt):
    """Make a single LLM request for the given prompt."""
    temp_sleep()
    if llm_provider == 'openai':
        client = OpenAI(api_key=openai_api_key)
        model = openai_model
    elif llm_provider == 'deepseek':
        client = OpenAI(api_key=deepseek_api_key, base_url=deepseek_base_url)
        model = deepseek_model
    else:
        raise ValueError(f"Unsupported LLM provider: {llm_provider}")
    
    completion = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}]
    )
    return completion.choices[0].message.content

# ============================================================================
# ########################[SECTION 1: LLM API STRUCTURE] ######################
# ============================================================================


def llm_request(prompt):
    """Make a basic LLM request for the given prompt."""
    temp_sleep()
    try:
        if llm_provider == 'openai':
            client = OpenAI(api_key=openai_api_key)
            model = openai_model
        elif llm_provider == 'deepseek':
            client = OpenAI(api_key=deepseek_api_key, base_url=deepseek_base_url)
            model = deepseek_model
        else:
            raise ValueError(f"Unsupported LLM provider: {llm_provider}")
        
        completion = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}]
        )
        return completion.choices[0].message.content
    except Exception as e:
        print(f"LLM ERROR: {type(e).__name__} - {str(e)}")
        return "LLM ERROR"


#@timeout(150)
def llm_chat_request(prompt):
    """Make an LLM chat request for the given prompt."""
    try:
        if llm_provider == 'openai':
            client = OpenAI(api_key=openai_api_key)
            model = openai_model
        elif llm_provider == 'deepseek':
            client = OpenAI(api_key=deepseek_api_key, base_url=deepseek_base_url)
            model = deepseek_model
        else:
            raise ValueError(f"Unsupported LLM provider: {llm_provider}")
        
        completion = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}]
        )
        return completion.choices[0].message.content
    except Exception as e:
        print(f"LLM ERROR: {type(e).__name__} - {str(e)}")
        return "LLM ERROR"

def llm_multimodal_request(prompt, image_url1, image_url2, image_url3):
    """Make an LLM request with multimodal support (text + images)."""
    try:
        chat_completion = openai.chat.completions.create(
              model="gpt-4o",
              messages=[
                {
                  "role": "user",
                  "content": [
                    {"type": "text", "text": prompt},
                    {"type": "image_url","image_url": {"url": image_url1,},},
                    {"type": "image_url","image_url": {"url": image_url2,},},
                    {"type": "image_url","image_url": {"url": image_url3,},},
                  ],
                }
              ],
              #max_tokens=300,
            )
        return chat_completion.choices[0].message.content

    except Exception as e:
        print(f"ChatGPT ERROR: {type(e).__name__} - {str(e)}")
        return "ChatGPT ERROR"


#@timeout(50)
def send_llm_request(prompt):
    """Send an LLM request and return the response."""
    curr_llm_response = llm_chat_request(prompt).strip()
    return curr_llm_response


def llm_safe_generate_response(
    prompt,
    example_output,
    special_instruction,
    repeat=3,
    fail_safe_response="error",
    func_validate=None,
    func_clean_up=None,
    verbose=False,
):
    prompt = 'GPT-3 Prompt:\n"""\n' + prompt + '\n"""\n'
    prompt += (
        f"Output the response to the prompt above in json. {special_instruction}\n"
    )
    prompt += "Example output json:\n"
    prompt += '{"output": "' + str(example_output) + '"}'

    if verbose:
        print("CHAT GPT PROMPT")
        print(prompt)

    for i in range(repeat):
        try:
            curr_llm_response = llm_request(prompt).strip()

            end_index = curr_llm_response.rfind("}") + 1
            curr_llm_response = curr_llm_response[:end_index]
            curr_llm_response = json.loads(curr_llm_response)["output"]

            if func_validate(curr_llm_response, prompt=prompt):
                return func_clean_up(curr_llm_response, prompt=prompt)

            if verbose:
                print("---- repeat count: \n", i, curr_llm_response)
                print(curr_llm_response)
                print("~~~~")

        except Exception as e:
            print(f"LLM connection error: {type(e).__name__} - {str(e)}")
            pass

    return False


def llm_safe_generate_response_structured(
    prompt,
    example_output,
    special_instruction,
    repeat=3,
    fail_safe_response="error",
    func_validate=None,
    func_clean_up=None,
    verbose=False,
):
    # prompt = 'GPT-3 Prompt:\n"""\n' + prompt + '\n"""\n'
    prompt = '"""\n' + prompt + '\n"""\n'
    prompt += (
        f"Output the response to the prompt above in json. {special_instruction}\n"
    )
    prompt += "Please provide the response in the following format:\n"
    prompt += '{"output": "' + str(example_output) + '"}'


    if verbose:
        print("LLM PROMPT")
        print(prompt)
    # eventlet.monkey_patch()

    for i in range(repeat):
        try:
            #url1=trans_url("plot_stock.jpg")
            #url1=trans_url("plot_stock2.jpg")
            #curr_llm_response =  llm_multimodal_request(prompt, url1, url2, url3 ).strip()
            curr_llm_response = llm_chat_request(prompt).strip()#.replace("\n","")
            curr_llm_response = re.sub(r'\s{3,}', '\n', curr_llm_response).replace("\n","\\n")
            # curr_llm_response = send_llm_request(prompt)
            #print("curr_llm_response",curr_llm_response)
            end_index = curr_llm_response.rfind("}") + 1
            curr_llm_response = curr_llm_response[:end_index]
            curr_llm_response = json.loads(curr_llm_response)["output"]


            if verbose:
                print("---LLM Response---")
                print(curr_llm_response)
                print("---end of LLM Response---")

            print(func_validate(curr_llm_response, prompt=prompt))
            if func_validate(curr_llm_response, prompt=prompt):
                return func_clean_up(curr_llm_response, prompt=prompt)

            if verbose:
                print("---- repeat count: \n", i, curr_llm_response)
                print(curr_llm_response)
                # temp_sleep(5)
        except Exception as e:
            print(f"LLM connection error: {type(e).__name__} - {str(e)}")
            pass

    #return False



def llm_safe_generate_response_legacy(
    prompt,
    repeat=3,
    fail_safe_response="error",
    func_validate=None,
    func_clean_up=None,
    verbose=False,
):
    if verbose:
        print("LLM PROMPT")
        print(prompt)

    for i in range(repeat):
        try:
            curr_llm_response = llm_chat_request(prompt).strip()
            if func_validate(curr_llm_response, prompt=prompt):
                return func_clean_up(curr_llm_response, prompt=prompt)
            if verbose:
                print(f"---- repeat count: {i}")
                print(curr_llm_response)
                print("~~~~")

        except Exception as e:
            print(f"LLM error on attempt {i+1}/{repeat}: {type(e).__name__} - {str(e)}")
            pass
    print("FAIL SAFE TRIGGERED")
    return fail_safe_response


# ============================================================================
# #########################[SECTION 2: LEGACY STRUCTURE] #####################
# ============================================================================


def llm_completion_request(prompt, llm_parameter):
    """Make an LLM completion request (legacy format)."""
    temp_sleep()
    try:
        response = openai.Completion.create(
            model=llm_parameter["engine"],
            prompt=prompt,
            temperature=llm_parameter["temperature"],
            max_tokens=llm_parameter["max_tokens"],
            top_p=llm_parameter["top_p"],
            frequency_penalty=llm_parameter["frequency_penalty"],
            presence_penalty=llm_parameter["presence_penalty"],
            stream=llm_parameter["stream"],
            stop=llm_parameter["stop"],
        )
        return response.choices[0].text
    except:
        print("TOKEN LIMIT EXCEEDED")
        return "TOKEN LIMIT EXCEEDED"


def generate_prompt(curr_input, prompt_lib_file):
    """
  Takes in the current input (e.g. comment that you want to classifiy) and 
  the path to a prompt file. The prompt file contains the raw str prompt that
  will be used, which contains the following substr: !<INPUT>! -- this 
  function replaces this substr with the actual curr_input to produce the 
  final promopt that will be sent to the GPT3 server. 
  ARGS:
    curr_input: the input we want to feed in (IF THERE ARE MORE THAN ONE
                INPUT, THIS CAN BE A LIST.)
    prompt_lib_file: the path to the promopt file. 
  RETURNS: 
    a str prompt that will be sent to OpenAI's GPT server.  
  """
    if type(curr_input) == type("string"):
        curr_input = [curr_input]
    curr_input = [str(round_two_decimal(i)) for i in curr_input]

    f = open(prompt_lib_file, "r")
    prompt = f.read()
    f.close()
    for count, i in enumerate(curr_input):
        prompt = prompt.replace(f"!<INPUT {count}>!", i)
    if "<commentblockmarker>###</commentblockmarker>" in prompt:
        prompt = prompt.split("<commentblockmarker>###</commentblockmarker>")[1]
    return prompt.strip()


def safe_llm_generate_response(
    prompt,
    gpt_parameter,
    repeat=5,
    fail_safe_response="error",
    func_validate=None,
    func_clean_up=None,
    verbose=False,
):
    if verbose:
        print(prompt)

    for i in range(repeat):
        curr_llm_response = llm_completion_request(prompt, llm_parameter)
        if func_validate(curr_llm_response, prompt=prompt):
            return func_clean_up(curr_llm_response, prompt=prompt)
        if verbose:
            print("---- repeat count: ", i, curr_llm_response)
            print(curr_llm_response)
            print("~~~~")
    return fail_safe_response


def get_embedding(text, model="text-embedding-ada-002"):
    text = text.replace("\n", " ")
    if not text:
        text = "this is blank"
    return openai.Embedding.create(input=[text], model=model)["data"][0]["embedding"]


if __name__ == "__main__":
    gpt_parameter = {
        "engine": "text-davinci-003",
        "max_tokens": 50,
        "temperature": 0,
        "top_p": 1,
        "stream": False,
        "frequency_penalty": 0,
        "presence_penalty": 0,
        "stop": ['"'],
    }
    curr_input = ["driving to a friend's house"]
    prompt_lib_file = "prompt_template/test_prompt_July5.txt"
    prompt = generate_prompt(curr_input, prompt_lib_file)

    def __func_validate(gpt_response):
        if len(gpt_response.strip()) <= 1:
            return False
        if len(gpt_response.strip().split(" ")) > 1:
            return False
        return True

    def __func_clean_up(gpt_response):
        cleaned_response = gpt_response.strip()
        return cleaned_response

    output = safe_generate_response(
        prompt, gpt_parameter, 5, "rest", __func_validate, __func_clean_up, True
    )

    print(output)
