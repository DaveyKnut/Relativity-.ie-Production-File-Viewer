import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
import json


class IEFileViewerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Relativity .ie File Viewer")
        self.create_widgets()

    def create_widgets(self):
        # Upload button
        self.upload_button = tk.Button(self.root, text="Upload .ie File", command=self.upload_file)
        self.upload_button.pack(pady=10)

        # Summary section
        self.summary_frame = tk.Frame(self.root)
        self.summary_frame.pack(pady=10)

        self.summary_label = tk.Label(self.summary_frame, text="File Summary:", font=("Arial", 12, "bold"))
        self.summary_label.grid(row=0, column=0, sticky="w")

        self.summary_text = tk.Text(self.summary_frame, height=30, width=80, state="disabled", wrap="word")
        self.summary_text.grid(row=1, column=0, pady=5)

        # Table section
        self.table_frame = tk.Frame(self.root)
        self.table_frame.pack(pady=10)

        self.table_label = tk.Label(self.table_frame, text="Field Mapping:", font=("Arial", 12, "bold"))
        self.table_label.grid(row=0, column=0, sticky="w")

        self.table_text = tk.Text(self.table_frame, height=15, width=80, state="disabled", wrap="none")
        self.table_text.grid(row=1, column=0, pady=5)

        # Export button
        self.export_button = tk.Button(self.root, text="Export to CSV", command=self.export_to_csv, state="disabled")
        self.export_button.pack(pady=10)

        self.summary_cache = ""
        self.fields_cache = []

    def upload_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Relativity IE Files", "*.ie")])
        if file_path:
            try:
                with open(file_path, 'r') as file:
                    file_content = json.load(file)

                # Parse nested content
                raw_content = file_content.get("Content", "{}")
                parsed_content = json.loads(raw_content)

                # Display summary
                self.display_summary(parsed_content)

                # Display field mappings
                self.display_field_mapping(parsed_content.get("SelectedWorkspaceFields", []))
            except Exception as e:
                messagebox.showerror("Error", f"Failed to process the file: {str(e)}")

    def display_summary(self, content):
        self.summary_text.config(state="normal")
        self.summary_text.delete("1.0", tk.END)

        # Job metadata
        summary = {
            "Job Name": content.get("JobName", "Unknown"),
            "Export Type": content.get("ExportType", "Unknown"),
            "Total Fields": len(content.get("SelectedWorkspaceFields", [])),
            "Date Format": content.get("RegionalCultureCode", "Unknown"),
            "Long Date/Time Format": content.get("UseLongDateTime", "Unknown"),
        }

        summary_lines = []
        for key, value in summary.items():
            summary_lines.append(f"{key}: {value}")
            self.summary_text.insert(tk.END, f"{key}: {value}\n")

        # Text precedence settings
        text_settings = content.get("TextFieldPrecedenceSettings", {})
        precedence_fields = text_settings.get("Precedence", [])
        summary_lines.append("\nText Precedence Settings:")
        self.summary_text.insert(tk.END, "\nText Precedence Settings:\n")
        summary_lines.append(f"  Export Fields As Files: {text_settings.get('ExportFieldsAsFiles', 'Unknown')}")
        self.summary_text.insert(
            tk.END, f"  Export Fields As Files: {text_settings.get('ExportFieldsAsFiles', 'Unknown')}\n"
        )
        summary_lines.append(f"  Text File Encoding: {text_settings.get('TextFileEncodingCodePage', 'Unknown')}")
        self.summary_text.insert(
            tk.END, f"  Text File Encoding: {text_settings.get('TextFileEncodingCodePage', 'Unknown')}\n"
        )
        if precedence_fields:
            summary_lines.append("  Precedence Fields (Order of Text Population):")
            self.summary_text.insert(tk.END, "  Precedence Fields (Order of Text Population):\n")
            for idx, field in enumerate(precedence_fields, start=1):
                summary_lines.append(f"    {idx}. {field.get('Name', 'Unknown')}")
                self.summary_text.insert(tk.END, f"    {idx}. {field.get('Name', 'Unknown')}\n")

        # Volume settings
        advanced_settings = content.get("AdvancedSettings", {}).get("VolumeSettings", {})
        self.summary_text.insert(tk.END, "\nVolume Settings:\n")
        summary_lines.append("\nVolume Settings:")
        summary_lines.append(f"  Volume Prefix: {advanced_settings.get('VolumePrefix', 'Unknown')}")
        self.summary_text.insert(tk.END, f"  Volume Prefix: {advanced_settings.get('VolumePrefix', 'Unknown')}\n")
        summary_lines.append(f"  Volume Start Number: {advanced_settings.get('VolumeStartNumber', 'Unknown')}")
        self.summary_text.insert(tk.END, f"  Volume Start Number: {advanced_settings.get('VolumeStartNumber', 'Unknown')}\n")
        summary_lines.append(f"  Volume Max Size (MB): {advanced_settings.get('VolumeMaxSizeInMegabytes', 'Unknown')}")
        self.summary_text.insert(tk.END, f"  Volume Max Size (MB): {advanced_settings.get('VolumeMaxSizeInMegabytes', 'Unknown')}\n")
        summary_lines.append(f"  Volume Digit Padding: {advanced_settings.get('VolumeDigitPadding', 'Unknown')}")
        self.summary_text.insert(tk.END, f"  Volume Digit Padding: {advanced_settings.get('VolumeDigitPadding', 'Unknown')}\n")

        # Subdirectory settings
        subdirectory_settings = content.get("AdvancedSettings", {}).get("SubdirectorySettings", {})
        self.summary_text.insert(tk.END, "\nSubdirectory Settings:\n")
        summary_lines.append("\nSubdirectory Settings:")
        summary_lines.append(f"  Subdirectory Start Number: {subdirectory_settings.get('SubdirectoryStartNumber', 'Unknown')}")
        self.summary_text.insert(
            tk.END, f"  Subdirectory Start Number: {subdirectory_settings.get('SubdirectoryStartNumber', 'Unknown')}\n"
        )
        summary_lines.append(f"  Max Files Per Directory: {subdirectory_settings.get('MaxNumberOfFilesInDirectory', 'Unknown')}")
        self.summary_text.insert(
            tk.END, f"  Max Files Per Directory: {subdirectory_settings.get('MaxNumberOfFilesInDirectory', 'Unknown')}\n"
        )

        self.summary_cache = "\n".join(summary_lines)
        self.summary_text.config(state="disabled")

    def display_field_mapping(self, fields):
        self.table_text.config(state="normal")
        self.table_text.delete("1.0", tk.END)
        self.fields_cache = []

        if not fields:
            self.table_text.insert(tk.END, "No field mappings found in the file.")
        else:
            try:
                self.fields_cache = [
                    {"Field Name": field.get("Name", "Unknown"), "Field Type": field.get("FieldType", "Unknown")}
                    for field in fields
                ]
                df = pd.DataFrame(self.fields_cache)
                self.table_text.insert(tk.END, df.to_string(index=False))
            except Exception as e:
                self.table_text.insert(tk.END, f"Error displaying field mapping: {str(e)}")

        self.table_text.config(state="disabled")
        self.export_button.config(state="normal")

    def export_to_csv(self):
        save_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV Files", "*.csv")])
        if save_path:
            try:
                # Prepare the CSV data
                with open(save_path, 'w', encoding='utf-8') as csv_file:
                    # Write summary
                    csv_file.write(f"{self.summary_cache}\n\n")
                    # Write fields
                    if self.fields_cache:
                        field_df = pd.DataFrame(self.fields_cache)
                        field_df.to_csv(csv_file, index=False)
                    messagebox.showinfo("Success", "Data exported successfully.")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to export data: {str(e)}")


# Run the app
if __name__ == "__main__":
    root = tk.Tk()
    app = IEFileViewerApp(root)
    root.mainloop()
