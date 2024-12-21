# Ultimate Guide: Using Llama 3.2B with TalkDB

# Step 0: Start
**TalkDB is fun and easy to use! Let’s get started!**

# Step 1: Visit Ollama
🔗 Go to the [Ollama website](https://ollama.com/) to begin.

# Step 2: Download the Llama 3.2B Model
📥 Click the download button for Llama 3.2B and save the file on your computer.

# Step 3: Install the Model
🛠️ Open the file you downloaded and follow the on-screen instructions to complete the installation.


#### Step 4: Open the Command Prompt
- ⌨️ Press **Windows + R** to open the Run box.
- 📝 Type `cmd` and press Enter to open the Command Prompt.


#### Step 5: Download the Llama 3.2B Model via Command
📡 Type the following command in the Command Prompt and press Enter:

ollama run llama3.2

This will download and set up the Llama 3.2B model.

# Step 6: Clone the TalkDB Project
🖥️ Navigate to your workspace and run this command to clone the TalkDB project:

git clone https://github.com/prem-ramamoorthy/Project-TalkDB.git

> ⚠️ Ensure Git is installed on your computer before proceeding.

# Step 7: Install Required Libraries
📚 Go to the TalkDB folder and ensure all necessary libraries are installed. If any are missing, follow these steps:

# If Libraries Are Missing
1. ⚙ Create a virtual environment by running:

   python -m venv venv

2. 🌐 Activate the virtual environment:
   - On Windows:
     venv\Scripts\activate
   - On Mac/Linux:
     source venv/bin/activate
3. 🐼 Install the required libraries:
   pip install flask werkzeug mysql-connector-python
   
# Step 8: Start the Application
🌄 In the project folder, run the following command to start the app:

python app.py

# Step 9: Enjoy Using TalkDB
🎉 You’re all set! Use the Llama 3.2B model with TalkDB to ask questions and interact seamlessly.

# Step 10: Finish

You’ve successfully set up Llama 3.2B with TalkDB. Great work, and enjoy exploring!

