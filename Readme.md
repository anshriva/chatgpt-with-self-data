## Chat gpt usage on local.  
We are using the library: https://python.langchain.com/ <br> 

### Setup needed: 
1. Python3 
2. setup the environment variable for OPENAI_API_KEY which you can find on https://platform.openai.com/api-keys

### How it works? 
You can dump your data inside data folder and then all the json from the folder are picked.<br>
Then you can access the API using : 
``
curl -X POST -H "Content-Type: application/json" -d '{"prompt": "give me product for women"}' http://127.0.0.1:5000/chat
``

