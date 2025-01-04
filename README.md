## The Book Review App
This application studies the theme of Social Isolation in literature.  The input is located in `/books` directory.
The file names must be in the format of `<author name>-<book name>.[pdf,xml,epub]`.  In production, the app can be a 
little smarter and perhaps loose this requirement.  However, for the sake of ease of implementation and time 
constraint, I keep this as the only limitation of the system.  

I experimented with different OpenAI models and chose the current ones based on efficiency and rate/token limits.

The final output is in `isolation_analysis.txt`.  The intermediate document which is used to write the final report 
is in `book_analyses.json`

### How to run
To run this app you will need to have OpenAI API key.  To obtain the key, it is necessary to register a developer account 
with OpenAI.  In production, I can modify the code to allow more providers and even allow local AI instances using 
tools like [Ollama](https://ollama.com/).

The entry point to the app is located in `main.py` and teh app can be started by running `python main.py`.  Note, that
I tested it with python version 3.10.