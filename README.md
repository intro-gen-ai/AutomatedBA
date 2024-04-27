AutomatedBA
This Project is a project to test how different modules when added to LLMs change the performance of a LLM model to write proper SQL queries. In particular we use Snowflake and thus are writing snowflake SQL which has minor syntactical changes. Due to this any reported statistics are mildly different. I worked with my group from Project in AI to adapt this project in attempt to compete in the Data Science showcase on Friday 4/19. 

Project Team:
(Gabe Denton is the only one taking this class)

Gabe Denton - Project Lead - mason.g.denton@vanderbilt.edu - dentonmg, 
Luke Gries - luke.j.gries@vanderbilt.edu, 
Ananth Josyula - ananth.j.josyula@vanderbilt.edu, 
Mayaank Pillai - mayaank.p.pillai@vanderbilt.edu

I (Gabe) am filling out the group members information and as we never truely updated our roles we only have rough regions we worked on except for mine as I pitched the idea for that class. 

Gabe - Snowflake - Architecture - encryption/safety of keys - Model structure - UI - Prompt Structure
Ananth - Additional Models Integration - All Pre & Post Prompts
Mayaank - Bug fixed Rag - Markdowns - made our poster seen on DS's competition day - Testing and getting results
Luke - RAG module

Description of Problem/Opportunity
Proposed Solution/Approach
Project Outline and Timeline
What are the steps to complete the project? State your milestones and the dates you want to complete them.

Goals of project

Goal 1: Usable UI interface and Commandline Chat
Goal 2: Model integration and several modules
Goal 3: Testable way of getting results for different configurations
Goal 4: (Not accomplished) - Creating Graphs (This is extremely easy to do a bad version of with streamlit graphs so we could easily have added it but that is disengenious if you look at commit history, we wanted to make custom matplotlib ones - not as trivial and we failed to get this far)

Project Metrics
Compose 2-5 metrics to determine the success of the project. These should be measureable, and should translate to a letter grade for each.

Metric 1: Is this product usable and can it be configured by an individual in a custom way
Metric 2: Do the different modules improve the performance in any meaningful way

Self-Evaluation
Due April 26, 11:59pm

300-1000 words

Address each of the goals, and assess each of the metrics. Include a statement on each on what you achieved or did not achieve, give support for your assessments.

Goal 1) Yes we achieved this fully. In order to test this try running the file commanline.py with the different tags. These allow a person to chat with a model and recieve a chat with the different models depending on the pipeline configuration they decided on. Furthermore, in order to test the UI try doing streamlit run src/uiHello.py. The instructions on that base page are out of date and will be updated in future works. However, navigate to the Query page and run the different models. They will chat with you, the SQL runs automatically and you get the outputs. 

Goal 2) Yes, we did this quite well. We added several models, all of which can be seen in the src/model/* area as the leaf classes of the step hierachry. Furthermore, all of them can be run that we included in our src/util/convert.json file. If you want to test this configure them correctly with the UI and do some local testing. Additionally, if this is to much to do you can see their results in our testing directory.

Goal 3) Yes, we achieved results for everything. However, our means of testing had numerous errors and would need some improvement. We should have enforced data similarity instead of just column's data similarity. Thus, our results are very very inaccurate as they undercount dramatically. However, as the goal was to have a testable way of determining accuracy if we use even this metric we can see that:
	1) The models are testable with our test set.
	2) The models' base SQL capabilities are benchmarkable.
	3) We found improvement with some configurations on the best model's SQL generation capabilities.

Goal 4) No we removed this as a goal. We found that we still could improve the base project a lot and after some deliberate thought we decided that starting down a complely new path would be more beneficial. We decided that generating a pipeline without agents is likely to be a fundamentally flawed way of improving SQL performance. Thus, we decided to finish the core functionalty the best we could and evaluate our different means of editing the model's context to decide which features were improving and important for the next rendition we will be doing this summer. Above in the goals section I explained why we didn't forfill this goal as if we did it would be against the root idea.

Reflection on Learning
Due April 26, 11:59pm

What do you take away from the project? Has this changed how you understand AI? Does and how does this affect future plans for learning, work, or otherwise?

I learned a lot from this project, mainly focusing around the different ways of editing the space around a model and how to improve performance with context. We didn't attempt to do any agents or fine tuning which would likely be a great tool for future works. Most of what I learned doing this project goes around the different libraries and models, how to use them, what they are good for, and what changes to their inputs will cause. We read numerous papers and looked at many project attempting to do similar things to build our base project. This spanned from papers about prompt engineering to RAG. My take aways are mostly mistakes with this MVP as it has so many inaccuracies in what could be done better like:
	1) Architecture - having the main loop being a single pass through was short sighted as it didn't make the project modular enough to take in major additions of new components we wanted to add (namely agents)
	2) Prompts - Instruction sets and pre prompts are both vital and need a lot more effor to tuning to the question. Switching from our choose a set method we are doing now to a set of high perfomance onces which an agent or algorithm (maybe from encodings) chooses would make a much better product. 
	3) Eliminate markdowns - This architectural choice was adhoc and without everyone understanding it was made, it added a lot of uncertainty into our models outputs as it left empty spaces or forced injections in our prompt builder. I build our models not knowing we were going to use markdowns and switching to congruency would be better for salvaging some of this project and turning it into the next version this summer. While they were not a bad choice they didn't fit into the other modules (RAG & Model) and should be redone or rethought.

This project has not changed my understanding of AI all that much. It has dramatically changed what components I see as super powerful though. I see the future of this project as something heavily relying on tuning agents to databases & previous accempted results. This research has made the process of building a future product significantly less painful as we build modular code much of which will be retoolable when we try to build something. The future works component is only really possible because of the frameworks we build here and the research we did. Without it I would've gone down the wrong path and not really known until it ate even more time than building this did. 

What's Next?
Due April 26, 11:59pm

Do you plan on continuing the project? What will you do with what you've learning?

Yes, I will be continueing this project this summer. However, it will be nothing like this architecture and will be dramatically re-engineered likely from the ground up. Having a base loop was a dumb architecture to being building from as it was built purely for chat completions. This is a reasonable choice for benchmarking the processes we went after. However, it is unlikely to be a good product to sell as a SQL writing product.

Link to correct Video:
https://drive.google.com/file/d/1JiYyTrtO3SM4umRCbG614Jhn0WwP--oa/view?usp=sharing