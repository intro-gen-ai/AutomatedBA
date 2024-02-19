Core - This is the core of the project, it drives all actions and will be controlled by either the commandline or the UI. It will dispense to different modules based on input parameters controlled in ../.config. It has four main components it is dependent upon:
- All of the below will be chosen either by UI or command line if chosen else will import from config
    - semantics layer: chooses from a set of possible semantics that can be used for the model (taken from semantic_layer folder)
    - encoding: lanchain or other ways of importing information for the querying (taken from encoding folder)
    - prompts: a set of instructions and prompts which must be chosen from our set we make and contain in the prompt folder.
    - models: selects the chosen model and uses the methods contained in its model's file (from the model folder)

Detail Files & Purpose below: