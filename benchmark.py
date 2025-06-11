import re
import json

# --- Part 1: Function to extract the full boxed command ---

def extract_boxed_content(text: str) -> str | None:
    """
    Finds the last occurrence of '\\boxed' and returns the rest of the string.

    This avoids regex parsing issues with nested braces by finding the last
    instance of the command and assuming it's the final answer.

    Args:
        text: The string to search within.

    Returns:
        The substring starting from the last "\\boxed" command, or None if not found.
    """
    # Use rfind() to get the starting index of the last occurrence of '\\boxed'.
    last_boxed_index = text.rfind('\\boxed')
    
    if last_boxed_index != -1:
        # Return the substring from that index to the end of the string.
        # .strip() is added to remove potential leading/trailing whitespace.
        return text[last_boxed_index:].strip()
    else:
        # Return None if no instance of '\\boxed' was found.
        return "no box found"

# --- Part 2: Function to process the JSONL file and save results ---

def process_jsonl_file(input_filepath: str, output_filepath: str | None = None) -> list[str]:
    """
    Loads a JSONL file, extracts the full boxed command, and optionally saves it.

    This function iterates through a JSONL file, parsing each line as a JSON object.
    It applies the extract_boxed_content function to each string found in the 'turns' list.
    If an output_filepath is provided, it writes all extracted commands to that file.

    Args:
        input_filepath: The path to the input .jsonl file.
        output_filepath: Optional. The path to the output text file where results
                         will be saved, one per line.

    Returns:
        A list of all extracted boxed commands found in the file.
    """
    all_extractions = []
    try:
        with open(input_filepath, 'r', encoding='utf-8') as f:
            for line in f:
                data = json.loads(line)
                choices = data.get("choices", [])
                if choices and isinstance(choices, list):
                    turns = choices[0].get("turns", [])
                    for turn_text in turns:
                        if isinstance(turn_text, str):
                            extracted = extract_boxed_content(turn_text)
                            if extracted:
                                all_extractions.append(extracted)
                                
    except FileNotFoundError:
        print(f"Error: The file '{input_filepath}' was not found.")
        return [] # Return empty list on error
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON on a line in '{input_filepath}': {e}")
    except Exception as e:
        print(f"An unexpected error occurred during reading: {e}")
    
    # If an output path is provided, write the results to the file.
    if output_filepath:
        try:
            with open(output_filepath, 'w', encoding='utf-8') as f_out:
                for item in all_extractions:
                    f_out.write(item + '\n')
            print(f"\nSuccessfully wrote {len(all_extractions)} results to '{output_filepath}'")
        except Exception as e:
            print(f"Error writing to output file '{output_filepath}': {e}")
            
    return all_extractions

# --- Example Usage (for a notebook cell) ---

if __name__ == '__main__':
    # 1. Create a dummy JSONL file for demonstration purposes.
    dummy_input_file = "math500/llama38b2_40-temperature-0.0.jsonl"
    dummy_output_file = "math500/extracted_answers.txt" # Define the output file name


    # 2. Process the file, now providing an output path.
    print(f"Processing the file: {dummy_input_file}")
    extracted_results = process_jsonl_file(dummy_input_file, dummy_output_file)

    # 3. Print the results which are still returned from the function.
    print("\n--- In-Memory Results (for verification) ---")
    if extracted_results:
        for i, result in enumerate(extracted_results):
            print(f"{i+1}: {result}")
    else:
        print("No boxed content was found.")
