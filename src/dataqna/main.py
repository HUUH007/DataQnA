from pathlib import Path
from . import tools, agent, execute

def customer_input(
        number_conversation: int,
        file_path: Path
) -> tuple[str, Path]:

    if number_conversation < 1:
        # let the user confirm the analysis data file first.
        file = input("type csv file > ")
        file_path = Path(".") / "src" / "dataqna" / "data" / f"{file}.csv" or file

    customer_input = input("type question > ")

    if customer_input == "exit":
        # make sure customer can end the current conversation.
        return customer_input, file_path
    
    if customer_input == "changefile":
        # make sure customer can change the analysis data file.
        file = input("type csv file > ")
        file_path = Path(".") / "src" / "dataqna" / "data" / f"{file}.csv" or file
        customer_input = input("type question > ")

    return customer_input, file_path

def main():
    print(
    """
        =====================================================
        | if you need to change the file, type `changefile` |
        | if you need to end the conversation, type `exit`  |
        =====================================================
    """)

    number_conversation = 0
    file_path = Path()

    while True:

        question, file_path = customer_input(number_conversation, file_path)
        if question == "exit":
            print("system has been done")
            break

        if not file_path.exists():
            print("response > please try other files")
            continue
        
        schema = tools.schema_extract(file_path)
        code = execute.extract_python(agent.generate_code("deepseek:deepseek-flash", schema, question))
        result = execute.run_python(code, file_path)
        response = agent.generate_response("deepseek:deepseek-flash", schema, code, result, question)

        print()
        print("response > ")
        print(response)
        print()

        number_conversation += 1




if __name__=="__main__":
    main()