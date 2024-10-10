import tkinter as tk
from tkinter import ttk, scrolledtext
import threading
from analyzer import analyze_repository, NLExplanationGenerator
import json
import os
from datetime import datetime


class AnalyzerGUI:
    def __init__(self, master):
        self.master = master
        master.title("GitHub Repository Analyzer")
        master.geometry("600x500")

        self.label = ttk.Label(master, text="Enter GitHub Repository URL:")
        self.label.pack(pady=10)

        self.entry = ttk.Entry(master, width=50)
        self.entry.pack(pady=10)

        self.analyze_button = ttk.Button(master, text="Analyze", command=self.start_analysis)
        self.analyze_button.pack(pady=10)

        self.result_text = scrolledtext.ScrolledText(master, width=70, height=20)
        self.result_text.pack(pady=10)

    def start_analysis(self):
        repo_url = self.entry.get()
        if not repo_url:
            self.result_text.insert(tk.END, "Please enter a valid GitHub repository URL.\n")
            return

        self.analyze_button.config(state=tk.DISABLED)
        self.result_text.delete('1.0', tk.END)
        self.result_text.insert(tk.END, "Analysis in progress...\n")

        thread = threading.Thread(target=self.run_analysis, args=(repo_url,))
        thread.start()

    def run_analysis(self, repo_url):
        try:
            analysis_result = analyze_repository(repo_url)
            nl_generator = NLExplanationGenerator()
            explanation = nl_generator.generate_explanation(analysis_result)

            output_dir = 'outputs'
            os.makedirs(output_dir, exist_ok=True)

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            json_filename = f"repo_analysis_{timestamp}.json"
            json_filepath = os.path.join(output_dir, json_filename)

            with open(json_filepath, 'w') as f:
                json.dump(analysis_result, f, indent=2)

            nl_filename = f"repo_explanation_{timestamp}.txt"
            nl_filepath = os.path.join(output_dir, nl_filename)

            with open(nl_filepath, 'w') as f:
                f.write(explanation)

            self.master.after(0, self.update_result,
                              f"Analysis complete!\n\nJSON saved to: {json_filepath}\nExplanation saved to: {nl_filepath}\n\nNatural Language Explanation:\n{explanation}")
        except Exception as e:
            self.master.after(0, self.update_result, f"An error occurred: {str(e)}")

    def update_result(self, text):
        self.result_text.delete('1.0', tk.END)
        self.result_text.insert(tk.END, text)
        self.analyze_button.config(state=tk.NORMAL)


if __name__ == "__main__":
    root = tk.Tk()
    gui = AnalyzerGUI(root)
    root.mainloop()