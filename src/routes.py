# routes.py

from flask import request, render_template

def setup_routes(app):
    @app.route("/")
    def main():
        return render_template("index.html")

    @app.route("/echo", methods=["POST"])
    def process_input_echo():
        # Get the selected option from the query parameters
        selected_option = request.args.get("selected_option")

        if selected_option == "large_input":
            # Handle large input option
            large_input = request.form.get("large_input", "")
            # Process the large input as needed
            return render_template("echo.html", selected_option=selected_option, large_input=large_input)

        elif selected_option == "files_input":
            # Handle file upload
            uploaded_files = request.files.getlist("file_input")
            files_info = []
            for file in uploaded_files:
                # Process each uploaded file
                filename = file.filename
                file_size = len(file.read())
                # Add filename and file size to files_info list
                files_info.append({"filename": filename, "file_size": file_size})

            # Render the echo page with the uploaded file information
            return render_template("echo.html", selected_option=selected_option, files_info=files_info)
        else:
            # Handle other options (if any)
            return "Invalid option selected"


