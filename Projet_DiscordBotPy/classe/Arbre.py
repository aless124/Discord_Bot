class node : 
  def __init__(self, question, reponses):
    self.question = question
    self.reponses = reponses
    self.next_nodes = []

  def append(self, question,reponses,previous_question):
    if previous_question == self.question:
      self.next_nodes.append(node(question,reponses))
    else:
      for N in self.next_nodes:
        N.append(question,reponses,previous_question)

  def delete(self, question):
    for N in self.next_nodes:
      if N.question == question:
        del N
      else:
        N.delete(question)

class tree : 
  def __init__(self,first_question):
    self.first_node = node(first_question,[])
    self.current_node = self.first_node

  def append_question(self,question,reponses,previous_question):
    self.first_node.append(question,reponses,previous_question)

  def delete_question(self,question):
    if self.first_node.question == question:
      self.first_node = None
    else:
      self.first_node.delete(question)

  def get_question(self):
    return self.current_node.question

  def send_answer(self, reponse):
    for N in self.current_node.next_nodes:
      if reponse in N.reponses:
        self.current_node = N
        break
    
    return self.current_node.question
  def first_question(self):
    self.current_node = self.first_node
    return self.current_node.question
  
 

T = tree("Voulez vous parlez de Python?")
T.append_question("Choisissez un thème :  POO, language informatique, Python",["Oui"],"Voulez vous parlez de Python?")
T.append_question("Et Ecla ?",["Non"],"Voulez vous parlez de Python?")
# Noeud 2  réponse Oui
T.append_question("La programmation orientée objet (ou POO en abrégé) correspond à une autre manière d'imaginer, de construire et d'organiser son code. La programmation orientée objet repose sur le concept d'objets qui sont des entités qui vont pouvoir posséder un ensemble de variables et de fonctions qui leur sont propres. over",["POO"],"Choisissez un thème :  POO, language informatique, Python")
T.append_question("Un langage informatique est un langage formel non nécessairement Turing-complet utilisé lors de la conception, la mise en œuvre, ou l'exploitation d un système d'information. over",["language informatique"],"Choisissez un thème :  POO, language informatique, Python")
T.append_question("Python est un genre de serpents de la famille des Pythonidae.Ce sont des serpents constricteurs ovipares. La taille des pythons peut varier de 50 cm à 10 m. over ",["python"],"Choisissez un thème :  POO, language informatique, Python")
# Noeud 3 réponse POO
T.append_question("Chatbot **Off**",["over"],"La programmation orientée objet (ou POO en abrégé) correspond à une autre manière d'imaginer, de construire et d'organiser son code. La programmation orientée objet repose sur le concept d'objets qui sont des entités qui vont pouvoir posséder un ensemble de variables et de fonctions qui leur sont propres. over")

# Noeud 3 réponse language informatique
T.append_question("Chatbot **Off**",["over"],"Un langage informatique est un langage formel non nécessairement Turing-complet utilisé lors de la conception, la mise en œuvre, ou l'exploitation d un système d'information. over")

# Noeud 3 réponse python
T.append_question("Chatbot **Off**",["over"],"Python est un genre de serpents de la famille des Pythonidae.Ce sont des serpents constricteurs ovipares. La taille des pythons peut varier de 50 cm à 10 m. over")

# Noeud 2 réponse Non
T.append_question("Thomas Lemaitre \n Luca Morgado \n Axel Senecal \n Paul Chesneau \n Bamhammed METEHRI \n Mathieu GESLIN \n Djebril HARHAD",["Membre"],"Et Ecla ?")
T.append_question("Etre utilisé dans le milieu éducatif et être référencé sur Github",["But"],"Et Ecla ?")
T.append_question("Ecla est un langage de programmation conçu pour être facile à apprendre et à utiliser. C'est un langage polyvalent qui peut être utilisé pour de nombreuses choses différentes.",["Description"],"Et Ecla ?")
T.append_question("Pourquoi les éclairs sont-ils toujours contents ? Parce qu'ils sont Ecla-tants !",["Blague"],"Et Ecla ?")
T.append_question("Non",["Non"],"Et Ecla ?")  
# Noeud 3 réponse Membre
T.append_question("Chatbot **Off**",["over"],"Thomas Lemaitre \n Luca Morgado \n Axel Senecal \n Paul Chesneau \n Bamhammed METEHRI \n Mathieu GESLIN \n Djebril HARHAD")

# Noeud 3 réponse But
T.append_question("Chatbot **Off**",["over"],"Etre utilisé dans le milieu éducatif et être référencé sur Github")

# Noeud 3 réponse Description
T.append_question("Chatbot **Off**",["over"],"Ecla est un langage de programmation conçu pour être facile à apprendre et à utiliser. C'est un langage polyvalent qui peut être utilisé pour de nombreuses choses différentes.")

# Noeud 3 réponse Blague
T.append_question("Chatbot **Off**",["over"],"Pourquoi les éclairs sont-ils toujours contents ? Parce qu'ils sont Ecla-tants !")

# Noeud 3 réponse Non
T.append_question("Chatbot **Off**",["over"],"Non") 
#print(T.get_question())

#question_suivante = T.send_answer("Oui")

#print("question suivante : ",question_suivante)
