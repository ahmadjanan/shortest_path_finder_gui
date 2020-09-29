from tkinter import *
from collections import defaultdict, deque
import pandas as pd

class Graph(object):
    def __init__(self):
        self.nodes = set()
        self.edges = defaultdict(list)
        self.distances = {}

    def add_node(self, value):
        self.nodes.add(value)

    def add_edge(self, from_node, to_node, distance):
        self.edges[from_node].append(to_node)
        self.edges[to_node].append(from_node)
        self.distances[(from_node, to_node)] = distance

def dijkstra(graph, initial):
    visited = {initial: 0}
    path = {}

    nodes = set(graph.nodes)

    while nodes:
        min_node = None
        for node in nodes:
            if node in visited:
                if min_node is None:
                    min_node = node
                elif visited[node] < visited[min_node]:
                    min_node = node
        if min_node is None:
            break

        nodes.remove(min_node)
        current_weight = visited[min_node]

        for edge in graph.edges[min_node]:
            try:
                weight = current_weight + graph.distances[(min_node, edge)]
            except:
                continue
            if edge not in visited or weight < visited[edge]:
                visited[edge] = weight
                path[edge] = min_node

    return visited, path

def shortest_path(graph, origin, destination):
    visited, paths = dijkstra(graph, origin)
    full_path = deque()
    _destination = paths[destination]

    while _destination != origin:
        full_path.appendleft(_destination)
        _destination = paths[_destination]

    full_path.appendleft(origin)
    full_path.append(destination)

    return visited[destination], list(full_path)


def calculate(start, end):
    data = pd.read_excel('ml1.xlsx')
    data.columns = ['intersection1','intersection2','distance','traffic']

    intersection1 = data['intersection1'].tolist()
    intersection2 = data['intersection2'].tolist()
    traffic = data['traffic'].tolist()

    graph = Graph()

    for x in range(1,2*(len(intersection1)+1)):
        graph.add_node(x)

    for y in range(0,len(intersection1)):
        if traffic[y] == 1:
            graph.add_edge(intersection1[y], intersection2[y], 15)
            graph.add_edge(intersection2[y], intersection1[y], 15)
        elif traffic[y] == 2:
            graph.add_edge(intersection1[y], intersection2[y], 17)
            graph.add_edge(intersection2[y], intersection1[y], 17)
        else:
            graph.add_edge(intersection1[y], intersection2[y], 20)
            graph.add_edge(intersection2[y], intersection1[y], 20)

    time, path = shortest_path(graph, start, end)
    keys = graph.distances.keys()
    path_times = []

    for x in range(len(path)-1):
        path_times.append(graph.distances[(path[x], path[x+1])])

    paths = ''
    path1 = str(path[0])

    for i in range(0, len(path)-1):
        path1 += ' --> '+str(path[i+1])
        paths += str(path[i]) + ' --> ' + str(path[i+1]) + '\t\t:\t'+ str(path_times[i]) + '\n'
    
    return time, path1, paths


def find():
    t3.delete(0, 'end')
    start=t1.get()
    end=t2.get()
    time,path1,paths=calculate(int(start),int(end))    
    t3.configure(state='normal')
    t4.configure(state='normal')
    t5.configure(state='normal')
    t5.delete(1.0,"end")
    t3.delete(0,'end')
    t3.insert(END, str(time))   
    t4.delete(0,'end')
    t4.insert(END, str(path1))
    t5.insert(END, str(paths))
    t3.configure(state='disabled')
    t4.configure(state='disabled')
    t5.configure(state='disabled')

win = Tk()

lbl1=Label(win, text='Start')
lbl2=Label(win, text='End')
lbl3=Label(win, text='Total Time')
lbl4=Label(win, text='Path')
lbl5=Label(win, text='Edge Time')

t1=Entry(width=40,bd=3)
t2=Entry(width=40,bd=3)
t3=Entry(width=40,bd=3,state='disabled')
t4=Entry(width=40,bd=3,state='disabled')
t5=Text(width=30, height=10,bd=3,state='disabled')        
lbl1.place(x=100, y=50)
t1.place(x=200, y=50)
lbl2.place(x=100, y=100)
t2.place(x=200, y=100)


lbl3.place(x=100, y=200)
t3.place(x=200, y=200)
lbl4.place(x=100, y=250)
t4.place(x=200, y=250)
lbl5.place(x=100,y=300)
t5.place(x=200,y=300)

b1=Button(win, text='     Find     ', bd=3, command=find)
b2=Button(win, text='     Exit     ', bd=3, command=win.destroy)

b1.place(x=100, y=150)
b2.place(x=384, y=150)

win.title('Least Time-consuming Path Finder')
win.geometry("570x500+10+10")
win.mainloop()