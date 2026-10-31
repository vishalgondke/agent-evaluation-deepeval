# agent-evaluation-deepeval
Built a refund support agent, trace its tool calls, and evaluate both its answers and its behavior with seven DeepEval metrics.
A correct final answer is only one part of a successful agent run. Did the agent identify the customer, check refund eligibility, select the right tools, and refund only the requested items?

This repository is a hands-on learning lab for answering those questions. It pairs a LangChain refund agent with eight evaluation scenarios, seven metrics, and small examples that isolate individual evaluation concepts. Start with the examples, follow the complete evaluation flow, then adapt it to your own agent.

DeepEval report showing task completion, step efficiency, plan quality, and plan adherence.

How the agent works
The agent handles refund requests against the sample purchase records in agent/data.py. Its system prompt requires it to identify the customer, check that purchases are no more than 30 days old and are not in the future, and refund only the items requested.

Tool	Purpose
get_user_purchase_history	Look up a customer's purchases by username
get_today_date	Read the current date for eligibility checks
calculate_right_refund	Add the prices of the requested items
issue_refund_ticket	Return a simulated ticket confirmation for the refund amount
The tools use in-memory sample data. Issuing a ticket returns a string; it does not contact a payment provider or create an external ticket. Eligibility checks are directed by the prompt rather than enforced inside the refund tools.

agent/agent.py creates the agent with an InMemorySaver checkpointer and the Pydantic Answer schema:

class Answer(BaseModel):
    answer: str
    conversation: bool = True
answer contains the user-facing reply. conversation indicates whether the agent needs another user response. Evaluation cases each receive a new thread ID to keep their conversation histories separate.

<img width="450" height="762" alt="image" src="https://github.com/user-attachments/assets/582fc9f0-1626-47c6-998e-29d6d737d043" />



Run evaluations
All seven metrics
evaluations/evaluate_all.py is the main entry point. It performs evaluation in two stages:

dataset.evals_iterator(...) runs four metrics against the execution trace captured by CallbackHandler.
The runner collects the same run's structured answer and tool calls into an LLMTestCase. evaluate(...) then applies the remaining three metrics.
Reusing the response avoids generating a different answer for each metric. The runner disables cache reads and writes and sets inspect_after_run=False, so it does not automatically launch the inspector. The terminal ends with:

Completed all 7 metrics for 8 test cases.
Completion means the evaluation finished; individual metrics can still fail. The script produces two evaluation reports, one for each stage, rather than a single combined export.

Study one metric at a time
For small examples without the refund workflow:

uv run --env-file .env python understanding_metrics/tool_correctness.py
uv run --env-file .env python understanding_metrics/argument_correctness.py
uv run --env-file .env python understanding_metrics/all_metrics.py
For an individual metric applied to the refund agent:

uv run --env-file .env python evaluations/task_completion.py
uv run --env-file .env python evaluations/tool_correctness.py
uv run --env-file .env python evaluations/answer_correctness.py
Each individual script invokes the agent again. Its configuration can differ from the combined runner. In particular, evaluations/argument_correctness.py collects tool calls but omits them from its LLMTestCase; use the combined runner for refund argument evaluation.

Evaluation metrics
These thresholds are defined in build_metrics() in evaluations/evaluate_all.py. Scores run from 0 to 1; a score at or above the threshold passes.

Metric	DeepEval implementation	What it checks	Evidence	Threshold
Task completion	TaskCompletionMetric	Whether the agent achieved the task under the stated refund rules	Execution trace + task description	0.80
Step efficiency	StepEfficiencyMetric	Whether the agent took unnecessary or redundant steps	Execution trace	0.80
Plan quality	PlanQualityMetric	Whether the agent's plan is suitable for the task	Execution trace	0.80
Plan adherence	PlanAdherenceMetric	Whether execution follows the agent's plan	Execution trace	0.80
Argument correctness	ArgumentCorrectnessMetric	Whether tool inputs are appropriate for the request	User input + actual tool calls and arguments	0.90
Tool correctness	ToolCorrectnessMetric	Whether the agent called the expected tools	Actual tool calls + expected tools	0.90
Answer correctness	GEval	Whether the answer reaches the expected logical conclusion	Input + actual answer + expected answer	0.80
The refund dataset specifies expected tool names, without reference arguments. The combined runner also leaves exact matching and tool ordering at their defaults. Its tool correctness score therefore does not establish that arguments or execution order were correct. Inspect those separately.

The GEval rubric checks the logical conclusion against the reference answer. Read the reasons alongside the score to see whether details such as the refund amount were assessed as intended.
