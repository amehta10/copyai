from flask import Flask, render_template, request
import requests
import json

WORKFLOW_ID = "PKGW-51585ccc-7c38-4716-853a-96758a4e5d33"
API_KEY = "a1681819-df35-4d64-97db-ec81c13225d8"

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':


        def start_workflow_run(value1, value2):
            # Step 1: Start a workflow run
            print("start_workflow_run:",value1)
            print("start_workflow_run:",value2)
            url = f"https://api.copy.ai/api/workflow/{WORKFLOW_ID}/run"
            headers = {"x-copy-ai-api-key": API_KEY,
                       "Content-Type": "application/json"}
            payload = {
                "startVariables": {
                    "Input 1": value1,
                    "Input 2": value2
                },
	                "metadata": {"api": True}
            }

            print("Input 1:", payload["startVariables"]["Input 1"])
            print("Input 2:", payload["startVariables"]["Input 2"])

            # Convert the payload to JSON
            #json_payload = json.dumps(payload)

            response = requests.post(url, headers=headers, json=payload)
            response_data = response.json()
            run_id = response_data["data"]["id"]
            print(run_id)
            return run_id

        def track_workflow_run(run_id):
            # Step 2: Track the progress of the workflow run
            url = f"https://api.copy.ai/api/workflow/{WORKFLOW_ID}/run/{run_id}"
            headers = {"x-copy-ai-api-key": API_KEY}

            while True:
                response = requests.get(url, headers=headers)
                response_data = response.json()
                status = response_data["data"]["status"]

                if status == "COMPLETE":
                    output = response_data["data"]["output"]
                    return output

        def process_workflow_run():
            value1 = request.form['value1']
            value2 = request.form['value2']

            # Step 3: Get inputs from the user and process the workflow run
            run_id = start_workflow_run(value1, value2)
            print("Workflow run started. Tracking progress...")

            output = track_workflow_run(run_id)
            print("Workflow run complete. Output:")
            #print(output)
            text_output = output['text']

            structured_data = output['structured']
            components = json.loads(structured_data)

            formatted_text = ''
            for component in components:
                for key, value in component.items():
                    formatted_text += f"\n{key.capitalize()}: {value.strip()}\n\n"

            print(text_output)
            # Print the formatted text
            print(formatted_text)

            return text_output, formatted_text

        # Run the main function
        text_output, formatted_text = process_workflow_run()

        return render_template('result.html', text_output=text_output, formatted_text=formatted_text)
    
    return render_template('index.html')

if __name__ == '__main__':
    app.run()