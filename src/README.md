Src organization detailing:

Core - This is the core of the project, it drives all actions and will be controlled by either the commandline or the UI. It will dispense to different modules based on input parameters controlled in ../.config. It has four main components it is dependent upon:
- All of the below will be chosen either by UI or command line if chosen else will import from config
    - semantics layer: chooses from a set of possible semantics that can be used for the model (taken from semantic_layer folder)
    - encoding: lanchain or other ways of importing information for the querying (taken from encoding folder)
    - prompts: a set of instructions and prompts which must be chosen from our set we make and contain in the prompt folder.
    - models: selects the chosen model and uses the methods contained in its model's file (from the model folder)

Encoding - This is where we do some preprocessing on the users prompts to draw in extra relevant information to then create better prompts. This occurs before sending to the model. The main processes in this will likely be langchain if it performs well, will be updated as necessary.

Model - This is where all the functions needed to communicate with the models and parse the responses will occur. It will likely require some support for the models run on local GPU when necessary - could cause massive lead times if done poorly. May need to spin up instances for this purpose if we cannot get our wait times down. The functions must contain time limiting. 

Prompt - This is where we create a set of different prompts and sets we can choose from. This should contain a driver file which will have a function to return a prompt based on a set of parameters. Selecting the correct response by reading the relevant txt file and returning it. This must also contain the files for all of the prompts.

Semantics_layer - This will have files which detail all of the necessary functions to integrate and use different types of semantics layers we will try. From different instruction sets & prior knowledge sets to cube for creating an api interface. 

UI - This is where our UI will be for the entire project which will be able to run all of the steps like command line would be able to.