# Max Academy Week 4 Project - Agents

This is the repo for Max Academy's [Week 4 project](https://hackmd.io/@timothy1ee/B168iavA0#Practical-LLM-Bootcamp-for-Devs), 
where we're going to build our own agent framework and develop a primitive version of Devin.

## Week 4 Project Milestones

- [x] Milestone 1: Create Chainlit starter
- [x] Milestone 2: Create a basic agent
- [x] Milestone 3: Add artifacts
- [x] Milestone 4: Add an implementation agent
- [ ] Milestone 5 (optional): Supervisor agent (ReAct)
- [ ] Milestone 6 (optional): Reviewer agent (Reflexion)
- [ ] Milestone 7 (optional): Visual feedback (Reflexion)

## Getting Started

### 1. Create a virtual environment

First, create a virtual environment to isolate the project dependencies:
```bash
python -m venv .venv
```

### 2. Activate the virtual environment:

- On Windows:
  ```bash
  .venv\Scripts\activate
  ```
- On macOS and Linux:
  ```bash
  source .venv/bin/activate
  ```

### 3. Install dependencies

Install the project dependencies from the `requirements.txt` file:

```bash
pip install -r requirements.txt
```

### 4. Set up environment variables

- Copy the `.env.sample` file to a new file named `.env`
- Fill in the `.env` file with your API keys

## Running the app

To run the app, use the following command:

```bash
chainlit run app.py -w
``` 

## Updating dependencies

If you need to update the project dependencies, follow these steps:

1. Update the `requirements.in` file with the new package or version.

2. Install `pip-tools` if you haven't already:
   ```bash
   pip install pip-tools
   ```

3. Compile the new `requirements.txt` file:
   ```bash
   pip-compile requirements.in
   ```

4. Install the updated dependencies:
   ```bash
   pip install -r requirements.txt
   ```

This process ensures that all dependencies are properly resolved and pinned to specific versions for reproducibility.