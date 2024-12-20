import subprocess as s 
import json
def generate_query(prompt):
    try:
        f = open ( "maindata.txt")
        data = f.read()
        f.close()
        file1 = open("data.txt","w")
        file1.write(data)
        file1.close()
        command = "ollama run llama3.2 \\Analyze the following database details, including table names, column names, data types, relationships, and any additional constraints provided. Based on this analysis, generate a MySQL query that meets the described requirements. Ensure the query adheres to standard SQL syntax and focuses on clarity, accuracy, and efficiency. Only provide the MySQL query as output, without any explanatory text or additional commentary.{0} and the question is : {1}".format(data ,prompt)
        result =s.run(command, shell=True, capture_output=True, text=True)
        cleaned_output = result.stdout.strip()
        return cleaned_output
    except UnicodeDecodeError as e:
        pass


print(generate_query("how to see the available databases"))

