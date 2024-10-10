import json
from transformers import pipeline


class NLExplanationGenerator:
    def __init__(self, model_name="gpt2"):
        self.generator = pipeline("text-generation", model=model_name)

    def generate_explanation(self, json_data):
        # Convert JSON to a string representation
        json_str = json.dumps(json_data, indent=2)

        # Generate prompt for the model
        prompt = f"Explain the following GitHub repository structure:\n\n{json_str}\n\nExplanation:"

        # Generate text
        generated_text = self.generator(prompt, max_length=500, num_return_sequences=1)[0]['generated_text']

        # Extract the explanation part
        explanation = generated_text.split("Explanation:")[1].strip()

        return explanation


def process_repository(repo_url):
    # Your existing code to fetch and analyze repository
    analysis_result = analyze_repository(repo_url)

    # Generate natural language explanation
    nl_generator = NLExplanationGenerator()
    explanation = nl_generator.generate_explanation(analysis_result)

    return {
        "analysis": analysis_result,
        "explanation": explanation
    }


if __name__ == "__main__":
    repo_url = input("Enter the GitHub repository URL to analyze: ")
    result = process_repository(repo_url)
    print(result['explanation'])

    # Save results
    with open('outputs/repo_analysis_with_explanation.json', 'w') as f:
        json.dump(result, f, indent=2)