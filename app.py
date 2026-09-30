from flask import Flask, request, jsonify
from models.task import Task
from typing import List, Dict, Any
app = Flask(__name__)

# CRUD
# Create, Read, Update and Delete

tasks: List[Task] = []
task_id_control = 1

@app.route('/tasks', methods=['POST'])
def create_task():
    global task_id_control
    data = request.get_json()
    new_task = Task(id=task_id_control, title=data['title'], description=data.get('description'))
    task_id_control += 1
    print(data)
    tasks.append(new_task)
    print(tasks)
    return jsonify({"message":"Nova tarefa criada com sucesso"})

@app.route('/tasks', methods=['GET'])
def get_tasks():
    task_list: List[Dict[str, Any]] = []
    # POSSO USAR O FOR DESSA FORMA TBM 
    # task_list: [task.to_dict() for task in tasks]
    for task in tasks:
        task_list.append(task.to_dict())
        
    output: Dict[str, Any] = {
                "tasks": task_list,
                "total_tasks": len(task_list)
            }
    return jsonify(output)


@app.route('/tasks/<int:id>', methods=['GET'])
def get_task(id: int):
    for t in tasks:
        if t.id == id:
            return jsonify(t.to_dict())
    
    return jsonify({"message": "Não foi possivel encontrar a atividade"}), 404
'''
@app.route('/user/<username>')
def show_user(username: str):
    print(username)
    print(type(username))
    return username

@app.route('/us1/<int:number>')
def show_user(number: int):
    print(number)
    print(type(number))
    return "%s" % number

@app.route('/us2/<float:number>')
def show_user(number: float):
    print(number)
    print(type(number))
    return "%s" % number

@app.route('/us3/<path:number>')
def show_user(number: __path__):
    print(number)
    print(type(number))
    return "%s" % number
'''

@app.route('/tasks/<int:id>', methods=["PUT"])
def update_tasl(id):
    task = None
    for t in tasks:
        if t.id == id:
            task = t
            break
    
    if task == None:
        return jsonify({"message":"Não foi possivel encontrar a atividade"}), 404

    data = request.get_json()
    task.title = data['title']
    task.description = data['description']
    task.completed = data['completed']
    print(task)
    return jsonify({"message":"Tarefa atualizada com sucesso"})
    

@app.route('/tasks/<int:id>', methods=["DELETE"])
def delete_task(id):
    task = None
    for t in tasks:
        print(t.to_dict())
        if t.id == id:
            task = t
            break
    
    if not task:
        return jsonify({"message":"Não foi possivel encontrar a atividade"}), 404
    
    tasks.remove(task)
    return jsonify({"message":"Tarefa deletada com sucesso"})

if __name__ == "__main__":
    app.run(debug=True)