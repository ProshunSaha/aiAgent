import sys
from agent_core import Agent

def main():
    if len(sys.argv) < 2:
        print("You need to provide a prompt!")
        sys.exit(1)

    verbose_flag = False
    if len(sys.argv) == 3 and sys.argv[2] == "--verbose":
        verbose_flag = True

    prompt = sys.argv[1]
    
    try:
        agent = Agent()
        result = agent.run(prompt, verbose=verbose_flag)
        # The logs are already printed by the agent.run method for now to maintain CLI behavior
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
