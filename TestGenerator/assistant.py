# -*- coding: utf-8 -*-

#pip install --upgrade tavily-python


from openai import OpenAI
from tavily import TavilyClient


class Assistant:
        
    def __init__(self, GPT_token, instructions = "None", name = "my_assistant", tools = "file_search", model = "gpt-3.5-turbo", tool_resources = None, web_browsing = False, TAVILY_KEY=None):
        if isinstance(GPT_token, str):
            self.client = OpenAI(
               api_key = GPT_token
               )
            self.GPT_token = GPT_token
        else: 
            raise TypeError("Attribute 'GPT_token' must be a string")
            
        if isinstance(instructions, str):    
            self.instructions = instructions
        else: 
            raise TypeError("Attribute 'instructions' must be a string")
        
        if isinstance(name, str):    
            self.name = name
        else: 
            raise TypeError("Attribute 'name' must be a string")
        
        if isinstance(tools, str):                   
            if self.checkTool(tools):
                self.tools = tools
        else:
            raise TypeError("Attribute 'tools' must be a string")
            
        if isinstance(model, str): 
            if self.checkModel(model):
                self.model = model
        else:
            raise TypeError("Attribute 'model' must be a string")
            
        if tool_resources!= None:
            if isinstance(tool_resources.file_search.vector_store_ids, list):
                # Check if all elements in the list are strings
                if all(isinstance(vector_store_id, str) for vector_store_id in tool_resources.file_search.vector_store_ids):
                    if(self.checkFiles(tool_resources.file_search.vector_store_ids)):
                        self.vectool_resourcestor_store_ids = tool_resources
                    else:
                        self.tool_resources = None
                else:
                    raise TypeError("all elements in 'file_ids' should be strings")
            else:
                raise TypeError("Attribute 'file_ids' must be a list")
        else:
            self.tool_resources = None
       
        if isinstance(web_browsing, bool):
            if (web_browsing and self.checkWebBrowsingCapability(self.model)):
                self.web_browsing = web_browsing 
                
                if(self.web_browsing):
                    self.tavily_client = TavilyClient(api_key=TAVILY_KEY) ## read this from env file
                else:
                    self.tavily_client = None
                    
            else:
                self.web_browsing = False
                self.tavily_client = None
        else:
            raise TypeError("Attribute 'web_browsing' must be a boolean")
            
        self.id = None
  
    def createAssistant(self):         
        if self.web_browsing:
            web_tool={
                "type": "function",
                "function": {
                    "name": "tavily_search",
                    "description": "Get recent information from the latest news in the web.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "query": {"type": "string", "description": "The search query to use"},
                        },
                        "required": ["query"]
                    }
                }
            }
            toolset = [{"type": self.tools}, web_tool]
        else:
            toolset = [{"type": self.tools}]
                            
        assistant = self.client.beta.assistants.create(
            instructions = self.instructions,
            name = self.name,
            tools = toolset,
            model = self.model,
            tool_resources = self.tool_resources
        )
        
        self.id = assistant.id 
        
        return assistant   
    
    def retrieveAssistant(self, assistant_id): 
        response = self.client.beta.assistants.list()
        
        available_ids = [assistant.id for assistant in response.data]
        if assistant_id not in available_ids:
            ValueError("Invalid assistant id, the provided id is not in the list")
            return False
        else:    
            assistant = self.client.beta.assistants.retrieve(assistant_id)
            self.instructions = assistant.instructions
            self.name = assistant.name
            self.tools = assistant.tools
            self.model = assistant.model
            self.tool_resources = assistant.tool_resources    
            self.id = assistant.id
            return True
        
    def deleteAssistant(self):
        response = self.client.beta.assistants.delete(self.id)
        return response
  
    
    def updateToken(self, token):
        if isinstance(token, str):
            self.client = OpenAI(
               api_key = token
               )
            self.GPT_token = token
        else:      
            raise TypeError("GPT token must be a string")
            
  
        
    def updateInstruction(self, instruction):
        self.instruction = instruction
        # assistant update 
        self.client.beta.assistants.update(self.id, instructions = self.instruction)
        
    def updateTool(self, tools):
        if self.checkTool(tools):
            self.tools = tools
            # assistant update 
            self.client.beta.assistants.update(self.id, tools = self.tools)

    def updateModel(self, model):
        if self.checkModel(model):
            self.model = model
            # assistant update 
            self.client.beta.assistants.update(self.id, model = self.model)

    def updateName(self, name):
        self.name = name
        # assistant update 
        self.client.beta.assistants.update(self.id, name = self.name)
    
    def updateWebBrowsing(self, web_browsing, TAVILY_KEY):
        self.web_browsing = web_browsing
        # assistant update 
        if(self.web_browsing == True):
            if(self.tavily_client == None):
                self.tavily_client = TavilyClient(api_key=TAVILY_KEY) ## read this from env file
        else:
            self.tavily_client = False    
        
    def checkTool(self, tools):
        if tools in ["code_interpreter", "file_search"]:
            return True
        else:
            ValueError("Invalid tool, it should be one of the following options: code_interpreter, retrieval, function")
            return False
        
    def checkModel(self, model):
        response = self.client.models.list()
        
        available_models = [model.id for model in response.data]
        if model not in available_models:
            ValueError("Invalid model, the provided model is not in the list")
            return False
        return True
    
    # Web-browsing is only supported by gpt-4 models, i.e.:   
    # "gpt-4-0125-preview", "gpt-4-turbo-preview", "gpt-4-turbo-2024-04-09", "gpt-4-vision-preview", "gpt-4" 
    # "gpt-4-1106-vision-preview", "gpt-4-1106-preview","gpt-4-0613", "gpt-4-turbo"
    
    def checkWebBrowsingCapability(self, model):
        response = self.client.models.list()
        
        available_models = [model.id for model in response.data]      
        gpt_4_models = [model for model in available_models if model.startswith("gpt-4")]
        
        if model not in gpt_4_models:
            ValueError("The provided model does not support web browsing")
            return False
        return True            

    def checkFiles(self, vector_store_ids):
        response = self.client.beta.vector_stores.files.list()
           
        available_files = [file.id for file in response.data]
        for file_id in vector_store_ids:
            if file_id not in available_files:
                ValueError("Invalid file, the provided file does not exist")
                return False
        return True
    
    # Function to perform a Tavily search
    def tavily_search(self, query):       
        if(query == "news"):
            query="latest news"
        try:
            search_result = self.tavily_client.get_search_context(query, search_depth="advanced", max_tokens=8000)
        except:     
            print("an error ocurred")
            search_result=""
            
        return search_result
        