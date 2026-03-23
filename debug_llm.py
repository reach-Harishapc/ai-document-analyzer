#!/usr/bin/env python3
"""
Debug script to test crewai-chat-ui LLM calls
"""
import os
from litellm import completion
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_llm_call():
    """Test a simple LLM call similar to what crewai-chat-ui might do"""
    try:
        response = completion(
            model=os.getenv('MODEL', 'groq/llama3-8b-8192'),
            messages=[
                {
                    'role': 'system',
                    'content': 'You are a helpful AI assistant that can call crew functions. You have access to a PdfRag_crew function that can research and analyze topics.'
                },
                {
                    'role': 'user',
                    'content': 'What is in my knowledge base?'
                }
            ],
            temperature=0.7,
            max_tokens=1000
        )

        print("LLM Response:")
        print(f"Model: {response.model}")
        print(f"Content: '{response.choices[0].message.content}'")
        print(f"Finish Reason: {response.choices[0].finish_reason}")
        print(f"Usage: {response.usage}")

        return response.choices[0].message.content

    except Exception as e:
        print(f"Error calling LLM: {e}")
        return None

def test_function_call():
    """Test function calling which crewai-chat-ui uses"""
    try:
        response = completion(
            model=os.getenv('MODEL', 'groq/llama3-8b-8192'),
            messages=[
                {
                    'role': 'system',
                    'content': 'You are a helpful AI assistant that can call crew functions. You have access to a PdfRag_crew function that can research and analyze topics.'
                },
                {
                    'role': 'user',
                    'content': 'Please research AI LLMs for the year 2026'
                }
            ],
            tools=[
                {
                    'type': 'function',
                    'function': {
                        'name': 'PdfRag_crew',
                        'description': 'Research and analyze topic data',
                        'parameters': {
                            'type': 'object',
                            'properties': {
                                'topic': {'type': 'string', 'description': 'The topic to research'},
                                'current_year': {'type': 'string', 'description': 'The current year'}
                            },
                            'required': ['topic', 'current_year']
                        }
                    }
                }
            ],
            temperature=0.7
        )

        print("\nFunction Call Test:")
        print(f"Model: {response.model}")
        print(f"Content: '{response.choices[0].message.content}'")
        print(f"Tool Calls: {response.choices[0].message.tool_calls}")
        print(f"Finish Reason: {response.choices[0].finish_reason}")

        return response

    except Exception as e:
        print(f"Error in function call test: {e}")
        return None

if __name__ == '__main__':
    print("Testing LLM calls for crewai-chat-ui debugging...")
    print(f"Using model: {os.getenv('MODEL', 'groq/llama3-8b-8192')}")

    # Test simple call
    content = test_llm_call()

    if content == "" or content is None:
        print("\n❌ Empty response detected! This matches the crewai-chat-ui issue.")
    else:
        print("\n✅ LLM is responding normally.")

    # Test function calling
    func_response = test_function_call()