from pathlib import Path
from . import tools, agent, execute

def main():
    question = "how many coffee saled"
    file_path = Path(".") / "src" / "dataqna" / "data" / "coffee_sales.csv"
    schema = tools.schema_extract(file_path)
    
    code = agent.generate_code("deepseek:deepseek-flash", schema, question)
    result = execute.run_python(code, file_path)
    response = agent.generate_response("deepseek:deepseek-flash", schema, code, result, question)
    print(response)




if __name__=="__main__":
    main()