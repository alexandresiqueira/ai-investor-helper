# -*- coding: utf-8 -*-


from dtreeviz.trees import *

def dtree_visualize(dtreeClf, X_train, y_train, target_name, feature_names, class_names, title=None):
    viz = dtreeviz(dtreeClf,
              X_train,
              y_train,
              target_name=target_name,
              feature_names=feature_names,
              class_names=class_names,
              title= None)  

    viz.view()
"""
import pydotplus 
# Create DOT data
dot_data = tree.export_graphviz(tree_iris, out_file=None, 
                                #proportion=True,
                                rounded =True,
                                filled=True,
                                feature_names=iris.feature_names,  
                                class_names=["setosa", "versicolor", "virginica"])

# Draw graph
graph = pydotplus.graph_from_dot_data(dot_data)  

# Show graph
Image(graph.create_png())
"""